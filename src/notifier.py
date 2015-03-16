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


# python3 notifier.py --delay=30 --notify=lanmomo.ca css
def main():
    opts, args = getopt.getopt(sys.argv[1:], 'r:n:sP:p:', ['repeat=', 'notify=', 'show', 'protocol=', 'port='])

    show_data = None
    hostname = None
    repeat_delay = None
    protocol_name = "None"
    port=None

    for opt in opts:
        if opt[0] in ('-n', '--notify'):
            hostname = opt[1]
        elif opt[0] in ('-r', '--repeat'):
            repeat_delay = int(opt[1])
        elif opt[0] in ('-s', '--show'):
            show_data = True
        elif opt[0] in ('-P', '--protocol'):
            protocol_name = opt[1]
        elif opt[0] in ('-p', '--port'):
            port=opt[1]

    if not args:
        print('No game_id specified')
        exit(1)
    game_id = args[0]

    # What protocol does Trackmania uses?
    # Call of Duty 4 uses Quake 3 protocol

    if protocol_name.lower() == "gamespy": # Unreal, GMOD, Minecraft (1.8+)
        query_server = protocols.gamespy_query_server
    elif protocol_name.lower() in ("a2s", "source"): # CSS, TF2, Natural Selection, CSGO,
        query_server = protocols.a2s_query_server
    else :
        query_server = protocols.network_identity

    while True:
        query_result = query_server(port) # Server is always the current machine
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
