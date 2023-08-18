import tkinter as tk
import socket

root = tk.Tk()
root.title('ZBANK LINK - LOGIN')
root.geometry('800x600')

host = "192.168.1.71"
port = 12346

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

confLabel = tk.Label(root, text="", fg='black') 

def main(username,password):
    usernameEntry.delete(0,tk.END)
    passwordEntry.delete(0, tk.END)
    balanceLabel = tk.Label(root, text='')

    def getBalance():
        client_socket.send(f'balance.{username}'.encode('utf-8'))
        balas = client_socket.recv(1024)
        balas = balas.decode('utf-8')
        balanceLabel.config(text=f'£{balas}')
        print(balas)

    client = tk.Toplevel(root)
    client.title(f'ZBANK LINK - {username}')
    client.geometry('799x599')

    balanceLabel.pack()
    getBalance()


def login():
    username = usernameEntry.get()
    password = passwordEntry.get()
    print(f'{username}\n{password}')
    client_socket.send(f'login.{username}.{password}'.encode('utf-8'))
    conf = client_socket.recv(1024)
    conf = conf.decode('utf-8')
    print(conf)
    if conf == "Correct Details":
        confLabel.config(text="Correct Details", fg='green')
        main(username, password)
    elif conf == "Incorrect Password":
        confLabel.config(text="Incorrect Password", fg='red')  
    elif conf == "Account Not Found":
        confLabel.config(text='Account Not Found', fg='red')  
    else:
        confLabel.config(text="Sorry, we couldn't log you in. We don't know why.", fg='red')  

mainTitle = tk.Label(root, text='ZBANK LINK - LOGIN', font=('Arial', 40))  
usernameLabel = tk.Label(root, text='Username:')
usernameEntry = tk.Entry(root)
passwordLabel = tk.Label(root, text='Password:')
passwordEntry = tk.Entry(root, show="*")
loginButton = tk.Button(root, text='Login', command=login)

mainTitle.pack()
usernameLabel.pack()
usernameEntry.pack()
passwordLabel.pack()
passwordEntry.pack()
loginButton.pack()
confLabel.pack()

root.mainloop()
