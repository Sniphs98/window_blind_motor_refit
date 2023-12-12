from logger import *
from configurator import *
from network import WLAN
from secret import WIFI_SSID, WIFI_PASS
from machine import Pin, Timer
from microdot import Microdot, Response, send_file, redirect
from machine import Pin
from time import sleep
import uasyncio as asyncio
import time
import network
import sys
import os

IN1 = Pin(26,Pin.OUT)
IN2 = Pin(25,Pin.OUT)
IN3 = Pin(33,Pin.OUT)
IN4 = Pin(32,Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence_up = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
sequence_down = [[1,0,0,0],[1,0,0,1],[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0]]

app = Microdot()
logger = Logger()
configurator = Configurator(logger)
server_address = ""
server_static_ip = '192.168.178.107'
windowMaxSteps = 13520
windowOpenProcent = 0
       
def one_rotation_up():
    for i in range(520):
        for step in sequence_up:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

def one_rotation_down():
    for i in range(520):
        for step in sequence_down:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

def led_off():
    sleep(0.1)
    pins[0].value(0)
    pins[1].value(0)
    pins[2].value(0)
    pins[3].value(0)
    sleep(0.1)

@app.route('/static/css/index.css')
def send_css(request):
    return send_file("static/css/index.css")

@app.route('/static/js/index.js')
def send_css(request):
    return send_file("static/js/index.js")

@app.route('/')
def page(request):
    return send_file("static/html/index.html")

@app.route('/logs')
def get_logs(request):
    return send_file("logging.txt")

@app.get('/state/getRollo')
def getWindowOpenProcent(request):
    return Response(body=str(windowOpenProcent), headers={"Content-Type": "text/plain"})

# @app.route('/api/switchOn')
# def rollo_up(request):
#     logger.log("rollo up")
#     for i in range(26):
#         one_rotation_up()
#     led_off()
#     logger.log("done")
#     return 'done'
# 
# @app.route('/api/switchOn50')
# def rollo_up_50(request):
#     logger.log("rollo up")
#     for i in range(13):
#         one_rotation_up()
#     led_off()
#     logger.log("rollo up down")
#     return 'done'
# 
# @app.route('/api/switchOff')
# def rollo_up(request):
#     logger.log("rollo down")
#     for i in range(26):
#         one_rotation_down()
#     led_off()
#     logger.log("rollo down done")
#     return 'done'
# 
@app.route('/api/switchOff50')
def rollo_up_50(request):
    logger.log("rollo down")
    for i in range(13):
        one_rotation_down()
    led_off()
    logger.log("rollo down done")
    return 'done'

@app.route('/api/preset/<int:preset>')
def rollo_up(request, preset):
    by_procent(None, preset)
    led_off()
    return 'done'

@app.route('/api/changeValue/procent/<int:procent>')
def change_procent_value_to(request, procent):
    global windowOpenProcent
    windowOpenProcent = procent
    return "done"

@app.route('/api/setProcent/<int:procent>')
def by_procent(request, procent):
    if(procent > 100):
        procent = 100
    if(procent < 0):
        procent = 0
    runProcent = 0
    global windowOpenProcent
    if(procent < windowOpenProcent):
        runProcent = procent - windowOpenProcent
        runProcent = runProcent * (-1)
        rollo_down_procent(runProcent)
        windowOpenProcent = procent
    if (procent > windowOpenProcent):
        runProcent = procent - windowOpenProcent
        rollo_up_procent(runProcent)
        windowOpenProcent = procent
    led_off()
    return redirect('/')



def rollo_up_procent(procent):
    logger.log("up")
    logger.log(procent)
    stepsToDo = (windowMaxSteps / 100) * procent
    stepsToDo = round(stepsToDo)
    logger.log(stepsToDo)
    for i in range(stepsToDo):
        for step in sequence_up:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

def rollo_down_procent(procent):
    logger.log("down")
    logger.log(procent)
    stepsToDo = (windowMaxSteps / 100) * procent
    stepsToDo = round(stepsToDo)
    logger.log(stepsToDo)
    for i in range(stepsToDo):
        for step in sequence_down:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

@app.route('/api/motorOff')
def test(request):
    led_off()
    return "motorOff"

@app.route('/api/serverOff')
def shut_down_server(request):
    request.app.shutdown()
    return 'The server is shutting down...'

@app.route('/api/test/<int:value>')
def test(request, value):
    for i in range(value):
        one_rotation_down()
    led_off()
    return 'done'


@app.route('/test/print')
def test_print(request):
    logger.log("test")
    return 'done'


# def connect():
#     time.sleep(1)
#     logger.log("Try to connecting")
#     wlan = network.WLAN(network.STA_IF)
#     if not wlan.isconnected():
#         wlan.active(True)
#         wlan.connect(WIFI_SSID,WIFI_PASS)
#     else:
#         server_address = wlan.ifconfig()[0]
#     time.sleep(1)
#     logger.log("Server:", server_address)
#     return wlan.ifconfig()[0]
    
# def connect_static_ip():
#     try:
#         logger.log("Attempting to establish connection...")
#         wlan = network.WLAN(network.STA_IF)
#         if not wlan.isconnected():
#             wlan.active(True)
#             wlan.ifconfig((server_static_ip, '255.255.255.0', '192.168.178.1', '192.168.178.1'))
#             wlan.connect(WIFI_SSID, WIFI_PASS)
#         while not wlan.isconnected():
#             time.sleep(1)
#             logger.log("Connection successfully established. IP address:" + wlan.ifconfig()[0])
#         else:
#             logger.log("Already connected. IP address:" + wlan.ifconfig()[0])
# 
#     except Exception as e:
#         logger.log("WLAN Exception:" + str(e))
#         sys.exit(1)

def connect_to_wifi(SSID_and_PASS):
    try:
        ssid, password = SSID_and_PASS
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        timeout = 20  # Timeout in seconds
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

        if wlan.isconnected():
            logger.log("Connected to WLAN:" + str(ssid))
            logger.log("With IP address:" + wlan.ifconfig()[0])
            return True
        else:
            logger.log("Connection to WLAN failed.")
            return False

    except Exception as e:
        logger.log("Error in WLAN connection:" + str(e))
        return False


def numer_input(consol_out):
    logger.log(consol_out)
    while True:
        user_intput = input()
        if user_intput.isdigit():
            return int(user_intput)
        else:
            logger.log("Only input numbers!")

def get_wlan_credentials():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    scan_results = wlan.scan()
    logger.log("Found Wi-Fi Networks:")
    number = 0
    for result in scan_results:
        number = number + 1
        ssid = result[0].decode("utf-8")
        signal_strength = result[3]
        logger.log(f"{number}| {ssid}, Signal Strength: {signal_strength} dB")
    SSID_number = numer_input("Choose a WIFI number: ")
    SSID = scan_results[SSID_number - 1][0].decode("utf-8")
    PASS = input(f"Enter WLAN password for {SSID}: ")
    return {SSID,PASS}
    

def create_setup_file():
    logger.log("First setup")
    with open(config_file, "w") as file:
        file.write("Hier sind einige Standardkonfigurationsdaten.")
    
def read_setup_file():
    logger.log("read_setup_file")

def start_server():
    logger.log("Starting server!")
    try:
        app.run(port=80)
        app.allowed_origins("*")
    except:
        logger.log("Server stoped")
        app.shutdown()
      
      
dir_iterator = os.ilistdir("./")
setup_config_exists = any(item[0] == "setup_config" and item[1] == 0 for item in dir_iterator)

if not setup_config_exists:
    SSID_and_PASS = get_wlan_credentials()
    if connect_to_wifi(SSID_and_PASS):
        configurator.create_file()
    else:
        logger.log("Pls Unluck the EPS and try agine")
        while True:
            time.sleep(1)
    # create_setup_file()
else:
    read_setup_file()

    # connect_static_ip()
start_server()
       

            


    
    



