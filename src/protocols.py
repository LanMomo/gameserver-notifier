import subprocess

default_game_settings = {
    'ut2004' : ('gamespy', 7787),
    'css' : ('a2s', 27015),
    'tf2' : ('a2s', 27015),
    'csgo' : ('a2s', 27015),
    'kf' : ('gamespy', 7717),
    'gmod-prop' : ('a2s', 27015),
    'gmod-ttt' : ('a2s', 27015),
    'mc' : ('gamespy', 25565),
    #'pa' : ('???', 0),
    #'cod4' : ('quake3', 0),
    #'tm' : ('???', 0),
    #'ns2' : ('a2s', 0), #Steam only?
}

def network_identity(port):
    data = {}
    command_ip = "ip addr | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 | grep -v '127.' | head -n 1"
    data['hostname'] = subprocess.check_output("hostname", shell=True).rstrip().decode()
    data['lan_ip'] = subprocess.check_output(command_ip, shell=True).rstrip().decode()
    return data

def gamespy_query_server(port):
    data = {}
    data.update(network_identity(port))
    return data

def a2s_query_server(port):
    data = {}
    data.update(network_identity(port))
    return data

#Packet template
