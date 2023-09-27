# Ai Powered Chatbot (Kyro) - Backend

Postman API documentation Link - https://documenter.getpostman.com/view/30053279/2s9YJZ3QB8

## Description

I have successfully implemented the backend of the chatbot. This involved developing a deep learning model using Natural Language Processing (NLP) techniques in Python. I integrated the model with Flask, creating endpoints to provide responses based on the trained model. Additionally, I incorporated MongoDB to ensure data persistence, allowing for the storage of chat history between users and the chatbot. PyTorch was my framework of choice for building and training the neural networks used in this development. This combination of technologies and components forms the foundation of the chatbot's backend.

## Architecture
![Untitled-2023-09-27-1803](https://github.com/mdsimar1901/faq-chatbot-backend/assets/66200713/cceabfd7-4520-40a8-bb3f-82f51706a13e)

## Table of Contents
- [Data Workflow](#backend-workflow)
- [Natural Language Processing (NLP)](#natural-language-processing-nlp)
- [Neural Network](#neural-network)
- [Flask Integration](#flask-integration)
- [Data Persistence](#data-persistence)
- [How to Run Locally](#how-to-run-locally)
- [Deployment](#deployment)


## Data Workflow

The backend of this chatbot follows a specific workflow:

- intents.json file containing tags,patterns and responses is used as the dataset for the model.
- nltk_utils is used to stem,tokenize and create bag_of_words basically following the nlp preprocessing pipline
- model is created using torch.nn which is a feed forward Neural Network.
- in the train module, intent.json is destructure and dataset and dataLoader are used to train neural networks.
- The responses are reciprocated in the chat module.
<br/>

![workflow](https://github.com/mdsimar1901/faq-chatbot-backend/assets/66200713/2898f4cb-805d-403d-aacf-42c1f54eee00)

## Natural Language Processing (NLP)
- Our NLP preprocessing Pipeline looks like

![nlp_pipeline](https://github.com/mdsimar1901/faq-chatbot-backend/assets/66200713/6aa58fac-a672-4a93-be56-97acd598da4a)

## Neural Network
- Feed Forward Neural Network

![ff](https://github.com/mdsimar1901/faq-chatbot-backend/assets/66200713/9c8b7a47-2875-4f38-9aa6-22d997b43be5)

```
self.l1 = nn.Linear(input_size, hidden_size)
self.l2 = nn.Linear(hidden_size, hidden_size)
self.l3 = nn.Linear(hidden_size, num_classes)
```
```
out = self.l1(x)
out = self.relu(out)
out = self.l2(out)
out = self.relu(out)
out = self.l3(out)
```

## Flask Integration
- Create a flask App
- Imported the chat respone and creating a REST API
```
- POST Request in /predict endpoint.
```
```
{ "text":"User Input"}
```
- Payload as above is sent to generate response from model

```
@app.route("/predict", methods=["POST"])
def predict():
  data = request.get_json(force=True)
  text = data.get("text")
  response = get_response(text)
  message = {"answer": response}
  return jsonify(message)
```

Postman API documentation Link - https://documenter.getpostman.com/view/30053279/2s9YJZ3QB8

## Data Persistence
- Have used MongoDB to keep maintain track of chat history between user and chatbot
- MongoDB model
```
def connect():
    atlas_connection_string = "mongodb+srv://simar:1234@cluster0.4vk9j99.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(atlas_connection_string)
    db = client.mydatabase
    collection = db.chat_history
    return collection, client
```
```
chat_history = collection.find_one() or {"session_history": []}
session_history = chat_history.get("session_history", [])
chat_entry = {"input": text, "output": response}
session_history.append(chat_entry)
collection.replace_one({}, {"session_history": session_history}, upsert=True)
```
- View of chat history stored as Objects in MongoDB

![data-storage](https://github.com/mdsimar1901/faq-chatbot-backend/assets/66200713/1031c1ca-307c-40b3-958d-bf864f6978ca)

## How to run locally

Clone repo and create a virtual environment

```
$ git clone https://github.com/mdsimar1901/faq-chatbot-backend.git
$ cd faq-chatbot-backend
$ python3 -m venv venv
$ . venv/bin/activate
```

Install dependencies

```
$ (venv) pip install Flask torch torchvision nltk
```

Install nltk package

```
$ (venv) python
>>> import nltk
>>> nltk.download('punkt')
```
Run

```
$ (venv) python train.py
$ (venv) python chat.py
```

# Deployment 
- have deployed the flask application in Google Cloud Platform.
- Deploying Flask in Google Cloud Platform
- Lets assume the app is running good in localhost
```
if __name__ == "__main__":
    app.run()
```
- Create app.yml file
```
runtime: python39
entrypoint: gunicorn -b :$PORT main:app

handlers:
- url: /.*
  script: auto
```
- Create requirments.txt
```
pip freeze > requirements.txt
pip install gunicorn
```
- Deploy the app using the command
```
gcloud app deploy
```

![Screenshot 2023-09-28 010605](https://github.com/mdsimar1901/faq-chatbot-backend/assets/66200713/3d3059c8-4902-4982-9d45-9db3261c9354)
