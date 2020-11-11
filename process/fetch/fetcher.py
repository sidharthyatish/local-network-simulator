from process import connection_graph
from urllib.parse import urlparse, parse_qs


def fetch_devices():
    response = {"devices": []}
    for node in connection_graph.graph.keys():
        device = dict()
        device['type'] = node.type
        device['name'] = node.name
        response["devices"].append(device)
    return 200, response


def fetch_route_information(data):
    code = None
    message = None
    print("FETCHING ROUTE ", data)
    parsed_url = urlparse(data)
    query_dict = parse_qs(parsed_url.query)

    try:
        f_node = query_dict["from"]
        t_node = query_dict["to"]
        from_node = connection_graph.get_node_by_name(f_node[0])
        to_node = connection_graph.get_node_by_name(t_node[0])
        if from_node is None:
            code = 400
            message = "Node '"+f_node[0]+"' not found"
        elif to_node is None:
            code = 400
            message = "Node '" + t_node[0] + "' not found"
        elif from_node.type == "REPEATER" or to_node.type == "REPEATER":
            code = 400
            message = "Route cannot be calculated with repeater"
        else:
            paths = connection_graph.get_path(source=from_node,dest=to_node)
            if paths[0] is not None:
                code = 200
                message = "Route is "+"->".join(paths)
            else:
                code = 404
                message = "Route not found"

    except KeyError:
        code = 400
        message = "Invalid Request"

    print(code,message)
    return code, {"msg": message}
