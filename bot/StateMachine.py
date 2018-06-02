# -*- coding: utf-8 -*-
from enum import Enum
import config

class States(Enum):
    """
    A simple state machine to easier navigation through @decorator functions
    in alarms_bot.py """
    START = 0
    TG = 10
    TG_ERR = 11
    NOT_REG = 13
    GMAIL = 121

    HOME = 200
    NOTIF = 300
    CONTACT = 40
    CONTACT_THANKS = 42

    LNAME= 61

    USER_SAVED = 85

    ERROR = 1
    NOT_IMPLEMENTED = 888
    FETCH = 999             # data is fetching please wait 
