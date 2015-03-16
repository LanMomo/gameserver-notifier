import subprocess

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