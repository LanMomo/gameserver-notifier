#!/usr/bin/env/python3
import sys
import subprocess
import time
import json
import getopt

def query_server(game_id):
    data = {}
    command_ip = "ip addr | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 | grep -v '127.' | head -n 1"
    data['hostname'] = subprocess.check_output("hostname", shell=True).rstrip().decode()
    data['lan_ip'] = subprocess.check_output(command_ip, shell=True).rstrip().decode()
    data['game_id'] = game_id
    return data

def notify_master(hostname, data):
    payload = json.dumps(data)
    requests.post(hostname, data=payload)


# python3 notifier.py --delay=30 --notify=lanmomo.ca css
def main():
    opts, args = getopt.getopt(sys.argv[1:], 'r:n:s', ['repeat=', 'notify=', 'show'])

    show_data = None
    hostname = None
    repeat_delay = None

    for opt in opts:
        if opt[0] in ('-n', '--notify'):
            hostname = opt[1]
        elif opt[0] in ('-r', '--repeat'):
            repeat_delay = int(opt[1])
        elif opt[0] in ('-s', '--show'):
            show_data = True

    if not args:
        print('No game_id specified')
        exit(1)
    game_id = args[0]

    while True:
        query_result = query_server(game_id)
        if show_data:
            print(query_result)
        if hostname:
            notify_master(hostname, query_result)
        if not repeat_delay:
            exit(0)
        time.sleep(repeat_delay)

if __name__ == '__main__':
    main()
