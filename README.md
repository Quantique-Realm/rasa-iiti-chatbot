# Rasa Chatbot
# IIT Indore Chatbot Backend 🤖 (Rasa Server)

This repository contains the **Rasa backend** for the IIT Indore Campus Chatbot. It handles all chatbot logic, NLU/NLP, dialogue management, and custom actions.

## 🚀 Features
- Built with **Rasa Open Source (v3.x)**
- REST API enabled for frontend integration
- Includes **custom actions server**
- Easily deployable on local or cloud servers

## 🛠️ Requirements
- Python 3.9.x (Recommended)
- Virtual Environment (venv)
- Pip

## 🖥️ Local Setup Instructions
1. **Clone the repository:**
```
git clone https://github.com/Quantique-Realm/rasa-iiti-chatbot.git
cd rasa-iiti-chatbot
```
Create and activate a Python virtual environment:

```
python3.9 -m venv rasa_env
source rasa_env/bin/activate
```
Upgrade pip and install dependencies:

```
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```
Train the Rasa Model:
```
rasa train
```
This will create a model inside the /models directory.

✅ Running the Servers
Run the Rasa Server (Port 5005):

```
rasa run --enable-api --cors "*" --port 5005
```
API will be live at:
http://localhost:5005

Main REST endpoint for frontend:
POST http://localhost:5005/webhooks/rest/webhook

Run the Action Server (Port 5055):
In a new terminal:
```
source rasa_env/bin/activate
rasa run actions --port 5055
```
✅ Frontend Integration
To connect the frontend React app to this backend, please visit the frontend repository:
https://github.com/Quantique-Realm/rasa_iiti_frontend
