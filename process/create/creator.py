from process import connection_graph


def create_connection(data):
    print("CREATING CONNECTION ", data)

    code = None
    message = None

    try:
        source_node = data["source"]
        target_nodes = data["targets"]

        # If source node exists
        if connection_graph.get_node_by_name(source_node) is not None:
            for target_node in target_nodes:
                if source_node == target_node:
                    code = 400
                    message = "Cannot connect device to itself"
                    break
                elif connection_graph.get_node_by_name(target_node) is not None:
                    if connection_graph.edge_exists(source_node, target_node):
                        code = 400
                        message = "Devices are already connected"
                    else:
                        connection_graph.add_edge(source_node, target_node)
                        code = 200
                        message = "Successfully connected"
                else:
                    code = 400
                    message = "Node '" + target_node + "' not found"
        else:
            code = 400
            message = "Node '" + source_node + "' not found"
    except KeyError:
        print("source or target nodes not in input")
        code = 400
        message = "Invalid command syntax"
    return code, {"msg": message}


def create_device(data):
    possible_devices = ["COMPUTER", "REPEATER"]
    print("CREATING DEVICE ", data)
    code = None
    message = None
    try:
        node_type = data["type"]
        node_name = data["name"]
        if node_type not in possible_devices:
            print("NODE", node_type, "NOT SUPPORTED")
            code = 400
            message = "type '" + node_type + "' is not supported"
        elif connection_graph.add_node(type=node_type, name=node_name):
            print("NODE", node_type, node_name, "CREATED")
            code = 200
            message = "Successfully added " + node_name
        else:
            print("NODE ALREADY EXISTS")
            code = 400
            message = "Device '" + node_name + "' already exists"
    except KeyError:
        print("Type or Name not found")
        code = 400
        message = "Invalid command"
    return code, {"msg": message}
