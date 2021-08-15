from flask import Flask
import subprocess
from flask import request,jsonify
import itertools
import pandas as pd
from io import StringIO
from pretty_html_table import build_table


app = Flask(__name__)

headers = ['timestamp', 'time', 'health', 'CPUPerc', 'MemPerc', 'MemUsage', 'BlockIO', 'NetIO', 'Container', 'ID', 'Name', 'PIDs']

file_loc = "/logs/docker_status.log"


def read_file():
    try:
        with open(file_loc,"r") as f:
            data = f.read()
    except:
        data = "file not found"
    return data

def fetch_metrics(start,end):
    try:
        with open(file_loc,"r") as f:
            for i,line in enumerate(f):
                if i>0:
                    try:
                        cells = line.split(",")
                        ts = int(cells[0])
                    except:
                        continue
                    if start<=ts<=end:
                        yield cells
                    if ts>end:
                        break
            
    except Exception as e:
        print(f"Error {format(e)}")
        raise e




def tail(n=100):
    cmd = ['tail', '-n', f'{n}', file_loc]
    try:
        lines =  subprocess.check_output(cmd).decode().strip("\n")
        return lines
    except:
        return False


@app.route("/")
def root():
    data = tail()
    if data:
        if data.startswith('timestamp'):
            df = pd.read_csv(StringIO(data),sep=',')
        else:
            df = pd.read_csv(StringIO(data),sep=',',names=headers)
        html_table = build_table(df, 'blue_light')
        return(f"<html>{html_table}</html>")
    else:
        return "file not found"


@app.route("/api/metrics/period",methods=["GET"])
def api():
    data = request.get_json(silent=True)
    start = data.get('start')
    end = data.get('end')
    if start and end:
        try:
            rows = list(fetch_metrics(int(start),int(end)))
        except:
            return "Not Ready",503
        return jsonify([dict(zip(headers,row)) for row in rows])
    else:
        return "Bad Request",400

@app.route("/healthcheck")
def healthcheck():
    return 'ok',200

if __name__ == "__main__":
    app.run(host='0.0.0.0')