import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            data = data.decode('utf-8')
            print(data)
            if not data:
                print("Client disconnected")
                break
            else:
                datas = data.split('.')
                cmd = datas[0]
                if cmd =="login":
                    username = datas[1]
                    password = datas[2]
                    try:
                        with open(f'db/users/{username}') as file:
                            corpass = file.read()
                        if corpass == password:
                            client_socket.send('Correct Details'.encode('utf-8'))
                        else:
                            client_socket.send('Incorrect Password'.encode('utf-8'))
                    except FileNotFoundError:
                        client_socket.send('Account Not Found'.encode('utf-8'))

        except:
            print("Error:")
            break
    client_socket.close()

def main():
    host = "192.168.1.71"
    port = 12346

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print("Server listening on {}:{}".format(host, port))

    while True:
        try:
            client_socket, client_address = server.accept()
            print("Accepted connection from:", client_address)
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
            break

    server.close()

if __name__ == "__main__":
    main()
