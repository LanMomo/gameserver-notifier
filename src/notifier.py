#!/usr/bin/env/python3
import sys
import time
import json
import getopt
import requests
import protocols


def notify_master(hostname, data):
    payload = json.dumps(data)
    requests.post(hostname, data=payload)

def query_server(protocol_name, port):
    if protocol_name == "gamespy":
        query_method = protocols.gamespy_query_server
    elif protocol_name in ("a2s", "source"):
        query_method = protocols.a2s_query_server
    else :
        query_method = protocols.network_identity

    return query_method(port) # Server is always the current machine

# python3 notifier.py -r 30 -n lanmomo.ca css dod:a2s:27015
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

    games_on_server = [];

    for arg in args:
        # ut2004:gamespy:1337
        parts = arg.split(':')
        game_id = parts[0]
        if len(parts) == 1 :
            protocol = protocols.default_game_settings.get(game_id)
            if protocol == None :
                print("%s does not have a pre-assigned protocol." % game_id)
                continue
        elif len(parts) == 3 and isinstance(parts[1], str) and isinstance(parts[2], int):
            protocol = (parts[1].lower, parts[2])
        game_protocol_pair = (game_id, protocol)
        games_on_server.append(game_protocol_pair)

    if not games_on_server:
        print('No valid game specified')
        exit(1)

    while True:
        for game in games_on_server:
            game_id = game[0]
            protocol = game[1]

            query_result = query_server(*protocol)

            query_result['timestamp'] = int(time.time())
            query_result['game_id'] = game_id

            if show_data:
                print(query_result)
            if hostname:
                notify_master(hostname, query_result)

        if not repeat_delay:
            exit(0)
        time.sleep(repeat_delay)

if __name__ == '__main__':
    main()
