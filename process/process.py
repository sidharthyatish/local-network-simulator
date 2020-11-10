import process.create.device as dev
import process.create.connection as con
import process.fetch.devices as fet
if __name__ == '__main__':
    con.create_connection()
    dev.create_device()
    fet.fetch_devices()
