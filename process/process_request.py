from process.create import creator
from process.fetch import fetcher
import json


def input_validator(input_data):
    possible_commands = {"CREATE": ["/devices", "/connections"], "MODIFY": ["/strength"], "FETCH": ["/devices"]}

    response = {"command": None, "sub_command": None, "data": {}}
    data_lines = input_data.splitlines()
    '''
    data_lines must have 
    Line 0 -> Command (CREATE /devices)
    Line 1 -> header  (content-type : application/json)
    Lines in between -> spaces
    Line n-1 -> parameter for command ({"type" : "COMPUTER", "name": "A1"})
    '''
    len_data_line = len(data_lines)
    if len_data_line > 0:
        command_line = data_lines[0].split(" ")
        if len(command_line) > 1:
            command = command_line[0]
            if command not in possible_commands.keys():
                response["command"] = "INVALID"
            else:
                response["command"] = command
                sub_command = command_line[1]
                if command != "FETCH" and sub_command not in possible_commands[command]:
                    response["sub_command"] = "INVALID"
                else:
                    response["sub_command"] = sub_command
                    if command in ["CREATE", "MODIFY"]:
                        last_data_line = data_lines[len_data_line - 1].strip()
                        try:
                            command_data = json.loads(last_data_line)
                            if type(command_data) != dict:
                                command_data = "INVALID"
                        except ValueError:
                            command_data = "INVALID"
                        response["data"] = command_data

    else:
        response["command"] = "INVALID"

    return response


def process_request_data(data):
    data_lines = data.splitlines()
    result = {"code": None, "message": None}

    command_line = data_lines[0].split(" ")
    # print(command_line)
    command = command_line[0]
    if command == 'CREATE':
        # print(data_lines)
        if len(data_lines) < 3:
            result["code"] = 400
            result["message"] = "Invalid command"
        sub_command = command_line[1]
        if sub_command == '/devices':
            creator.create_device()
        elif sub_command == '/connection':
            creator.create_connection()
    elif command == 'FETCH':
        sub_command = command_line[1]
        if sub_command == '/devices':
            creator.create_device()
        elif sub_command == '/connection':
            creator.create_connection()

    return result


def process_req_data(input_data):
    validated_input = input_validator(input_data)
    result = {"code": None, "message": None}
    code = 404
    message = "Unknown error"
    print(validated_input)
    if validated_input["command"] == "INVALID" or validated_input["sub_command"] == "INVALID" or validated_input[
        "data"] == "INVALID":
        code = 400
        message = "Invalid command syntax"
    elif validated_input["command"] == "CREATE":
        if validated_input["sub_command"] == "/devices":
            code, message = creator.create_device(validated_input["data"])
        elif validated_input["sub_command"] == "/connections":
            creator.create_connection(validated_input["data"])
    elif validated_input["command"] == "FETCH":
        if validated_input["sub_command"] == "/devices":
            code, message = fetcher.fetch_devices()
        elif "info-routes" in validated_input["sub_command"]:
            fetcher.fetch_route_information(validated_input["sub_command"])
    result["code"] = code
    result["message"] = message
    return result


if __name__ == '__main__':
    data = 'FETCH /info-routes?from=A1&to=A1'

    process_req_data(data)
