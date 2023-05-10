import re



async def add(text):
    import time
    t = time.localtime()
    time_day = time.strftime("%d.%m - %H:%M:%S", t)
    file_log = open('log.txt', 'a')
    file_log.write(str(time_day) +' : ' + text + '\n')
    file_log.close()


async def time():
    import time
    t = time.localtime()
    current_time = time.strftime("%c", t)
    return str(current_time)


def bro_list():
    bros = []
    file_bro = open('bro.txt', 'r')
    for st in file_bro:
        st = re.sub(r'\n', '', str(st))
        bros.append(int(st))
    file_bro.close()
    return bros


def kis_list():
    kises = []
    file_kis = open('kis.txt', 'r')
    for st in file_kis:
        st = re.sub(r'\n', '', str(st))
        kises.append(int(st))
    file_kis.close()
    return kises


def to_bro_list(bro_id):
    with open('bro.txt', 'a') as f:
        f.write('\n' + bro_id)


def to_kis_list(kis_id):
    with open('kis.txt', 'a') as f:
        f.write('\n' + kis_id)


async def get_file():
    return open('log.txt', 'r', encoding='Windows-1251')
