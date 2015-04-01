#!/usr/bin/env python3
import sys
import subprocess
import time
import json
import getopt
import requests


def query_server(token, game_id):
    data = {}
    command_ip = 'ip addr | grep "inet " | grep -v "127." | head -n 1 | tr -s " " | cut -d " " -f3 | cut -d "/" -f1'
    data['hostname'] = subprocess.check_output('hostname -s', shell=True).rstrip().decode()
    data['ip'] = subprocess.check_output(command_ip, shell=True).rstrip().decode()
    data['game'] = game_id
    data['token'] = token

    return data


def notify_master(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    return requests.post(url + '/api/servers', data=json.dumps(data), headers=headers).json()


# python3 notifier.py --token=abc123 --interval=60 --url=https://lanmomo.ca css
def main():
    opts, args = getopt.getopt(sys.argv[1:], 't:i:u:v', ['token=', 'interval=', 'url=', 'verbose'])

    token = None
    interval = None
    url = None
    verbose = None
    invalid = False

    for opt in opts:
        if opt[0] in ('-t', '--token'):
            token = opt[1]
        elif opt[0] in ('-i', '--interval'):
            interval = int(opt[1])
        elif opt[0] in ('-u', '--url'):
            url = opt[1]
        elif opt[0] in ('-v', '--verbose'):
            verbose = True

    if not token:
        print('No token specified')
        invalid = True
    if not url:
        print('No url specified')
        invalid = True
    if not args:
        print('No game_id specified')
        invalid = True
    if invalid:
        exit(1)

    game_id = args[0]

    while True:
        query_result = query_server(token, game_id)

        if verbose:
            print(query_result)

        result = notify_master(url, query_result)

        if verbose:
            print(result)

        if not interval:
            break

        time.sleep(interval)


if __name__ == '__main__':
    main()
