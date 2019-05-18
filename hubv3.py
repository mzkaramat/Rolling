# creating a web API to Store and View and Delete Time Stamp
# create a multiCastDNS using avahi and zeroconf
from __future__ import print_function # In python 2.7
from zeroconf import ServiceInfo, Zeroconf
from flask import Flask, request
import pickle
import datetime
from flask import jsonify
from time import gmtime, strftime
# import socket programming library
import socket
import socket
import sys
import requests
import json
import random
import time
import sys

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
import pickle
# importing libaries ----
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import datetime

pkl_filename = "anom.pkl"  
# Load from file
with open(pkl_filename, 'rb') as file:  
    pickle_model = pickle.load(file)
# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=iothub-fgwq2.azure-devices.net;DeviceId=engine;SharedAccessKey=xTU/FCCaLwHAAUcP6QwPn5z13um8X0UY83MjluxcrkM="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.HTTP
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60

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

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

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
    resp['EventTime'] = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
    payload = json.dumps(resp)
    
    X_outliers = pd.DataFrame([{'x1':10,'x2':69.79}])
    y_pred_outliers = pickle_model.predict(X_outliers)
    
    output = 'Normal'
    if y_pred_outliers[0] == -1:
        output = "Anom"
    else:
        print("Nothing to worry about", file=sys.stderr)
    
    resp['notification_alert'] = output
    print(output ,file=sys.stderr)
    data_t = strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime())
    #payload = '{ "data": '+payload+', "deviceId": "engine", "time": "'+data_t+'" }'
    #payload = payload
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
    
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit", file=sys.stderr)

        message = IoTHubMessage(payload)

        # Add a custom application property to the message.
        # An IoT hub can filter on these properties without access to the message body.
        prop_map = message.properties()
        

        # Send the message.
        print( "Sending message: %s" % message.get_string() , file=sys.stderr)
        client.send_event_async(message, send_confirmation_callback, None)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error , file=sys.stderr)
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" , file=sys.stderr)

    
    print(resp, file=sys.stderr)
    return saveData()

if __name__ == '__main__':
    registerService()
    #app.run(host= ip)
    app.run(host = ip)

