import bluetooth


def listen():
    server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = bluetooth.PORT_ANY
    server_sock.bind(("", port))
    server_sock.listen(1)
    print("listening on port %d" % port)

    bluetooth.advertise_service(server_sock, "FooBar Service", service_classes=[bluetooth.SERIAL_PORT_CLASS], profiles=[bluetooth.SERIAL_PORT_PROFILE])

    client_sock,address = server_sock.accept()
    print("Accepted connection from ",address)

    data = client_sock.recv(1024)
    print("received [%s]" % data)

    client_sock.close()
    server_sock.close()


while 1:
    command = input(" -> ")

    if command == 'listen':
        listen()
