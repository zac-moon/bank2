import socket
import threading
import datetime

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            data = data.decode('utf-8')
            

            if not data:
                print("Client disconnected")
                break
            else:
                datas = data.split('.')
                cmd = datas[0]

                if cmd == "login":
                    username = datas[1]
                    password = datas[2]
                    try:
                        with open(f'db/users/{username}') as file:
                            corpass = file.read().strip()
                        if corpass == password:
                            client_socket.send('Correct Details'.encode('utf-8'))
                        else:
                            client_socket.send('Incorrect Password'.encode('utf-8'))
                    except FileNotFoundError:
                        client_socket.send('Account Not Found'.encode('utf-8'))

                elif cmd == "balance":
                    username = datas[1]
                    try:
                        with open(f'db/balance/{username}') as file:
                            bal = file.read().strip()
                            client_socket.send(bal.encode('utf-8'))
                    except FileNotFoundError:
                        client_socket.send('Account Not Found'.encode('utf-8'))

                elif cmd == "transfer":
                    froms = datas[1]
                    amount = int(datas[2])
                    to = datas[3]

                    try:
                        with open(f'db/balance/{froms}') as file:
                            curbal = int(file.read().strip())
                            if curbal < amount:
                                client_socket.send('Insufficient Funds'.encode('utf-8'))
                            else:
                                curbal -= amount
                                with open(f'db/balance/{froms}', 'w') as file:
                                    file.write(str(curbal))

                        with open(f'db/balance/{to}') as file:
                            curbal = int(file.read().strip())
                            curbal += amount
                            with open(f'db/balance/{to}', 'w') as file:
                                file.write(str(curbal))

                        client_socket.send('Transfer of Funds Completed Successfully'.encode('utf-8'))

                    except FileNotFoundError:
                        client_socket.send('Account Not Found'.encode('utf-8'))

        except Exception as error:
            print(f"Error Occurred: {error}")
            break

    client_socket.close()

def main():
    host = "127.0.0.1"
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
