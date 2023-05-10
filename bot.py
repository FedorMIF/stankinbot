import random
import re

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove

import log
import way
import bd

from os import listdir
from os.path import isfile, join

bot = Bot('5240511847:AAEHJgb-EJWnzyvp_JE9kq-wFpwf9q0wZ4c')
dp = Dispatcher(bot, storage=MemoryStorage())

kb = (
        ('<', 'left'), 
        ('>','right')
    )

row_bt = (InlineKeyboardButton(text, callback_data=data) for text, data in kb)

menu1 = InlineKeyboardMarkup(row_width=1)
menu1.row(*row_bt)

change_role = InlineKeyboardMarkup()
change_role_button = InlineKeyboardButton(text="Изменить роль", callback_data="change_role")
change_role.add(change_role_button)

role_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
role_keyboard.row("Студент", "Сотрудник", "Администратор")

class row_auds(StatesGroup):
    numbers = State()

class StudentInfo(StatesGroup):
    role = State()
    fullname = State()
    group_number = State()
    group_role = State()
    phone = State()
    email = State()

def validate_user_data(data):
    name, surname, group, role_group, phone, email = data.split(',')

    if not (name and surname and group and role_group):
        return False

    if role_group.lower() == 'староста' and (not phone or not email):
        return False

    if phone and not re.match(r'^\+?\d{10,15}$', phone):
        return False

    if email and not re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email):
        return False

    return True


@dp.message_handler(commands=['createbd'])
async def create_bd(message):
    if await bd.create_tables():
        await bot.send_message(message.chat.id, f'Создалась')
    else:
        await bot.send_message(message.chat.id, f'Что не так')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message):	
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, ' +
                                      f'я бот, который строит маршрут между аудиториями МГТУ Станкин.')
    await bd.add_new_user(message.from_user.first_name, message.chat.id, 'пользователь')

@dp.message_handler(commands=['sendimg'])
async def sen_img(mess):
    onlyfiles = [f for f in listdir('src/png/') if isfile(join('src/png/', f))]
    await bot.send_photo(mess.chat.id, photo=open(f"src/png/{random.choice(onlyfiles)}.png", 'rb'), caption='Это МТГУ Станкин')

@dp.message_handler(commands=['myrole'])
async def send_myrole(mess):
    user_id = mess.from_user.id
    name, role = await bd.give_user_name(user_id)

    if name and role:
        await bot.send_message(mess.chat.id, f"Имя: {name}\nРоль: {role}", reply_markup=change_role)
    else:
        await bot.send_message(mess.chat.id, "Пользователь не найден")

@dp.callback_query_handler(lambda c: c.data == 'change_role')
async def change_role_callback(callback_query: CallbackQuery):

    await bot.send_message(callback_query.from_user.id, "Выберите свою роль:", reply_markup=role_keyboard)
    await bot.answer_callback_query(callback_query.id)

#-----------------Студент----------------------------------

@dp.message_handler(lambda message: message.text == "Студент")
async def student_info_fullname(mess: types.Message, state: FSMContext):
    await state.update_data(role=mess.text.strip())
    await StudentInfo.fullname.set()
    await bot.send_message(mess.chat.id, "Введите ваше имя и фамилию:", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(lambda message: message.text and not message.text.isspace(), state=StudentInfo.fullname)
async def student_info_group_number(mess: types.Message, state: FSMContext):
    await state.update_data(fullname=mess.text.strip())
    await StudentInfo.next()
    await bot.send_message(mess.chat.id, "Введите номер вашей группы:")

@dp.message_handler(lambda message: message.text and not message.text.isspace(), state=StudentInfo.group_number)
async def student_info_group_role(mess: types.Message, state: FSMContext):
    await state.update_data(group_number=mess.text.strip())
    await StudentInfo.next()
    await bot.send_message(mess.chat.id, "Введите вашу роль в группе (Староста или Студент):")

@dp.message_handler(lambda message: message.text in ["Староста", "Студент"], state=StudentInfo.group_role)
async def student_info_phone(mess: types.Message, state: FSMContext):
    await state.update_data(group_role=mess.text)
    await StudentInfo.next()
    await bot.send_message(mess.chat.id, "Введите ваш номер телефона (по желанию):")

@dp.message_handler(lambda message: message.text, state=StudentInfo.phone)
async def student_info_email(mess: types.Message, state: FSMContext):
    await state.update_data(phone=mess.text)
    await StudentInfo.next()
    await bot.send_message(mess.chat.id, "Введите ваш номер электронную почту (по желанию):")

@dp.message_handler(lambda message: message.text, state=StudentInfo.email)
async def process_phone_and_email(mess: types.Message, state: FSMContext):
    await state.update_data(email=mess.text)
 
    user_data = await state.get_data()

    if user_data['role'] == 'Староста':

        user_info = f"{mess.from_user.id},{user_data['role']}"
        admins = await bd.get_admins()
        admin_exept = InlineKeyboardMarkup()
        confirm_button = InlineKeyboardButton("Подтвердить", callback_data=f"confirm_student_info,{user_info}")
        decline_button = InlineKeyboardButton("Отклонить", callback_data=f"decline_student_info,{user_info}")
        admin_exept.add(confirm_button, decline_button)

        if admins:
            admin_id = admins[0]
            await bot.send_message(admin_id, f"Пользователь {user_data['fullname']} с ID {mess.from_user.id} хочет стать {user_data['role']} со следующими данными:\n\n"
                                            f"Имя и фамилия: {user_data['fullname']}\n"
                                            f"Номер группы: {user_data['group_number']}\n"
                                            f"Роль в группе: {user_data['group_role']}\n"
                                            f"Телефон: {user_data['phone']}\n"
                                            f"Email: {user_data['email']}\n\n"
                                            f"Подтвердить информацию?", reply_markup=admin_exept)

            await bot.send_message(mess.chat.id, "Запрос на изменение роли отправлен администратору.")
        else:
            await bot.send_message(mess.chat.id, "Нет администраторов для подтверждения изменения роли.")
    
    else:
        await bd.edit_user_role(int(mess.from_user.id), user_data['fullname'], user_data['role'], user_data['group_number'], user_data['group_role'], user_data['phone'], user_data['email'])
        await bot.send_message(int(mess.from_user.id), f"Ваша роль успешно изменена на Студент")
    # Сброс состояния
    
    await state.finish()

#-----------------Подтверждение данных-------------------

@dp.callback_query_handler(lambda c: c.data.startswith('confirm_student_info'))
async def confirm_role_change(callback_query: types.CallbackQuery):
    _, user_id, role = callback_query.data.split(',')

    _, _, fullname, group_number, group_role, phone, email, _, _ = (callback_query.message.text).split('\n')

    await bd.edit_user_role(int(user_id), fullname.split()[1], role, group_number.split()[1], group_role.split()[1], phone.split()[1], email.split()[1])

    await bot.send_message(int(user_id), f"Ваша роль успешно изменена на Студент")

    #await state.finish()
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('decline_student_info'))
async def decline_role_change(callback_query: CallbackQuery):
    _, user_id = callback_query.data.split(',')

    await bot.send_message(int(user_id), "Администратор отклонил ваш запрос на изменение роли.")
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)

