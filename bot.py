import telebot
import bcrypt
import os
import json

# Max number of messages a user can send by day
MAX_COUNT = 5

# Env vars that configures the bot
BOT_TOKEN = os.getenv('BOT_TOKEN')  # Telegram bot token
AUTH_CODE = os.getenv('AUTH_CODE')  # Auth code for the users
GROUP = os.getenv('GROUP')          # Group id to which the message will be send

bot = telebot.TeleBot(BOT_TOKEN)

# Get the users from the json file
def read_users():
  f = open('./data/users.json', 'r')
  users = json.loads(f.read())
  f.close()
  return users['users']

# Create a user hashing the user id
def create_user(new_user):
  hashed_user = str(bcrypt.hashpw(str(new_user).encode('utf-8'), bcrypt.gensalt()))
  users = read_users()
  users.append({
    "id": hashed_user,
    "count": 0
  })
  f = open('./data/users.json', 'w')
  f.write(json.dumps({"users": users}))
  f.close()

# Check if the user has sufficient permissions
def check_user(user_id):
  users = read_users()
  for user in users:
    if bcrypt.checkpw(str(user_id).encode('utf-8'),user['id'][2:-1].encode('utf-8')):
      if user['count'] < MAX_COUNT:
        return True
      else:
        return False
  return False

# Add a request to the user counter
def add_to_counter(user_id):
  users = read_users()
  for i, user in enumerate(users):
    if bcrypt.checkpw(str(user_id).encode('utf-8'),user['id'][2:-1].encode('utf-8')):
      users[i]['count'] = user['count'] + 1
  f = open('./data/users.json', 'w')
  f.write(json.dumps({"users": users}))
  f.close()  

# Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.send_message(message.from_user.id, "Use the command /auth and the code for authorization.")
  bot.send_message(message.from_user.id, "For example: /auth my_auth_code")

# Auth the user. If the user sends the correct auth code
@bot.message_handler(commands=['auth'])
def send_welcome(message):
  if not check_user(message.from_user.id):
    if ' ' in message.text:
      user_auth_code = message.text.split(' ')[1]
      if user_auth_code == AUTH_CODE:
        bot.send_message(message.from_user.id, "Welcome.")
        create_user(str(message.from_user.id))
      else:
        bot.send_message(message.from_user.id, "Try again.")
    else:
      bot.send_message(message.from_user.id, "Try again.")
  else:
    bot.send_message(message.from_user.id, "Hey, I know you.")

# Send the message to the group
@bot.message_handler(commands=['yahoo'])
def send_welcome(message):
  if not check_user(message.from_user.id):
    bot.send_message(message.from_user.id, "I don't know you or you are using the bot to often.")
  else:
    add_to_counter(message.from_user.id)
    bot.send_message(message.from_user.id, "Congrats.")
    bot.send_message(GROUP, "Yahoooooooo")
    audio_file = open('yodel.mp3', 'rb')
    bot.send_audio(GROUP, audio_file, performer="Someone", title="Yahoo")

if __name__ == "__main__":
  # Create the user file if doesn't exists
  if not os.path.exists("./data/users.json"):
    f = open('./data/users.json', 'w')
    f.write(json.dumps({"users": []}))
    f.close()
  # Poll to Telegram
  bot.infinity_polling()
