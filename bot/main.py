import config
import log
import tgflow as tgf
import threading
from UI import goals, notifs,login, misc
from StateMachine import States
from DataBase import db

from telebot import apihelper

apihelper.proxy = {
    'https':'socks5://localhost:9050'}
#apihelper.CONNECT_TIMEOUT=20

lg=log.bot.info

tgf.configure(token=config.token,state=States.HOME)

UI = {}
print(misc.UI)
UI.update(misc.UI)
UI.update(login.UI)
UI.update(goals.UI)
UI.update(notifs.UI)

tgf.start(UI)


