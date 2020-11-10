import process.create.device as dev
import process.create.connection as con
import process.fetch.devices as fet


def process_request_data(data):
    data_lines = data.splitlines()
    result = {"code": None, "message": None}

    command_line = data_lines[0].split(" ")
    print(command_line)
    command = command_line[0]
    if command == 'CREATE':
        print(data_lines)
        if len(data_lines) < 3:
            result["code"] = 400
            result["message"] = "Invalid command"
        sub_command = command_line[1]
        if sub_command == '/devices':
            dev.create_device()
        elif sub_command == '/connection':
            con.create_connection()
    elif command == 'FETCH':
        sub_command = command_line[1]
        if sub_command == '/devices':
            dev.create_device()
        elif sub_command == '/connection':
            con.create_connection()

    return result


if __name__ == '__main__':
    con.create_connection()
    dev.create_device()
    fet.fetch_devices()
