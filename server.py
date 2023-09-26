from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response

import pymongo
app = Flask(__name__)

CORS(app)


def connect():
    atlas_connection_string = "mongodb+srv://simar:1234@cluster0.4vk9j99.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(atlas_connection_string)
    db = client.mydatabase
    collection = db.chat_history
    return collection, client


@app.before_first_request
def create_chat_history_collection():
    collection, client = connect()
    client.close()


@app.route("/predict", methods=["POST"])
def predict():
    collection, client = connect()

    try:
        data = request.get_json(force=True)
        text = data.get("text")
        response = get_response(text)
        chat_history = collection.find_one() or {"session_history": []}
        session_history = chat_history.get("session_history", [])
        chat_entry = {"input": text, "output": response}
        session_history.append(chat_entry)
        collection.replace_one(
            {}, {"session_history": session_history}, upsert=True)
        message = {"answer": response}
        return jsonify(message)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        client.close()


if __name__ == "__main__":
    app.run(debug=True)
