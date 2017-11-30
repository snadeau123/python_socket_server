import test_client
from thread import *
import time




def clientThread(client):
    client.listen()
    print "Client listening"


if __name__ == '__main__':
    clients = []

    for i in range(5):
        time.sleep(0.01)
        print "loading thread : %d"%i
        clients.append(test_client.Client())
        start_new_thread(clientThread, (clients[i],))

    text = raw_input("press any key to continue")

    for client in clients:
        client.s.send('q')
        client.s.close()

