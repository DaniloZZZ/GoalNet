import config

import tgflow as tgf

#from modules import login, student, apply
from UI import goals, notifs
from DataBase import db


tgf.configure(token=config.token,state='start')

UI ={
    'start':{
        't':'hello there!'
    }
}
UI.update(goals.UI)
UI.update(notifs.UI)

tgf.start(UI)


