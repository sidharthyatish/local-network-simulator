from process import connection_graph


def create_connection(data):
    print("CREATING CONNECTION ", data)
    print("connection created")


def create_device(data):
    possible_devices = ["COMPUTER", "REPEATER"]
    print("CREATING DEVICE ",data)
    code =None
    message =None
    try:
        node_type = data["type"]
        node_name = data["name"]
        if node_type not in possible_devices:
            print("NODE",node_type,"NOT SUPPORTED")
            code = 400
            message = "type '"+node_type+"' is not supported"
        elif connection_graph.add_node(type=node_type, name=node_name):
            print("NODE",node_type,node_name,"CREATED")
            code = 200
            message = "Successfully added "+node_name
        else:
            print("NODE ALREADY EXISTS")
            code = 400
            message = "Device '"+node_name+"' already exists"
    except KeyError:
        print("Type or Name not found")
        code = 400
        message =  "Invalid command"
    return code, {"msg" : message}
