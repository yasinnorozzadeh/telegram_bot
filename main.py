import random
import telebot
import khayyam
from gtts import gTTS
from qrcode import make

mybot = telebot.TeleBot("5591959528:AAGy7ODAuQhbfNGe-iPRL7aJakJsFU7OXeA")
NUMBER = random.randint(0 ,100)

@mybot.message_handler(commands=["start"])
def welcom(message):
    mybot.reply_to(message, f"welcom {message.chat.first_name} to python bot")

@mybot.message_handler(commands=["help"])
def help(message):
    mybot.reply_to(message, "/game\t for guess number game\n/age\t for calculate your age\n/voice\t for convert text to voice\n/max\t for find biggest numbers\n/argmax\t for find biggest index of numbers\n/qrcode\t for make qrcode\n/help\t for show commands")

@mybot.message_handler(commands=["qrcode"])
def qrcode(message):
    message = mybot.send_message(message.chat.id, "give me youre text/url/...")
    mybot.register_next_step_handler(message, makeqrcode)
def makeqrcode(message):
    img = make(message.text)
    img.save("qrcode.png")
    image = open("qrcode.png","rb")
    try:
        mybot.send_photo(message.chat.id, image)
    except:
        mybot.send_message(message.chat.id, "operation was unsuccessful")

@mybot.message_handler(commands=["max"])
def max_list(message):
    message = mybot.send_message(message.chat.id, "give me numbers speling with , (1,2,3,4,5,...)")
    mybot.register_next_step_handler(message, maxlist)
def maxlist(message):
    number = message.text
    number_list = list(map(int, number.split(",")))
    max_list = str(max(number_list))
    try:
        mybot.send_message(message.chat.id, "max number of list: " + max_list)
    except:
        mybot.send_message(message.chat.id, "you didn't input corectly numbers")

@mybot.message_handler(commands=["voice"])
def voice(message):
    message = mybot.send_message(message.chat.id, "send ne an english sentence")
    mybot.register_next_step_handler(message, t_2_v)
def t_2_v(message):
    voice = gTTS(message.text,lang="en",slow=False)
    voice.save("voice.mp3")
    voice = open("voice.mp3", "rb")
    try:
        mybot.send_voice(message.chat.id, voice)
    except:
        mybot.send_message(message.chat.id, "enter text in english")

@mybot.message_handler(commands=["age"])
def age(message):
    message = mybot.send_message(message.chat.id, "give me date of your birth (1387.1.18)")
    mybot.register_next_step_handler(message, ageconvert)
def ageconvert(message):
    user_birthday = message.text.split(".")
    if len(user_birthday) == 3:
        today = khayyam.JalaliDatetime.now()
        birthday = khayyam.JalaliDatetime(user_birthday[0], user_birthday[1], user_birthday[2])
        age_days = today - birthday
        mybot.send_message(message.chat.id, "you are" + str(age_days.days // 365) + "years , " + str(age_days.days) + "days")

@mybot.message_handler(commands=["game"])
def game(message):
    message = mybot.send_message(message.chat.id, "you must recognize the desired number(0, 100)")
    mybot.register_next_step_handler(message, game_1)
def game_1(message):
    global NUMBER
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    btn1 = telebot.types.KeyboardButton('new game')
    markup.add(btn1)
    if message.text == "new game":
        NUMBER = random.randint(0, 100)
        mybot.register_next_step_handler_by_chat_id(message.chat.id, game)
    else:
        try:
            if int(message.text) == NUMBER:
                mybot.send_message(message.chat.id, "your win!!", reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
                NUMBER = random.randint(0, 100)
            elif int(message.text) > NUMBER:
                message = mybot.send_message(message.chat.id, 'lower', reply_markup=markup)
                mybot.register_next_step_handler(message, game_1)
            elif int(message.text) < NUMBER:
                message = mybot.send_message(message.chat.id, 'bigger',reply_markup=markup)
                mybot.register_next_step_handler(message, game_1)
        except:
            mybot.send_message(message.chat.id, "give me a number", reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))

@mybot.message_handler(commands=["argmax"])
def index_max(message):
    message = mybot.send_message(message.chat.id, "give me numbers speling with , (1,2,3,4,5,...)")
    mybot.register_next_step_handler(message, max_index)
def max_index(message):
    number = message.text
    number_list = list(map(int, number.split(",")))
    max_list_index = str(number_list.index(max(number_list)))
    try:
        mybot.send_message(message.chat.id, "max index  of list: " + max_list_index)
    except:
        mybot.send_message(message.chat.id, "you didn't input corectly numbers")

@mybot.message_handler(commands="song")
def song(message):
    pass
mybot.polling()