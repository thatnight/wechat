# 微信聊天机器人

from wxpy import *
import requests
import time, random

KEY = 'ef3aa1656f90edf4df8d0a66c8ff6b18'
apiUrl = 'http://www.tuling123.com/openapi/api'

bot = Bot(cache_path=True)
reply_group = bot.groups().search('大学之光')[0]
# file_helper=bot.file_helper
robot = Tuling(api_key=KEY)
open_robot = True
print('登录成功!')
bot.file_helper.send_msg('机器人开启中...')


# 文件传输助手的字符串识别
def match_str(msg):
    global open_robot
    if msg.text == '啊':
        open_robot = not open_robot
        is_open(open_robot)
    if msg.text == '饿':
        is_open(open_robot)


def is_open(open_robot):
    if open_robot:
        bot.file_helper.send_msg('机器人已打开')
    else:
        bot.file_helper.send_msg('机器人已关闭')


# 文件传输助手
@bot.register(except_self=False)
def controller(msg):
    if msg.receiver == bot.file_helper:
        match_str(msg)


# 自动回复消息
@bot.register([Friend, reply_group], TEXT, except_self=False)
def auto_reply(msg):
    if open_robot:
        print(msg)
        if msg.sender == bot.self:
            if '百科' in msg.text:
                print(msg.text[2:])
                print(get_reply(msg))
                return get_reply(msg)
        else:
            reply = robot.reply_text(msg)
            print(reply)
            # time.sleep(random.randint(1, 3))
            return '威Bot' + reply

# 自己重写了获取图灵的回复
def get_reply(msg):
    data = {
        'key': KEY,
        'info': msg.text[2:],
        'userid': msg.sender
    }
    try:
        response = requests.post(url=apiUrl, data=data).json()
        return response.get('text')
    except:
        print('异常')
        return


bot.join()
