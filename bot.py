import telebot
import bcrypt
import os
import json

BOT_TOKEN = os.getenv('BOT_TOKEN')
AUTH_CODE = os.getenv('AUTH_CODE')
GROUP = os.getenv('GROUP')

bot = telebot.TeleBot(BOT_TOKEN)

def read_users():
  f = open('users.json', 'r')
  users = json.loads(f.read())
  f.close()
  return users['users']

def save_user(new_user):
  hashed_user = str(bcrypt.hashpw(str(new_user).encode('utf-8'), bcrypt.gensalt()))
  users = read_users()
  users.append({
    "id": hashed_user,
    "count": 0
  })
  f = open('users.json', 'w')
  f.write(json.dumps({"users": users}))
  f.close()

def check_user(user_id):
  users = read_users()
  for user in users:
    if bcrypt.checkpw(str(user_id).encode('utf-8'),user['id'][2:-1].encode('utf-8')):
      return True
  return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.send_message(message.from_user.id, "Use the command /auth and the code for authorization.")
  bot.send_message(message.from_user.id, "For example: /auth my_auth_code")
  print(check_user(message.from_user.id))

@bot.message_handler(commands=['auth'])
def send_welcome(message):
  if not check_user(message.from_user.id):
    if ' ' in message.text:
      user_auth_code = message.text.split(' ')[1]
      if user_auth_code == AUTH_CODE:
        bot.send_message(message.from_user.id, "Welcome.")
        save_user(str(message.from_user.id))
      else:
        bot.send_message(message.from_user.id, "Try again.")
    else:
      bot.send_message(message.from_user.id, "Try again.")
  else:
    bot.send_message(message.from_user.id, "Hey, I know you.")

@bot.message_handler(commands=['yahoo'])
def send_welcome(message):
  if not check_user():
    bot.send_message(message.from_user.id, "I don't know you.")
  else:
    bot.send_message(message.from_user.id, "Congrats.")
    bot.send_message(GROUP, "Yahoooooooo")

if __name__ == "__main__":

  if not os.path.exists("./users.json"):
    f = open('users.json', 'w')
    f.write(json.dumps({"users": []}))
    f.close()

  bot.infinity_polling()
