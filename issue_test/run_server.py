from flask import Flask, jsonify, request
from server import Server

app = Flask(__name__)
server = Server()

@app.route('/request/token', methods=['POST'])
def requestToken():
    req = request.get_json()
    response = server.requestToken(req['id'], req['pw'])
    return jsonify(response)

@app.route('/request/add-member', methods=['POST'])
def requestAddGml():
    req = request.get_json()
    response = server.requestAddGml(req["uid"], req["token"], req["sign"])
    return jsonify(response)

if __name__ == "__main__":
    # 특정 포트로 열기 ##########################################
    app.run(host='0.0.0.0', port='80')
