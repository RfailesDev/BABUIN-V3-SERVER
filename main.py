import hashlib

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
import LoadDataModules
import variables
import system
import network_API
import SafeAsyncio
SafeAsyncio.get_or_create_eventloop()

bot = Bot("6276352725:AAGL-klmb2pgQ9bwVUw-BlNFE-u3AcYGszc")
db = Dispatcher(bot)

async def AutoStop(message, userid):
    AutoStopInput = system.StopInput("Auto", str(int(userid)))
    if AutoStopInput:
        await message.answer(
            AutoStopInput)  # Auto - значит автоматически(ели ошибка, то реакции нет)   - Отменяет ввод предыдущей команды(если она есть)

@db.message_handler(commands=['start'])
async def start(message: types.Message):
    # await bot.send_message(message.chat.id, "Абоба")
    userid = message.from_user.id
    await AutoStop(message, userid)
    answer = system.Login(str(int(userid)))
    await message.answer(answer)
    await message.answer(variables.HELP_MESSAGE)

@db.message_handler(commands=['AddLimit'])
async def AddLimit(message: types.Message):
    # await bot.send_message(message.chat.id, "Абоба")
    userid = message.from_user.id
    await AutoStop(message, userid)
    answer = system.AddLimit("Command", str(int(userid)), message)
    if answer:
        await message.answer(answer)

@db.message_handler(commands=['RemoveLimit'])
async def RemoveLimit(message: types.Message):
    # await bot.send_message(message.chat.id, "Абоба")
    userid = message.from_user.id
    await AutoStop(message, userid)
    answer = system.RemoveLimit("Command", str(int(userid)), message)
    if answer:
        await message.answer(answer)

@db.message_handler(commands=['ShowLimits'])
async def ShowLimits(message: types.Message):
    userid = message.from_user.id
    await AutoStop(message, userid)
    answer = system.ShowLimits("Command", str(int(userid)))
    if answer:
        await message.answer(answer, parse_mode="MarkdownV2")

@db.message_handler(commands=['SetCookie'])
async def SetCookie(message: types.Message):
    userid = message.from_user.id
    await AutoStop(message, userid)
    answer = system.SetCookie("Command", str(int(userid)), message)
    if answer:
        await message.answer(answer)

@db.message_handler(commands=['StopInput'])
async def StopInput(message: types.Message):
    userid = message.from_user.id
    answer = system.StopInput("Command", str(int(userid)))
    if answer:
        await message.answer(answer)

@db.message_handler(commands=['SecretKey'])
async def SecretKey(message: types.Message):
    userid = message.from_user.id
    answer = system.SecretKey("Command", str(int(userid)))
    if answer:
        await message.answer(answer, parse_mode="MarkdownV2")

@db.message_handler()
async def ChatMessage(message: types.Message):
    userid = message.from_user.id
    userid = hashlib.md5(str(userid).encode()).hexdigest()
    print(1)
    print(variables.USERS_DATABASE)
    account_exists = str(userid) in variables.USERS_DATABASE
    if account_exists:  # Если аккаунт существует
        print(2)
        # Получаем информацию о последней функции(ответ на которую ждет от пользователя бот)
        user_object = variables.USERS_DATABASE[str(userid)]
        ResponseableLastCommand = user_object.bot_waits_answer_from_function_with_name

        if not message.text.startswith("/") and ResponseableLastCommand:  # чтобы команды игнорировались, а также пропускал только тогда, когда ожидается ответ на команду.
            answer = ""
            if ResponseableLastCommand == "AddLimit":
                answer = system.AddLimit("Message", str(int(message.from_user.id)), message)
            elif ResponseableLastCommand == "SetCookie":
                print(SetCookie)
                answer = system.SetCookie("Message", str(int(message.from_user.id)), message)
            elif ResponseableLastCommand == "RemoveLimit":
                answer = system.RemoveLimit("Message", str(int(message.from_user.id)), message)
            if answer:
                await message.answer(answer)
    else:
        return variables.REGISTER_ERROR

executor.start_polling(db)