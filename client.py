import socket
import select
import time
import threading
import File
from Functions import *
from Protocol import *

SERVER_IP = "192.168.0.105"
addr = SERVER_IP
ADDRESSES = []
OUR_FILES = []
PEERS_FILES = []
UDP_PORT = 50000
BUFFER_SIZE = 4096
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def initialize():
    global OUR_FILES
    OUR_FILES = get_all_files()


def print_our_files():
    for file_object in OUR_FILES:
        file_object.print_file_info()


def print_peers_files():
    for file_object in PEERS_FILES:
        file_object.print_file_info()


def UDP_listener():
    """
    This function starts a new thread that listens
    to incoming UDP packets
    """
    listen_thread = threading.Thread(target=UDP_listen)
    listen_thread.start()


def handle_data(data):
    """
    Receives the incoming data
    and does the appropriate action (send file, send list of connected peers etc...)
    """
    try:
        command_num, file_name, file_hash, file_parts_num, file_size, file_description, answer_type = convert_message(data)
    except NameError:
        debug_print("Data doesn't fit the protocol")


def new_connection(addr):
    debug_print(addr + "Connected")
    if ADDRESSES:
        client_socket.sendto(';'.join(ADDRESSES), (addr, UDP_PORT))
    else:
        client_socket.sendto("None", (addr, UDP_PORT))
    add_addresses(addr)


def send_files_list(addr):
    debug_print("{0} asked us for our files list!".format(addr))
    if addr not in ADDRESSES:
        ADDRESSES.append(addr)
    content = "FILES:"
    for file_object in OUR_FILES:
        content += file_object.to_string() + ';'
    content = content[:-1]  # Remove the last ;
    client_socket.sendto(content, (addr, UDP_PORT))


def get_files_list(data):
    list_of_files = data[6:].split(';')
    if len(list_of_files) > 0:
        for file_object in list_of_files:
            PEERS_FILES.append(File_Info(decrypt_file(file_object)))


def UDP_listen():
    """
    This function listens for incoming UDP packets
    It will be run a new thread
    """
    while True:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_socket.bind(("", UDP_PORT))
        data, addr = new_socket.recvfrom(BUFFER_SIZE)
        addr = addr[0]
        debug_print("Received this data " + data + " from " + addr)

        if data == "Hello":
            new_connection(addr)

        elif data == "show-files":
            send_files_list(addr)

        elif data.startswith("FILES:"):
            get_files_list(data)

        else:
            handle_data(data)


def print_addresses():
    print("Addresses:\n\t" + "\n\t".join(ADDRESSES))


def ask_for_files():
    for addr in ADDRESSES:
        client_socket.sendto("show-files", (addr, UDP_PORT))


def debug_print(data):
    print data


def add_addresses(data):
    if data != 'None':
        for address in data.split(';'):
            if address != socket.gethostbyname(socket.gethostname()) and address not in ADDRESSES:
                ADDRESSES.append(address)
        if ADDRESSES:
            print_addresses()
    else:
        debug_print("We didn't receive any addresses")


def connect_to_server():
    global ADDRESSES, addr
    connected = False
    new_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_listen_socket.bind(("", UDP_PORT))
    while not connected:
        client_socket.sendto("Hello", (addr, UDP_PORT))
        rlist = select.select([new_listen_socket], [], [], 5)
        if rlist[0]:
            # The server responded
            data, address = new_listen_socket.recvfrom(BUFFER_SIZE)
            address = address[0]
            if address == addr:
                debug_print("Connected to " + ("Main Server" if addr == SERVER_IP else addr))
                debug_print("We received " + data + " from " + ("Main server" if addr == SERVER_IP else addr))
                add_addresses(data)
                if addr not in ADDRESSES and addr != SERVER_IP:
                    ADDRESSES.append(addr)
                connected = True
        else:
            addr = raw_input("Could not connect to the IP " + addr + "\nPlease write another IP\n")
    new_listen_socket.close()


if __name__ == '__main__':
    initialize()
    connect_to_server()
    ask_for_files()
    UDP_listener()
