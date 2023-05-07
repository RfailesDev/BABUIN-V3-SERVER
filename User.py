from datetime import datetime
from time import sleep

import pause

import variables


class UserClass:
    def __init__(self, token):
        self.token = token
        self.limiteds = {}  # ID, time1, wait_time
        # Data
        self.waiting_to_delete = []
        self.bot_task_checkpoint = 0
        self.bot_user_working_item_id = ""
        self.bot_waits_answer_from_function_with_name = ""
        self.secret_key = ""

# {"token": "", "limiteds": {"id": ["", 0]}, "data": {"bot_task_checkpoint": 0, "bot_user_working_item_id": "", "bot_waits_answer_from_function_with_name": ""}}

def pause_until(item):  # tel.id, token, item, time1, countdown
    datetime_ = item[3]
    pause.until(datetime.strptime(datetime_, '%d/%m/%y %H:%M:%S'))  # Ждем до определенного времени(приостанавливаем поток)
    print(f"YEEEEEEEE!!!!!, {item[2]} added to checking list!!!")
    variables.GLOBAL_CHECKING_LIMITEDS.append(item)