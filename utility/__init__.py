import socket


def get_local_ip_address():
    ip_address = socket.gethostbyname(socket.gethostname())
    return ip_address
