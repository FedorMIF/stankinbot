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


async def get_file():
    return open('log.txt', 'r', encoding='Windows-1251')
