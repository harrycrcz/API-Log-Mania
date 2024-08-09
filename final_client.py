import requests
import random
import datetime
import os

API_KEY = os.getenv("API_KEY")
possible_clients = ['Google', 'Amazon', 'Nintendo']
USERNAME = random.choice(possible_clients)


def generate_log():
    events = ['debug', 'info', 'error']
    descriptions = {
        'debug': ['System running smoothly', 'Minor issue detected'],
        'info': ['User logged in', 'Operation completed successfully'],
        'error': ['Error occurred in module', 'Failed to load resource']
    }
    event = random.choice(events)
    description = random.choice(descriptions[event])
    timestamp = datetime.datetime.now().isoformat()
    client = USERNAME

    log = {
        'event': event,
        'description': description,
        'timestamp': timestamp,
        'client': client
    }
    return log


log = generate_log()
response = requests.post('http://localhost:5000/logs',
                         json=log, headers={'API-Key': API_KEY})

print(response.json())
