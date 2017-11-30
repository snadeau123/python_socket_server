#!/usr/bin/env python

import sys
import os
import time

from sys import platform

import socket
from thread import *

import logo
from ui import screenwrite
sw = screenwrite(ymin=13, ymax=23)

try:
    from msvcrt import getch  # try to import Windows version
except ImportError:
    def getch():   # define non-Windows version
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

bShouldExit = False
slideNumber = '0'
numberConnections = 0
clientList = []
btestmode = False
MaxSlideNumber = 2


# Client class to keep status of the connections
class Client(object):
    def __init__(self, connection, id):
        self.id = id
        self.conn = connection
        self.active = True

    def isActive(self):
        '''
        try:
            self.conn.send("ping")
        except socket.error as msg:
            self.active = False
        '''
        return self.active

    def close(self):
        self.conn.close()
        self.active = False

    def send(self, data):
        try:
            self.conn.send(data)
        except socket.error as msg:
            self.active = False



# helper class to check if value is a number
# returns a boolean
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# initialize the UI
def initui():
    sw.clearScreen()
    sw.printStatic(logo.title, 0, 0, 5)
    sw.printStatic('-' * 82, 0, 12)

    for i in range(13,24):
        sw.printStatic('|', 41, i)
        sw.printStatic('|', 82, i)

    sw.printStatic("q : Exit     t : Test Mode", 0, 11)

    sw.printStatic("current slide : ", 42, 13)
    sw.printStatic("set slide to : ", 42, 14)

    sw.printStatic("Active Connections : ", 42, 16, 1)


# initialize the server
def init_server():
    HOST = ''   # Symbolic name meaning all available interfaces
    PORT = 50007 # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sw.printnl('Socket created')

    # Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    sw.printnl('Socket bind complete',3)

    return s


# main function that calls the initialization of the server
# launches threads to listen to input keys, listen to for new clients and update/push the slide number
# also keep tracks of connections that are alive
def startserver():

    # build server  ui
    initui()

    sw.printnl('initializing server')
    s = init_server()

    # listen for key input
    start_new_thread(keylistener, (s,))
    start_new_thread(listen, (s, ))
    start_new_thread(slide_updater, tuple())

    # now stay awake until user quits
    while not bShouldExit:
        time.sleep(5)
        numberConnections = 0
        for client in clientList:
            if client.isActive():
                numberConnections += 1
        sw.printStatic('%d      '%numberConnections, 63, 16, 1)

    sw.printnl('shutdown complete', 5)


# check if slide number has changed
# push the new slide number to the clients
def slide_updater():

    global slideNumber
    global btestmode
    previousSlideNumber = 0

    while 1:
        if btestmode:
            time.sleep(2.5)
            slideNumber = str((int(slideNumber)+1) % MaxSlideNumber)

        time.sleep(0.1)
        if previousSlideNumber != slideNumber:
            for client in clientList:
                if client.isActive():
                    client.send('%s\n'%str(slideNumber))
            previousSlideNumber = slideNumber


# Listens to for connections
# create a new client object for each new connections and start a separate thread to handle messages from client
def listen(s):
    global numberConnections

    #Start listening on socket
    s.listen(10)
    sw.printnl('Socket now listening', 2)

    while 1:
        # wait to accept a connection - blocking call
        try:
            conn, addr = s.accept()
        except socket.error as msg:
            break

        sw.printnl('Connected with ' + addr[0] + ':' + str(addr[1]))

        # create a new client
        clientList.append(Client(conn, len(clientList)))

        start_new_thread(client_thread,(clientList[-1],))


# Listen to input keys from the console
# handles slide number input and 'q' for quit
def keylistener(s):

    global bShouldExit
    global slideNumber
    global btestmode

    inputNumber = ''
    while 1:
        keyinput = getch()
        if keyinput == 'q':
            for client in clientList:
                if client.isActive():
                    client.send('q')
                    client.close()

            #time.sleep(2)

            if platform == "linux" or platform == "linux2":
                s.shutdown(socket.SHUT_RDWR)

            s.close()
            sw.printnl('server closing connection', 4)
            bShouldExit = True
            break
        elif (keyinput == 't'):
            btestmode = not btestmode
            sw.printStatic("TEST MODE ACTIVE", 42, 18, 5)
        elif keyinput == '\r':
            if inputNumber != '':
                slideNumber = inputNumber
                sw.printStatic(slideNumber+'     ', 58, 13, 3)
                inputNumber = ''
                sw.printStatic('        ', 57, 14, 4)
        elif (keyinput == '\x08') or (keyinput == '\x7f'):  # handle backspace
            inputNumber = inputNumber[:-1]
            sw.printStatic(inputNumber+'     ', 57, 14, 4)
        else:
            if is_number(keyinput):
                inputNumber += keyinput
                sw.printStatic(inputNumber, 57, 14, 4)


# Function for handling connections. This will be used to create threads
def client_thread(client):
    global numberConnections
    global slideNumber

    # Sending message to connected client
    client.send('Welcome to the server\n') # send only takes string
    client.send('%s\n' % str(slideNumber))

    # infinite loop so that function do not terminate and thread do not end.
    while True:
        if(1):
            # Receiving from client
            data = client.conn.recv(1024)

            if not data:
                break
            if data.rstrip('\r\n') == 'q':
                break
            if data.rstrip('\r\n') == 'r':
                client.send('%s\n' % str(slideNumber))

    #came out of loop
    client.close()
    sw.printnl('connection closed')
    client.active = False


if __name__=='__main__':

    startserver()

    sw.printStatic('press Enter to Continue...', 0, 11, 5)
    raw_input("")

    sw.clearScreen()

