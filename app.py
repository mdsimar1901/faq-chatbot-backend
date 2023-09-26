from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response

app = Flask(__name__)

CORS(app)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    text = data.get("text")
    response = get_response(text)
    message = {"answer": response}

    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
