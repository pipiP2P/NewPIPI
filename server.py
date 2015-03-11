import socket

def debug_print(data):
    print data

UDP_PORT = 50000
ADDRESSES = []
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', UDP_PORT))
debug_print("Succeed binding on port " + str(UDP_PORT) )
while True:
    data, addr = udp_socket.recvfrom(4096)
    print data
    if data == "Hello":
        if ADDRESSES:
            udp_socket.sendto(';'.join(ADDRESSES), (addr[0], UDP_PORT))
        else:
            udp_socket.sendto("None",(addr[0], UDP_PORT))
        if addr not in ADDRESSES:
            # Todo: Check how much people send to the client
            ADDRESSES.append(addr)
