from process import connection_graph


def modify_strength(sub_command, data):
    """

    :param sub_command: sub command has the info on which node to modify the strength ex. devices/A1/strength
    :param data: data has the value of the new strength ex. {"value" : 10}
    :return: code and {msg : MESSAGE}

    Here we have further validation to check if the sub command is valid. We ensure all the params are
    appropriate and make strength specific validations and finally update the strength
    """
    code = None
    message = None
    print("MODIFY STRENGTH", sub_command, data)

    # subcommand : /devices/A1/strength has to be split based on /
    split_commands = sub_command.split('/')
    print("NODE", split_commands[2])
    if len(split_commands) < 4 or split_commands[1] != "devices" or split_commands[3] != "strength":
        code = 400
        message = "Invalid command syntax"
    # ensure that the node exists
    elif connection_graph.get_node_by_name(split_commands[2]) is not None:
        node = connection_graph.get_node_by_name(split_commands[2])
        print("NODE", split_commands[2])
        try:
            new_strength = data["value"]
            if type(new_strength) != int:
                code = 400
                message = "value should be an integer"
            elif node.type == "REPEATER":
                code = 400
                message = "Cannot set strength for a repeater"
            else:
                # If all conditions are met, set the new strength to the node
                node.strength = new_strength
                code = 200
                message = "Successfully defined strength"
        except KeyError:
            code = 400
            message = "Invalid command syntax"
    else:
        code = 404
        message = "Device not found"

    return code, {"msg": message}
