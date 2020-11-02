import config
import telebot
import sqlite3

db = sqlite3.connect("database.db", check_same_thread=False)

cursor = db.cursor()



from telebot import types

TOKEN = '1129238142:AAGdK5z3tBFnPcRFcaSzootUvvfrYj1YPdY'

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def startmessage(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	itembtn1 = types.KeyboardButton('Добавить задачу')
	itembtn2 = types.KeyboardButton('Отметить задачу выполненной')
	itembtn3 = types.KeyboardButton('Просмотреть задачи')
	markup.add(itembtn1, itembtn2, itembtn3)
	bot.send_message(message.chat.id, "Ниже ты можешь выбрать необходимую тебе опцию.", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def createTask(message):
	if(message.text == 'Добавить задачу'):
		markup = types.ReplyKeyboardRemove(selective=False)
		msg = bot.send_message(message.chat.id, 'Введите название задачи', reply_markup=markup)
		bot.register_next_step_handler(msg, askTaskName)
	elif(message.text == 'Просмотреть задачи'):
		cursor.execute("SELECT COUNT(*) FROM tasks WHERE warn = 1 AND done = 0")
		result = cursor.fetchone()
		if(result[0] == 0):
			bot.send_message(message.chat.id, '❌ Срочных задач нет.')
		else:
			global fTasks
			fTasks = []
			for row in cursor.execute("SELECT * FROM tasks WHERE done = 0 AND warn = 1"):
				fTasks.append(row[0])
			else:
				sfTasks = '\n- '
				maintitle = 'Срочные задачи:\n\n'
				sfTasks2 = maintitle + '- ' + sfTasks.join(fTasks) 
				bot.send_message(message.chat.id, sfTasks2)

		cursor.execute("SELECT COUNT(*) FROM tasks WHERE warn = 0 AND done = 0")
		result = cursor.fetchone()
		if(result[0] == 0):
			bot.send_message(message.chat.id, '❌ Недельных задач нет.')
		else:
			global sTasks
			sTasks = []
			for row in cursor.execute("SELECT * FROM tasks WHERE done = 0 AND warn = 0"):
				sTasks.append(row[0])
			else:
				maintitle = 'Недельные задачи:\n\n'
				ssTasks = '\n- '
				sTasks2 = maintitle + '- ' + ssTasks.join(sTasks) 
				bot.send_message(message.chat.id, sTasks2)
	elif(message.text == 'Отметить задачу выполненной'):
		markup = types.InlineKeyboardMarkup(row_width=4)
		for row in cursor.execute("SELECT * FROM tasks WHERE done = 0"):
			item = types.InlineKeyboardButton(row[0], callback_data='')
		bot.send_message(message.chat.id, 'Какую задачу вы хотите отметить выполненной: ')
def askTaskName(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	itembtn1 = types.KeyboardButton('Да')
	itembtn2 = types.KeyboardButton('Нет')
	markup.add(itembtn1, itembtn2)
	global taskName
	taskName = message.text
	msg = bot.send_message(message.chat.id, 'Окей, это срочная задача?', reply_markup=markup)
	bot.register_next_step_handler(msg, setWarn)

def setWarn(message):
	if(message.text == "Да"):
		global warn
		warn = 1
	else:
		warn = 0
	markup = types.ReplyKeyboardMarkup(row_width=2)
	itembtn1 = types.KeyboardButton('Добавить задачу')
	itembtn2 = types.KeyboardButton('Отметить задачу выполненной')
	itembtn3 = types.KeyboardButton('Просмотреть задачи')
	markup.add(itembtn1, itembtn2, itembtn3)
	bot.send_message(message.chat.id, 'Отлично, задача добавлена.', reply_markup=markup)
	cursor.execute("INSERT INTO tasks VALUES ('{0}', '{1}', '0', '0')".format(taskName, warn))
	db.commit()


bot.polling()
'''hello world'''