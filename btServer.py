import bluetooth

port = 1

client_address = "(insert the other pi's MAC address)"

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

server_socket.bind("", port)
server_socket.listen(1)

print("Waiting for connection...")
client_socket, client_info = server_socket.accept()
print(f"Accepted connection from {client_info}")

