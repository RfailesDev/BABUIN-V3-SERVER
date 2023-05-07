import threading

from aiogram import Bot, Dispatcher, executor, types
import ParseItemData
import ParseUserData
import User
import functions
import variables
import hashlib

def Login(id):
    account_exists = id in variables.USERS_DATABASE
    if account_exists:  # Входим в аккаунт
        return f"Аккаунт бота инициализирован. ID: `{id}`. {variables.LOGIN_MESSAGE}"
    else:  # Создаем аккаунт
        new_user = User.UserClass("")
        variables.USERS_DATABASE[hashlib.md5(str(id).encode()).hexdigest()] = new_user
        new_user.secret_key = hashlib.md5(str(id).encode()).hexdigest()
        return f"Аккаунт успешно создан. ID: `{id}`. {variables.LOGIN_MESSAGE}"

def AddLimit(TYPE, id, MessageObject: types.Message):
    id = hashlib.md5(str(id).encode()).hexdigest()

    message = MessageObject.text
    account_exists = id in variables.USERS_DATABASE
    if account_exists:  # Если аккаунт существует
        user_object = variables.USERS_DATABASE[id]
        if user_object.token:
            # Сначала нужно написать - "Хорошо, напишите id предмета:", потом уже добавлять
            if user_object.bot_task_checkpoint != 0 and TYPE == "Message" and user_object.bot_waits_answer_from_function_with_name == "AddLimit":  # Если это вводится просто через сообщение(не команда)
                Checkpoint = user_object.bot_task_checkpoint
                user_object.bot_task_checkpoint += 1
                # Сразу переключаемся на новый чекпоинт. В скрипте обрабатывается неизмененная версия(чекпоинт-1), т.к потом чекпоинт не получится прибавить из-за return, по этому делаю это заранее...

                if Checkpoint == 1:  # Вводим id предмета
                    ItemId = str(int(message))
                    ItemData = ParseItemData.GetAssetInfo(ItemId)
                    user_object.limiteds[ItemId] = [0, ItemData[0], ItemData[1]]
                    user_object.bot_user_working_item_id = ItemId
                    return variables.ITEM_TYPE_DATE
                if Checkpoint == 2:  # Вводим дату
                    item_id = user_object.bot_user_working_item_id
                    user_object.limiteds[item_id][0] = str(message)
                    return variables.ITEM_TYPE_TIMER
                if Checkpoint == 3:  # Вводим таймер отключения
                    item_id = user_object.bot_user_working_item_id
                    user_object.limiteds[item_id][1] = str(int(message))

                    item = [id, user_object.token, item_id, user_object.limiteds[item_id][0], str(int(message))]  # tel.id, token, item, time1, countdown
                    t = threading.Thread(target=User.pause_until, args=(item,))
                    t.start()
                    print(variables.GLOBAL_CHECKING_LIMITEDS)
                    user_object.bot_task_checkpoint = 0
                    user_object.bot_waits_answer_from_function_with_name = ""
                    return variables.ITEM_ADDED

            else:
                if TYPE == "Command":
                    user_object.bot_waits_answer_from_function_with_name = "AddLimit"
                    user_object.bot_task_checkpoint = 1
                    return variables.ITEM_TYPE_ID
                else:
                    return
        else:  # Если нет токена
            return variables.TOKEN_REQUESTS
    else:
        return variables.REGISTER_ERROR

def RemoveLimit(TYPE, id, MessageObject: types.Message):
    id = hashlib.md5(str(id).encode()).hexdigest()

    message = MessageObject.text
    account_exists = id in variables.USERS_DATABASE
    if account_exists:  # Если аккаунт существует
        user_object = variables.USERS_DATABASE[id]
        # Сначала нужно написать - "Хорошо, напишите id предмета:", потом уже добавлять
        if user_object.bot_task_checkpoint != 0 and TYPE == "Message" and user_object.bot_waits_answer_from_function_with_name == "RemoveLimit":  # Если это вводится просто через сообщение(не команда)
            Checkpoint = user_object.bot_task_checkpoint
            user_object.bot_task_checkpoint += 1
            # Сразу переключаемся на новый чекпоинт. В скрипте обрабатывается неизмененная версия(чекпоинт-1), т.к потом чекпоинт не получится прибавить из-за return, по этому делаю это заранее...

            if Checkpoint == 1:  # Вводим id предмета
                ItemId = str(int(message))
                user_object.limiteds[ItemId][1] = int(message)
                FindedItems = functions.FindInListFromIncludeValue(id, variables.GLOBAL_LIMITEDS)  # Сначала нахожу в списке все предметы от определенного пользователя
                FindedItem = functions.FindInListFromIncludeValue(ItemId, FindedItems)
                print(FindedItem)
                variables.GLOBAL_LIMITEDS.remove(variables.GLOBAL_LIMITEDS.index(FindedItem))  # Потом нахожу определенный предмет
                print(variables.GLOBAL_LIMITEDS)
                user_object.bot_task_checkpoint = 0
                user_object.bot_waits_answer_from_function_with_name = ""
                return variables.ITEM_REMOVED

        else:
            if TYPE == "Command":
                user_object.bot_waits_answer_from_function_with_name = "RemoveLimit"
                user_object.bot_task_checkpoint = 1
                return variables.ITEM_TYPE_ID_REMOVE
            else:
                return
    else:
        return variables.REGISTER_ERROR

