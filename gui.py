import tkinter as tk
import socket

root = tk.Tk()
root.title('ZBANK LINK - LOGIN')
root.geometry('800x600')

host = "127.0.0.1"
port = 12346

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

confLabel = tk.Label(root, text="", fg='black') 

def main(username, password):
    usernameEntry.delete(0, tk.END)
    passwordEntry.delete(0, tk.END)

    client = tk.Toplevel(root)
    client.title(f'ZBANK LINK - {username}')
    client.geometry('790x590')

    def logOut():
        client.destroy()
        confLabel.config(text='',fg='black')

    def transfer():
        trans = tk.Toplevel(client)
        trans.title('Transfer Menu')
        trans.geometry('')

        detLabel = tk.Label(trans,text='',fg='black')

        def trTransfer():
            to = toEntry.get()
            amount = amountEntry.get()
            client_socket.send(f'transfer.{username}.{amount}.{to}'.encode('utf-8'))

        toLabel = tk.Label(trans,text="Enter Username of Account to Transfer Too:")
        toEntry = tk.Entry(trans)
        amountLabel = tk.Label(trans,text="Enter Amount to Transfer :")
        amountEntry = tk.Entry(trans)
        transBtn = tk.Button(trans,text='Transfer Funds',command=trTransfer)

        toLabel.pack()
        toEntry.pack()
        amountLabel.pack()
        amountEntry.pack()
        transBtn.pack()
        detLabel.pack()

    balanceLabel = tk.Label(client, text='', font=('Arial', 90))
    transferButton = tk.Button(client,text='Transfer',command=transfer,width=8,height=6)
    logoutButton = tk.Button(client, text='Log Out',command=logOut,width=8,height=6)

    def getBalance(ty):
        if ty == "fir":
            client_socket.send(f'balance.{username}'.encode('utf-8'))
        else:
            client_socket.send(f'balance.{username}.upd'.encode('utf-8'))
        balas = client_socket.recv(1024)
        balas = balas.decode('utf-8')
        balanceLabel.config(text=f'£{balas}')
        client.after(200, getBalance('upd'))

    balanceLabel.pack()
    transferButton.pack()
    logoutButton.pack()
    getBalance('fir')


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
