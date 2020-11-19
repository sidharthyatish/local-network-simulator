from process.create import creator
from process.fetch import fetcher
from process.modify import modifier
from process.send import sender
import json


def input_validator(input_data):
    """
    :param input_data: input data as text
    :return: {"command" : MAIN_COMMAND, "sub_command" : SUB_COMMAND, "data" ; {DATA_AS_DICT}}

    data_lines must have
    Line 0 -> Command (CREATE /devices)
    Line 1 -> header  (content-type : application/json)
    Lines in between -> spaces
    Line n-1 -> parameter for command ({"type" : "COMPUTER", "name": "A1"})

    Depending on the type of command and sub command, we need to parse the data to be processed by that command
    Here we only validate commands and their structure, for each command, there can be further validation to enure that
    the data given for the command has all required information. Did that in each of the respective process module
    """

    possible_commands = {"CREATE": ["/devices", "/connections"], "MODIFY": ["/devices"], "FETCH": ["/devices"],
                         "ADD": ["BRIDGE"], "SEND":["/info"]}

    response = {"command": None, "sub_command": None, "data": {}}
    data_lines = input_data.splitlines()
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
                if command == "CREATE" and sub_command not in possible_commands[command]:
                    response["sub_command"] = "INVALID"
                elif command == "ADD" and sub_command not in possible_commands[command]:
                    response["sub_command"] = "INVALID"
                else:
                    response["sub_command"] = sub_command
                    command_data = {}
                    if command in ["CREATE", "MODIFY"]:
                        last_data_line = data_lines[len_data_line - 1].strip()
                        try:
                            command_data = json.loads(last_data_line)
                            if type(command_data) != dict:
                                command_data = "INVALID"
                        except ValueError:
                            command_data = "INVALID"

                    elif command == "ADD":
                        try:
                            bridge_name = command_line[2]
                            bridge_type = command_line[3]
                            command_data = {"b_name": bridge_name, "b_type": bridge_type}
                        except IndexError:
                            command_data = "INVALID"
                response["data"] = command_data

    else:
        response["command"] = "INVALID"

    return response


def process_request_data(input_data):
    """
    :param input_data: Input data as raw text :return: Return code and message for the given input ex. {"code" : 200,
    "message" : {"msg" : "Successfully connected"}}

        Here we make a high level validation of the commands (syntax check)
        Then we call the respective module with its data, depending on the command and sub commands
    """
    validated_input = input_validator(input_data)
    result = {"code": None, "message": None}
    code = 404
    message = "Unknown error"
    print(validated_input)

    # In high level validation, we can determine if the overall syntax is valid or not
    # Else we get the respective sub commands and delegate the request to the respective modules
    if validated_input["command"] == "INVALID" or validated_input["sub_command"] == "INVALID" or validated_input[
        "data"] == "INVALID":
        code = 400
        message = {"msg": "Invalid command syntax"}
    elif validated_input["command"] == "CREATE":
        if validated_input["sub_command"] == "/devices":
            code, message = creator.create_device(validated_input["data"])
        elif validated_input["sub_command"] == "/connections":
            code, message = creator.create_connection(validated_input["data"])
    elif validated_input["command"] == "FETCH":
        if validated_input["sub_command"] == "/devices":
            code, message = fetcher.fetch_devices()
        elif "info-routes" in validated_input["sub_command"]:
            code, message = fetcher.fetch_route_information(validated_input["sub_command"])
    elif validated_input["command"] == "SEND":
        if "info" in validated_input["sub_command"]:
            code, message = sender.send_message(validated_input["sub_command"])
    elif validated_input["command"] == "MODIFY":
        code, message = modifier.modify_strength(validated_input["sub_command"], validated_input["data"])
    elif validated_input["command"] == "ADD":
        code, message = creator.add_bridge(validated_input["data"])
    result["code"] = code
    result["message"] = message
    return result


if __name__ == '__main__':
    data = '''SEND /info?from=A1&to=A3&msg="Hello"'''

    print(process_request_data(data))
