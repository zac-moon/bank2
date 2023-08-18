import socket
import tools

host = socket.gethostname()
ip = socket.gethostbyname(host)
location = tools.location()

print("Host:", host)
print("IP:", ip)
print("Loction:",location)