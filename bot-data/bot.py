from flask import Flask, json, jsonify, request
import psutil
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
import operator
import collections
import time

from pprint import pprint

app = Flask(__name__)

def getData(): #get data from server
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boottime = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()

    sername = "<b><u> BackAdmin Server </u></b>"
    timedif = "Online for: %.1f Hours" % (((now - boottime).total_seconds()) / 3600)
    memtotal = "Total memory: %.2f GB " % (memory.total / 1000000000)
    memavail = "Available memory: %.2f GB" % (memory.available / 1000000000)
    memuseperc = "Used memory: " + str(memory.percent) + " %"
    diskused = "Disk used: " + str(disk.percent) + " %"

    pids = psutil.pids()
    pidsreply = ''
    procs = {}
    for pid in pids:
        p = psutil.Process(pid)
        try:
            pmem = p.memory_percent()
            if pmem > 0.5:
                if p.name() in procs:
                    procs[p.name()] += pmem
                else:
                    procs[p.name()] = pmem
        except:
            print("failed to get data")
    sortedprocs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
    for proc in sortedprocs:
        pidsreply += proc[0] + " " + ("%.2f" % proc[1]) + " %\n"

    data = {
        'server_name'      : sername,
        'uptime'           : timedif,
        'total_memory'     : memtotal,
        'used_memory'      : memuseperc,
        'available_memory' : memavail,
        'disk_used'        : diskused,
        'process'          : pidsreply,
    }

    return data

@app.route('/')
def index():
    #return "aaaa"
    return getData()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
