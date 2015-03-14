#!/usr/bin/env/python3
import subprocess
import time
import json

def query_server(game_id):
    data = {}
    command = "ip addr | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 | grep -v '127.' | head -n 1"
    data['lan_ip'] = subprocess.check_output(command, shell=True).rstrip().decode()
    data['game_id'] = game_id
    return data

def notify_master(hostname, data):
    payload = json.dumps(data)
    if not hostname:
        print(payload)
    else:
        requests.post(hostname, data=payload)


# python3 notifier.py --notify lanmomo.ca --gameid css
def main():
    hostname = None
    game_id = 'css'
    while True:
        notify_master(hostname, query_server(game_id))
        time.sleep(30)

if __name__ == '__main__':
    main()
