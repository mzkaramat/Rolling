# creating a web API to Store and View and Delete Time Stamp
# create a multiCastDNS using avahi and zeroconf
from __future__ import print_function # In python 2.7
from zeroconf import ServiceInfo, Zeroconf
from flask import Flask, request
import pickle
import datetime
from flask import jsonify

# import socket programming library
import socket
import socket
import sys
import requests
import json


url = "https://us-central1-alwaystuned2019.cloudfunctions.net/api/engines/by-id/efioerjhfg9qrufg2"

app = Flask(__name__)

# The timeStamp is stored in the pickle file
pickleFileName="data.pickle"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()
port="5000"
zeroconf = Zeroconf()

# configure and register the mDNS server to advertise packets
def registerService():
    info = ServiceInfo("_service._tcp.local.",
                   "mac._service._tcp.local.",
                   socket.inet_aton(ip), int(port), 0, 0,
                   {}, "ash-2.local.")
    zeroconf.register_service(info)
    print("motion Service Registered")

def saveData():
    #get data, append the timeStamp and save it at the end
    return(str(datetime.datetime.now()))


@app.route('/saveData', methods=['GET', 'POST'])
def onHttpRequestSave():
    #request.form['rawData']
    # Data Sample {'temperature': 'nan', 'humidity': 'nan'}
    resp = request.get_json()
    resp['EvennTime'] = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
    payload = json.dumps(resp)
    print(payload, file=sys.stderr)
    print(type(payload),file=sys.stderr)
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.11.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "0fa806d0-eee9-4960-8984-941eb1d8a340,0f174457-1072-4871-a853-2c2c8224f3f8",
        'Host': "us-central1-alwaystuned2019.cloudfunctions.net",
        'accept-encoding': "gzip, deflate",
        'content-length': "405",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }
    
    
    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text, file=sys.stderr)


    print(resp, file=sys.stderr)
    return saveData()

if __name__ == '__main__':
    registerService()
    #app.run(host= ip)
    app.run(host = ip)