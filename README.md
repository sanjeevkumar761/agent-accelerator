# Agent Acclerator based on Autogen with FastApi backend and React frontend

It is based upon autogenwebdemo and func_ui repositories for Autogen Agents using FastApi as backend and a frontend client using React.  

For SAP BASIS copilot, configure Azure Center for SAP Solutions for your SAP system and prepare a service principal to access Azure Resource Graph.  

1. **FastApi Backend**: A FastApi application running autogen.
2. **Webapp**: React webapp using websocket to communicate with FastApi.

## Running demo

1. **Clone this repo**
```
git clone https://github.com/sanjeevkumar761/agent-accelerator.git
cd agent-accelerator
```
2. **Configure backend**

Configure python deps
```
cd backend  
python -m venv agent_accelerator  
[For Windows based system] source agent_accelerator/Scripts/activate  
pip install -r ./requirements.txt   
```
Add your Openai key to .env inside src folder
```
cd backend/src (copy .env-sample as .env, then edit .env and add your keys; also copy OAI_CONFIG_LIST-sample as OAI_CONFIG_LIST and add your keys)  
```

Start backend server inside src folder
```
python main.py
```
You should see

```
INFO:     Started server process [85614]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

2. **Configure frontend**

Open a new terminal and go to the react-frontend folder (you need to have nodejs installed and npm >= v14 )
```
cd agent-accelerator/react-frontend
npm install
npm run dev
```
Open you browser on http://localhost:5173/ or the port shown 

Send the following messages:
```
-> Hi
<- Hello! How can I assist you today?

```


