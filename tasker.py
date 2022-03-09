from datetime import datetime
import time
import json

if __name__ == "__main__":
  while True:
    # Verify both the hour and minute in order to reset the counters
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    if hour == 0 and minute == 0:
      # Load the users
      f = open('./data/users.json', 'r')
      users = json.loads(f.read())['users']
      f.close()
      # Reset the counters
      for i, user in enumerate(users):
        users[i]['count'] = 0
      # Save the file
      f = open('./data/users.json', 'w')
      f.write(json.dumps({"users": users}))
      f.close()
    time.sleep(40)