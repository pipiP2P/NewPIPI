MESSAGE_LENGTHS = [2, 3, 4, 7]
FILE_REQUEST = '1'
FILE_RESPONSE = '2'
PART_REQUEST = '3'
PART_RESPONSE = '4'
COMMANDS_NUMS = [FILE_REQUEST, FILE_RESPONSE, PART_REQUEST, PART_RESPONSE]


def convert_message(message):
    message = message.split(';')

    if len(message) not in MESSAGE_LENGTHS:
        raise NameError("Protocol Error")

    command = message[0]

    if command not in COMMANDS_NUMS:
        raise NameError("Protocol Error")

    if len(message) == 2:
        if command != FILE_REQUEST:
            raise NameError("Protocol Error")
        return (message[0], message[1], 'None', 'None', 'None', 'None', 'None')

    if len(message) == 7:
        if command != FILE_RESPONSE:
            raise NameError("Protocol Error")
        return (message[0], message[1], message[2], message[3], message[4], message[5], message[6])

    if len(message) == 3:
        if command != PART_REQUEST:
            raise NameError("Protocol Error")
        return (message[0], message[1], message[2], message[3], message[4], message[5], message[6])

    if len(message) == 4:
        if command != PART_RESPONSE:
            raise NameError("Protocol Error")
        return message


def file_req_message(message):
    return (message[0], message[1], 'None', 'None', 'None', 'None', 'None')


def file_res_message(message):
    return (message[0], message[1], message[2], message[3], message[4], message[5], message[6])


