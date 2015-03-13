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
FILES = []
UDP_PORT = 50000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def UDP_listener():
    """
    This function starts a new thread that listens
    to incoming UDP packets
    """
    listen_thread = threading.Thread(target=UDP_listen())
    listen_thread.start()
    debug_print("Started the thread")


def handle_data():
    """
    Receives the incoming data
    and does the appropriate action (send file, send list of connected peers etc...)
    """
    return


def UDP_listen():
    """
    This function listens for incoming UDP packets
    It will be run a new thread
    """
    while True:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_socket.bind(("", 50000))
        data, addr = new_socket.recvfrom(4096)
        debug_print("Received this data " + data + " from " + addr[0])
        addr = addr[0]
        command_num, file_name, file_hash, file_parts_num, file_size, file_description, answer_type = convert_message(data)
        if data == "Hello":
            debug_print(addr + "Connected")
            client_socket.sendto(';'.join(ADDRESSES), (addr, UDP_PORT))
            add_addresses(addr)

        if data == "show-files":
            debug_print("{0} asked us for our files list!".format(addr))
            if addr not in ADDRESSES:
                ADDRESSES.append(addr)
            my_files = Functions.get_all_files()
            content = "FILES:"
            for file_object in my_files:
                content += file_object.to_string() + ';'
            client_socket.sendto(content, (addr, UDP_PORT))

        if data.startswith("FILES:"):
            list_of_files = data[6:].split(';')
            for file_object in list_of_files:
                #  This response is list of all files that the peer has
                file_name, file_hash, file_size, file_description = decrypt_file(file_object)
                FILES.append([file_name, file_hash, file_size, file_description])
                if int(command_num) == 1:
                    None


def print_addresses():
    print("Addresses:\n\t" + "\t".join(ADDRESSES))


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
    client_socket.sendto("Hello", (SERVER_IP, UDP_PORT))
    new_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_listen_socket.bind(("", UDP_PORT))
    rlist = select.select([new_listen_socket], [], [], 5)
    if rlist[0]:
        # The server responded
        data, addr = new_listen_socket.recvfrom(4096)
        debug_print("Connected to the main server")
        debug_print("We received " + data + " from server")
        add_addresses(data)

    else:
        while not ADDRESSES:
            # TODO: Check if the IP is correct / not ours
            addr = raw_input("Could not connect to the IP " + addr + "\nplease input other IP\n")
            client_socket.sendto("Hello", (addr, UDP_PORT))
            rlist = select.select([new_listen_socket], [], [], 5)
            if rlist[0]:
                if addr != SERVER_IP:
                    ADDRESSES.append(addr)  # That user is online
                data, addr = new_listen_socket.recvfrom(4096)
                debug_print("Connected to this address: " + addr[0])
                debug_print("Received the following data:" + data)
                add_addresses(data)
    new_listen_socket.close()


if __name__ == '__main__':
    connect_to_server()
    ask_for_files()
    UDP_listener()
