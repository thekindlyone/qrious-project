import subprocess
import json
from datetime import datetime
import time
import sys
import csv
import os

container_name = 'nginx'
output_file = os.path.expanduser('~/logs/docker_status.log')
if len(sys.argv)>1:
    container_name = sys.argv[1]

delim = '|,|'
headers = ['timestamp', 'time', 'health', 'CPUPerc', 'MemPerc', 'MemUsage', 'BlockIO', 'NetIO', 'Container', 'ID', 'Name', 'PIDs']
fmt = delim.join(f"{{{{.{header}}}}}" for header in headers[3:])
healthcheck_command = ["docker", "inspect", container_name, "--format='{{.State.Health.Status}}'"]
stats_command = ["docker", "stats", container_name, "--no-stream", f"--format='{fmt}'"]

def run_command(command):
    """run a command using subprocess
    
    Args:
        command (list): list of tokens representing shell command to run
    
    Returns:
        str: Cleaned output of command
    """
    try:
        return subprocess.check_output(command).decode().strip().strip("'")
    except:
        return False


def get_status():
    """collates the runtime metrics of the container with its healthcheck status and timestamp
    
    Returns:
        list: list of metrics
    """
    stats = run_command(stats_command)
    health_status = run_command(healthcheck_command)
    if not (health_status and stats):
        return False
    curr  = datetime.now()
    timestamp= int(curr.timestamp())
    time = curr.strftime("%d/%m/%Y %H:%M:%S")
    return [timestamp,time,health_status]+stats.split(delim)

def main():
    """driver code
    """
    if not os.path.exists(output_file):
        writeheaders=True
    with open(output_file,"a") as f:
        writer = csv.writer(f)
        if writeheaders:
            writer.writerow(headers)
            while True:
                status = get_status()
                if status:
                    writer.writerow(status)
                    f.flush()
                time.sleep(10)

if __name__ == '__main__':
    main()