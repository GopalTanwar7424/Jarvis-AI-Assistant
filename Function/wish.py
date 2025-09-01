from datetime import date
import datetime

from Data.dlg_data.dlg import good_morningdlg
from Head.mouth import speak
import random
from Data.dlg_data.dlg import *
from Function.welcome import welcome

today = date.today()
formated_date = today.strftime("%d %b %y")
nowx = datetime.datetime.now()


def wish():
    welcome()
    current_hour = nowx.hour

    if 5 <= current_hour < 12:
        gd_glg = random.choice(good_morningdlg)
        speak(gd_glg)
    elif 12 <= current_hour < 17:
        ga_glg = random.choice(good_afternoondlg)
        speak(ga_glg)
    elif 17 <= current_hour < 21:
        ge_glg = random.choice(good_eveningdlg)
        speak(ge_glg)
    else:
        gn_glg = random.choice(good_nightdlg)
        speak(gn_glg)



