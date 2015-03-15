#!/usr/bin/env/python3
import sys
import time
import json
import getopt
import requests
import subprocess

class Protocol:
    def query_server(self, hostname, port):
        data = {}
        command_ip = "ip addr | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 | grep -v '127.' | head -n 1"
        data['hostname'] = subprocess.check_output("hostname", shell=True).rstrip().decode()
        data['lan_ip'] = subprocess.check_output(command_ip, shell=True).rstrip().decode()
        return data

class GameSpy(Protocol):
    pass

class Main:
    protocols = {
        "gamespy": GameSpy,
        "base": Protocol,
    }

def notify_master(hostname, data):
    payload = json.dumps(data)
    requests.post(hostname, data=payload)


# python3 notifier.py --delay=30 --notify=lanmomo.ca css
def main():
    opts, args = getopt.getopt(sys.argv[1:], 'r:n:sP:p:', ['repeat=', 'notify=', 'show', 'protocol=', 'port='])

    show_data=None
    hostname=None
    repeat_delay=None
    protocol_name="Base"
    port=None

    for opt in opts:
        if opt[0] in ('-n', '--notify'):
            hostname=opt[1]
        elif opt[0] in ('-r', '--repeat'):
            repeat_delay=int(opt[1])
        elif opt[0] in ('-s', '--show'):
            show_data=True
        elif opt[0] in ('-P', '--protocol'):
            protocol_name=opt[1]
        elif opt[0] in ('-p', '--port'):
            port=opt[1]

    if not args:
        print('No game_id specified')
        exit()
    game_id = args[0]

    try:
        protocol_class = Main.protocols[protocol_name.lower()]
    except IndexError:
        protocol_class = Protocol()
    p = protocol_class()

    while True:
        query_result = p.query_server("localhost", port)
        query_result['game_id'] = game_id

        if show_data:
            print(query_result)
        if hostname:
            notify_master(hostname, query_result)
        if not repeat_delay:
            break
        time.sleep(repeat_delay)

if __name__ == '__main__':
    main()
