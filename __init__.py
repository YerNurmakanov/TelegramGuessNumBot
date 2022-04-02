import telebot
import config
import random

bot = telebot.TeleBot(config.telegram_token)

prog_number = 0
attemps = 0


@bot.message_handler(commands=['play'])
def welcome_player(message):
    hi = 'Good day! I am a GuessNumberBot!\nEnter following command to start a game: /start_game'
    bot.send_message(message.chat.id, hi)


@bot.message_handler(commands=['start_game'])
def start_game(message):
    global prog_number, attemps, end_game
    prog_number = random.randint(0, 15)
    attemps = 5
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f'{name} enter a number between 0 and 15 \nYou have 5 attemps')


@bot.message_handler(content_types=['text'])
def guess_number(message):
    global attemps, prog_number
    if attemps > 1:
        try:
            if int(message.text) == prog_number:
                bot.send_message(message.chat.id, 'You won!')
                start_game(message)
            else:
                attemps -= 1
                if int(message.text) > prog_number:
                    bot.send_message(message.chat.id, f'Your number is larger, you have {attemps} attemps')
                elif int(message.text) < prog_number:
                    bot.send_message(message.chat.id, f'Your number is smaller, you have {attemps} attemps')
        except ValueError:
            bot.send_message(message.chat.id, 'Please enter a number!')
    else:
        bot.send_message(message.chat.id, f'You lost, no attemps left. The number was {prog_number}')
        start_game(message)


bot.polling(none_stop=True)