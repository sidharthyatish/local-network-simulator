from process import connection_graph


def modify_strength(sub_command, data):
    code = None
    message = None
    print("MODIFY STRENGTH", sub_command, data)

    split_commands = sub_command.split('/')
    print("NODE", split_commands[2])
    if len(split_commands) < 4 or split_commands[1] != "devices" or split_commands[3] != "strength":
        code = 400
        message = "Invalid command syntax"
    elif connection_graph.get_node_by_name(split_commands[2]) is not None:
        node = connection_graph.get_node_by_name(split_commands[2])
        print("NODE",split_commands[2])
        try:
            new_strength = data["value"]
            if type(new_strength) != int:
                code = 400
                message = "value should be an integer"
            elif node.type == "REPEATER":
                code = 400
                message = "Cannot set strength for a repeater"
            else:
                node.strength = new_strength
                code = 200
                message = "Successfully defined strength"
        except KeyError:
            code = 400
            message = "Invalid command syntax"
    else:
        code = 400
        message = "Device not found"

    return code, {"msg": message}
