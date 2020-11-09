from flask import Flask, request

app = Flask(__name__)


@app.route('/ajiranet/process', methods=['POST'])
def process_request():
    data = request.data.decode()
    datas = data.splitlines()
    for d in datas:
        print(d.strip())
    return "Hello world"


if __name__ == '__main__':
    app.run()
