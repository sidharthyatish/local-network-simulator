from flask import Flask, request, abort
from process import process_request as proc

app = Flask(__name__)


@app.route('/ajiranet/process', methods=['POST'])
def process_request():
    data = request.data.decode()
    # response = process_request.process_request_data(data)
    res = proc.process_request_data(data)

    return res["message"],res["code"]


if __name__ == '__main__':
    app.run(port=5000)
