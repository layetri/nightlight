import sys
import bluetooth


def client(host, port):
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    s.connect((host, port))

    while True:
        message = raw_input('Send:')
        if not message: return
        s.send(message)
        data = s.recv(1024)
        print('Received: ' + data)

    s.close()


client(sys.argv[1], port=100)
