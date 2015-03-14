import socket


UDP_PORT = 50000
BUFFER = 4096
ADDRESSES = []
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def debug_print(data):
    print data


def new_connection(addr):
    if ADDRESSES:
        print 'Sending Those addresses: \n%s\nTo: %s' % ('\n'.join(ADDRESSES), addr)
        udp_socket.sendto(';'.join(ADDRESSES), (addr, UDP_PORT))
    else:
        print 'Sending None To: ', addr
        udp_socket.sendto("None", (addr, UDP_PORT))


if __name__ == '__main__':
    udp_socket.bind(('0.0.0.0', UDP_PORT))
    debug_print("Succeed binding on port " + str(UDP_PORT))
    while True:
        data, addr = udp_socket.recvfrom(BUFFER)
        addr = addr[0]
        debug_print('DATA RECEIVED: ' + data)
        if data == "Hello":
            new_connection(addr)

        if addr not in ADDRESSES:
            # Todo: Check how much people send to the client
            ADDRESSES.append(addr)
