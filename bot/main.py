import config
import log
import tgflow as tgf
import threading
from UI import goals, notifs,login, misc,home
from StateMachine import States
from DataBase import db
from tgflow.api.cli import cliAPI

from telebot import apihelper


#apihelper.proxy = {
    #'https':'socks5://localhost:9050'}
#apihelper.CONNECT_TIMEOUT=20

lg=log.bot.info
print('Hello. Starting bot')

tgf.configure(token=config.token,
              #apiModel=cliAPI,
              state=States.START)

UI = {}
UI.update(misc.UI)
UI.update(home.UI)
UI.update(login.UI)
UI.update(goals.UI)
UI.update(notifs.UI)

print(UI)
tgf.start(UI)


