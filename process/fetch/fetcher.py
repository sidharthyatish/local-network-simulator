from process import connection_graph
from urllib.parse import urlparse, parse_qs


def fetch_devices():
    """
    Gets all ndoes from graph containing
    :return: code, response containing list of devices. Empty list if no devices
    """
    response = {"devices": []}
    for node in connection_graph.graph.keys():
        device = dict()
        device['type'] = node.type
        device['name'] = node.name
        response["devices"].append(device)
    return 200, response


def fetch_route_information(data):
    """

    :param data: A url string like /info-routes?from=A1&to=A4
    :return: code, {"msg" : MESSAGE}

    Here the data will contain s string that itself is a URL. We need to parse it and get the query params
    This validation is done here and from graph (connection_graph) we get the path from source to destination
    """
    code = None
    message = None
    print("FETCHING ROUTE ", data)
    parsed_url = urlparse(data)
    query_dict = parse_qs(parsed_url.query)

    try:
        source = query_dict["from"]
        destination = query_dict["to"]
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
            message = "Route cannot be calculated with repeater"
        else:
            paths = connection_graph.get_path(source=from_node, dest=to_node)
            if paths[0] is not None:
                code = 200
                message = "Route is " + "->".join(paths)
            else:
                code = 404
                message = "Route not found"

    except KeyError:
        code = 400
        message = "Invalid Request"

    print(code, message)
    return code, {"msg": message}
