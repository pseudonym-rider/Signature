from flask import Flask, request, jsonify
import gps

app = Flask(__name__)

@app.route('/post-gps', methods=['POST'])
def post_gps():
    req = request.get_json()
    gps.save_gps(req["gps"], req["time"])
    return jsonify({"ok":"ok"})

@app.route('/get-gps', methods=['POST'])
def get_gps():
    response = gps.get_gps()
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")