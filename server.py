from flask import Flask, request, abort
from process import process

app = Flask(__name__)


@app.route('/ajiranet/process', methods=['POST'])
def process_request():
    data = request.data.decode()
    response = process.process_request_data(data)
    print(response)
    if (response["code"]) == 400:
        return {"msg": response["message"]}, 400
    return "Hello world"


@app.route('/hello')
def hello_world():
    return "hello world"


if __name__ == '__main__':
    app.run()
