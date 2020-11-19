from process import connection_graph
from urllib.parse import urlparse, parse_qs


def send_message(data):

    # Send message syntax SEND /info?from=A1&to=A3&msg="hello"
    code = None
    message = None
    print("FETCHING ROUTE ", data)
    parsed_url = urlparse(data)
    query_dict = parse_qs(parsed_url.query)

    try:
        source = query_dict["from"]
        destination = query_dict["to"]
        msg = query_dict["msg"][0]
        from_node = connection_graph.get_node_by_name(source[0])
        to_node = connection_graph.get_node_by_name(destination[0])
        if from_node is None:
            code = 400
            message = "Node '" + source[0] + "' not found"
        elif to_node is None:
            code = 400
            message = "Node '" + destination[0] + "' not found"
        elif from_node.type == "REPEATER" or to_node.type == "REPEATER":
            code = 400
            message = "Cannot send message to repeater"
        elif from_node.type == "BRIDGE" or to_node.type == "BRIDGE":
            code = 400
            message = "Source or destination cannot be a BRIDGE"
        else:
            paths = connection_graph.get_path(source=from_node, dest=to_node)
            if paths[0] is not None:
                for p in paths:
                    node_in_path = connection_graph.get_node_by_name(p)
                    print("NODE IN PATH ",node_in_path.name, node_in_path.type)
                    if node_in_path.type == "BRIDGE":
                        print("BRIDGE TYPE", node_in_path.sub_type)
                        if node_in_path.sub_type == "UPPER":
                            msg = msg.upper()
                            print("MESSAGE", msg)
                        elif node_in_path.sub_type == "LOWER":
                            msg = msg.lower()
                            print("MESSAGE", msg)

                print("FINAL MESSAGE",msg)
                code = 200
                message = "Message is " + msg
            else:
                code = 404
                message = "Route not found to send message"

    except KeyError:
        code = 400
        message = "Invalid Request"

    print(code, message)
    return code, {"msg": message}
