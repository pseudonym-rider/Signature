import socket 
from flask import Flask, jsonify, request
from issuer import Issuer

app = Flask(__name__)
issuer = Issuer()

@app.route('/request/gpk', methods=['POST'])
def requestGpk():
    req = request.get_json()
    response = issuer.requestGpk(req['group-type'])
    return jsonify(response)

@app.route('/request/valid-token', methods=['POST'])
def requestValidateToken():
    req = request.get_json()
    response = issuer.requestValidateToken(req['token'])
    return jsonify(response)

@app.route('/request/gml-id', methods=['POST'])
def requestGmlId():
    req = request.get_json()
    response = issuer.requestGmlId(req['token'], req['sign'])
    return jsonify(response)

if __name__ == "__main__":
    # 특정 포트로 열기 ##########################################
    app.run()