@dp.message_handler(commands=['findway'])
async def what_aud(mess: types.Message, state:FSMContext):
    await bot.send_message(mess.chat.id, 'Напиши *два* номера аудиторий через пробел:\n\n*Аудитория рядом* \t *Аудитория конечная*\n\n_Если хотите отменить команду напишите "Отмена"_', parse_mode="Markdown")
    await state.set_state(row_auds.numbers.state)

@dp.message_handler(state=row_auds.numbers)
async def make_way(mess: types.Message, state:FSMContext):
    await state.update_data(input_auds = mess.text.lower())
    user_data = await state.get_data()
    auds = (user_data['input_auds']).split()
    await state.finish()
    try:
        num1 = auds[0]
        num2 = auds[1]
        if way.pars_build(num1) and way.pars_build(num2):
            onlyfiles = way.this_is_the_way(auds)
            try:
                await bot.send_photo(mess.chat.id, photo=open(f"src/png/{onlyfiles[0]}.png", 'rb'), caption=f'Путь из {num1} в {num2} \nШаг 1 ', reply_markup=menu1)
            except Exception as e:
                print(e)
            await state.finish()
        else:
            await bot.send_message(mess.chat.id, 'Какого то номера нет, попробуй другой номер')
            await state.set_state(row_auds.numbers.state)
    except:
        if auds[0].lower() == 'отмена':
            await bot.send_message(mess.chat.id, 'Вы решили отменить путешествие по коридорам МТГУ Станкин')
        else:
            await bot.send_message(mess.chat.id, 'Ты ввел не числа, введи просто два номера аудиторий через пробел')
            await state.set_state(row_auds.numbers.state)

@dp.message_handler(commands=['test'])
async def send_test(mess):
    onlyfiles = [f for f in listdir('src/png/') if isfile(join('src/png/', f))]
    await bot.send_photo(mess.chat.id, photo=open(f"src/png/{onlyfiles[0]}.png", 'rb'), caption='Шаг 1', reply_markup=menu1)


@dp.callback_query_handler(text = 'left')
@dp.callback_query_handler(text = 'right')
async def callback_inline(query: types.CallbackQuery):
    nums = (query.message.caption).split()
    onlyfiles = way.this_is_the_way([nums[2], nums[4]])
    i = int(nums[6])
    
    if query.data == 'left':
        if i != 1:
            i-=1
            try:
                with open(f'src/png/{onlyfiles[i-1]}.png','rb') as f:
                    await bot.edit_message_media(types.InputMediaPhoto(f), query.message.chat.id, query.message.message_id,  reply_markup=menu1)
                    await bot.edit_message_caption(query.message.chat.id, query.message.message_id, caption = f'Путь из {nums[2]} в {nums[4]} \nШаг: {i}', reply_markup=menu1)
            except Exception as e:
                await log.add(f'{query.message.chat.id} : Ошибка: {e}')
        else:
            await bot.edit_message_caption(query.message.chat.id, query.message.message_id, caption = f'Путь из {nums[2]} в {nums[4]} \nШаг: {i} \nНачало маршрута', reply_markup=menu1)
    
    if query.data == 'right':
        if i != len(onlyfiles):
            i+=1
            try:
                with open(f'src/png/{onlyfiles[i-1]}.png','rb') as f:
                    await bot.edit_message_media( types.InputMediaPhoto(f), query.message.chat.id, query.message.message_id,  reply_markup=menu1)
                    await bot.edit_message_caption(query.message.chat.id, query.message.message_id, caption = f'Путь из {nums[2]} в {nums[4]} \nШаг: {i}',  reply_markup=menu1)
            except Exception as e:
                await log.add(f'{query.message.chat.id} : Ошибка: {e}')
        else:
            await bot.edit_message_caption(query.message.chat.id, query.message.message_id, caption = f'Путь из {nums[2]} в {nums[4]} \nШаг: {i} \nКонец маршрута', reply_markup=menu1) 


@dp.message_handler(content_types=['text'])
async def what_text(mess):
    if mess.text.lower() == 'привет':
        await bot.send_message(mess.chat.id, f'Привет, {mess.from_user.first_name}!')
    else:
        await bot.send_message(mess.chat.id, 'Я Вас не понимаю')

if __name__ == '__main__':
    executor.start_polling(dp)