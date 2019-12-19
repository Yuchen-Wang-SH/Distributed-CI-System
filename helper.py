import socket

def communicate(host, port, message):
    """
    Send a message to host:port and return its response
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(message)
        res = s.recv(1024)
        s.close()
        return res
    except socket.error as e:
        raise Exception('Something wrong with the socket communication. Error message: %s' % e.strerror)