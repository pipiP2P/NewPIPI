import socket

def debug_print(data):
    print data

UDP_PORT = 60000
ADDRESSES = []
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', UDP_PORT))
debug_print("Succeed binding on port " + str(UDP_PORT))
while True:
    data, addr = udp_socket.recvfrom(4096)
    print 'DATA: ', data
    if data == "Hello":
        if ADDRESSES:
            print 'Sending ADDRESSES To: ', addr
            udp_socket.sendto(';'.join(ADDRESSES), addr)
        else:
            print 'Sending None To: ', addr
            udp_socket.sendto("None", addr)
        if addr not in ADDRESSES:
            # Todo: Check how much people send to the client
            ADDRESSES.append(addr[0])
