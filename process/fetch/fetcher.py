from process import connection_graph


def fetch_devices():
    response = {"devices": []}
    for node in connection_graph.graph.keys():
        device = dict()
        device['type']=node.type
        device['name']=node.name
        response["devices"].append(device)
    return 200,response


def fetch_route_information(data):
    print("FETCHING ROUTE ", data)
    print("Route information fetched")
