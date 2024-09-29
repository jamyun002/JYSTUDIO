import subprocess

import time

# bot.py와 bot1.py를 독립적으로 실행

subprocess.Popen(['python', '/home/container/bot/bot.py'])

subprocess.Popen(['python', '/home/container/bot/bot1.py'])

subprocess.Popen(['python', '/home/container/bot/bot2.py'])

subprocess.Popen(['python', '/home/container/bot/bot3.py'])

subprocess.Popen(['python', '/home/container/bot/bot4.py'])

subprocess.Popen(['python', '/home/container/bot/bot5.py'])

# 메인 스크립트가 종료되지 않도록 대기

try:

    while True:

        time.sleep(1)

except KeyboardInterrupt:

    print("프로그램 종료")