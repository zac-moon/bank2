import tkinter as tk
import socket
from tkinter import ttk

root = tk.Tk()
root.title('ZBANK LINK - LOGIN')
root.geometry('800x600')

host = "192.168.1.71"
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

def login():
    username = usernameEntry.get()
    password = passwordEntry.get()
    print(f'{username}\n{password}')
    client_socket.send(f'login.{username}.{password}'.encode('utf-8'))
    conf =client_socket.recv(1024)
    conf = conf.decode('utf-8')
    print('conf')

mainTitle = tk.Label(root,text='ZBANK LINK - LOGIN',font=('Arial',60))
usernameLabel = tk.Label(root, text='Username :')
usernameEntry = tk.Entry(root)
passwordLabel = tk.Label(root, text='Password :')
passwordEntry = tk.Entry(root, show="*")
loginButton = tk.Button(root, text='Login',command=login)

mainTitle.pack()
usernameLabel.pack()
usernameEntry.pack()
passwordLabel.pack()
passwordEntry.pack()
loginButton.pack()


root.mainloop()