from process import connection_graph


def create_connection(data):
    print("CREATING CONNECTION ", data)
    print("connection created")


def create_device(data):
    possible_devices = ["COMPUTER", "REPEATER"]
    print("CREATING DEVICE ",data)
    try:
        node_type = data["type"]
        node_name = data["name"]
        if node_type not in possible_devices:
            print("NODE",node_type,"NOT SUPPORTED")
            return 400, "type '"+node_type+"' is not supported"
        elif connection_graph.add_node(type=node_type, name=node_name):
            print("NODE",node_type,node_name,"CREATED")
            return 200, "Successfully added "+node_name
        else:
            print("NODE ALREADY EXISTS")
            return 400, "Device '"+node_name+"' already exists"
    except KeyError:
        print("Type or Name not found")
        return 400, "Invalid command"
    # connection_graph.add_node()
