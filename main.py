import subprocess
import logging
import time

LOG_FILE = 'container_monitor.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')
threshold_seconds = 0.125* 60 

def convert_to_seconds(running_for):
    running_for = running_for.strip().lower()
    
    if 'less than' in running_for:
        return 0  
    
    hours = 0
    minutes = 0
    seconds = 0
    
    if 'h' in running_for:
        hours_part = running_for.split('h')[0]
        hours = int(hours_part.strip()) if hours_part.strip().isdigit() else 0
        running_for = running_for.split('h')[1].strip()

    if 'm' in running_for:
        minutes_part = running_for.split('m')[0]
        minutes = int(minutes_part.strip()) if minutes_part.strip().isdigit() else 0
        running_for = running_for.split('m')[1].strip() if 'm' in running_for else ''

    if 's' in running_for:
        seconds_part = running_for.split('s')[0]
        seconds = int(seconds_part.strip()) if seconds_part.strip().isdigit() else 0

    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

while True:
        output = subprocess.check_output(['docker', 'ps', '--format', "{{.ID}}\t{{.Names}}\t{{.Networks}}\t{{.RunningFor}}"])
        containers = [line.decode('utf-8').strip().split('\t') for line in output.splitlines()]
        
        networks = {}

        for container in containers:
            id, name, net, running_for = container
            net = net.split(',')
            for network in net:
                if network not in networks:
                    networks[network] = []
                networks[network].append((id, name, running_for))

        for network, containers in networks.items():
            running_for_seconds = [convert_to_seconds(container[2]) for container in containers]
            
            
            if all(seconds > threshold_seconds for seconds in running_for_seconds):
                for id, name, _ in containers:
                    logging.info(f'Stopping container {name} (ID: {id}) after running for more than {threshold_seconds} seconds.')
                    subprocess.call(['docker', 'stop', id])


    