def ShowLimits(TYPE, id):
    id = hashlib.md5(str(id).encode()).hexdigest()

    account_exists = id in variables.USERS_DATABASE
    if account_exists:  # Если аккаунт существует
        user_object = variables.USERS_DATABASE[id]
        if TYPE == "Command":  # Если это вводится через команду
            ReturnText = ""
            ReturnText += variables.SHOW_ITEMS+f"\n\n"
            limiteds = user_object.limiteds
            if len(limiteds) > 0:
                for id, item in limiteds.items():
                    if len(item) >= 3:  # Если предмет корректный.
                        itemId = item[1].replace(":", "\:")
                        itemType = item[2].replace(":", "\:")
                        ReturnText += f"*{str(id)}* \- {itemId}\({str(itemType)}\)\n"
                return ReturnText
            else:  # Если база данных лимиток пуста:
                return functions.AdaptiveMarkdown(variables.SHOW_ITEMS_EMPTY)
    else:
        return functions.AdaptiveMarkdown(variables.REGISTER_ERROR)

def SetCookie(TYPE, id, MessageObject: types.Message):
    id = hashlib.md5(str(id).encode()).hexdigest()

    message = MessageObject.text
    account_exists = id in variables.USERS_DATABASE
    if account_exists:  # Если аккаунт существует
        user_object = variables.USERS_DATABASE[id]
        if TYPE == "Command":  # Если это вводится через команду
            user_object.bot_waits_answer_from_function_with_name = "SetCookie"
            user_object.bot_task_checkpoint = 1
            return variables.ENTER_COOKIE
        elif user_object.bot_task_checkpoint == 1 and user_object.bot_waits_answer_from_function_with_name == "SetCookie":
            # Пользователь вводит токен.
            EnteredCookie = message
            AccountID = functions.CheckCookie(EnteredCookie)
            if AccountID:  # Если Cookie верный:
                user_object.token = EnteredCookie
                AccountData = ParseUserData.GetUsername(AccountID)

                user_object.bot_waits_answer_from_function_with_name = ""
                user_object.bot_task_checkpoint = 0

                return f"{variables.ENTER_COOKIE_DONE}\n\nАккаунт: {AccountData['displayName']}(@{AccountData['name']})"  # Cookie введен правильно
            else:
                return variables.ENTER_COOKIE_ERROR  # Неправильно введен Cookie
    else:
        return variables.REGISTER_ERROR

def StopInput(TYPE, id):
    id = hashlib.md5(str(id).encode()).hexdigest()

    account_exists = id in variables.USERS_DATABASE
    if account_exists:  # Если аккаунт существует
        user_object = variables.USERS_DATABASE[id]
        if user_object.bot_waits_answer_from_function_with_name:
            StoppedCommandName = str(user_object.bot_waits_answer_from_function_with_name)
            user_object.bot_waits_answer_from_function_with_name = ""
            user_object.bot_task_checkpoint = 0
            return f"{variables.STOP_INPUT_COMMAND_DONE}.\nКоманда /{StoppedCommandName} не выполнена."
        else:
            if TYPE != "Auto":  # Если автоматически, то ответ нне пишем
                return variables.STOP_INPUT_COMMAND_NONE
    else:
        if TYPE != "Auto":  # Если автоматически, то ответ нне пишем
            return variables.REGISTER_ERROR

def SecretKey(TYPE, id):
    id = hashlib.md5(str(id).encode()).hexdigest()

    account_exists = id in variables.USERS_DATABASE
    if account_exists:  # Если аккаунт существует
        user_object = variables.USERS_DATABASE[id]
        ret = f"Хорошо, вот ваш secret-key: ||{user_object.secret_key}||\n\n*Не сообщайте его никому!*"
        return functions.AdaptiveMarkdown(ret)
    else:
        if TYPE != "Auto":  # Если автоматически, то ответ нне пишем
            return functions.AdaptiveMarkdown(variables.REGISTER_ERROR)