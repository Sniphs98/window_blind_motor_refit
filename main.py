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

IN1 = Pin(26,Pin.OUT)
IN2 = Pin(25,Pin.OUT)
IN3 = Pin(33,Pin.OUT)
IN4 = Pin(32,Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence_up = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
sequence_down = [[1,0,0,0],[1,0,0,1],[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0]]

app = Microdot()
server_address = ""      
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

@app.get('/state/getRollo')
def getWindowOpenProcent(request):
    return Response(body=str(windowOpenProcent), headers={"Content-Type": "text/plain"})

# @app.route('/api/switchOn')
# def rollo_up(request):
#     print("rollo up")
#     for i in range(26):
#         one_rotation_up()
#     led_off()
#     print("done")
#     return 'done'
# 
# @app.route('/api/switchOn50')
# def rollo_up_50(request):
#     print("rollo up")
#     for i in range(13):
#         one_rotation_up()
#     led_off()
#     print("rollo up down")
#     return 'done'
# 
# @app.route('/api/switchOff')
# def rollo_up(request):
#     print("rollo down")
#     for i in range(26):
#         one_rotation_down()
#     led_off()
#     print("rollo down done")
#     return 'done'
# 
@app.route('/api/switchOff50')
def rollo_up_50(request):
    print("rollo down")
    for i in range(13):
        one_rotation_down()
    led_off()
    print("rollo down done")
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
    print("up")
    print(procent)
    stepsToDo = (windowMaxSteps / 100) * procent
    stepsToDo = round(stepsToDo)
    print(stepsToDo)
    for i in range(stepsToDo):
        for step in sequence_up:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

def rollo_down_procent(procent):
    print("down")
    print(procent)
    stepsToDo = (windowMaxSteps / 100) * procent
    stepsToDo = round(stepsToDo)
    print(stepsToDo)
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

def connect():
    print("Try to connecting")
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(WIFI_SSID,WIFI_PASS)
    else:
        server_address = sta_if.ifconfig()[0]
    time.sleep(1)
    print("Server:", server_address)

def connect_static_ip():
    try:
        print("Verbindung wird versucht herzustellen...")
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            sta_if.active(True)
            sta_if.ifconfig((server_static_ip, '255.255.255.0', '192.168.178.1', '192.168.178.1'))
            sta_if.connect(WIFI_SSID, WIFI_PASS)
            
        while not sta_if.isconnected():
            time.sleep(1)
            print("Verbindung erfolgreich hergestellt. IP-Adresse:", sta_if.ifconfig()[0])
        else:
            print("Bereits verbunden. IP-Adresse:", sta_if.ifconfig()[0])
    
    except Exception as e:
        print("Fehler bei der Verbindung:", e)
        file = open ("logging.txt", "w")	
        file.write("WLAN Exception:", e)
        file.close()    
        sys.exit(1)

def start_server():
    print("Starting server!")
    try:
        app.run(port=80)
        app.allowed_origins("*")
    except:
        print("Server stoped")
        app.shutdown()

connect()
start_server()