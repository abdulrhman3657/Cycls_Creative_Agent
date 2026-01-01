# Creative Agent

**Creative Agent** is a web-based AI tool that helps non-technical marketers generate **ready-to-publish Arabic marketing creative** with a Saudi tone.

Built using **Cycls**, the Distribution SDK for AI Agents.


## What It Does

- Turns rough or incomplete briefs into high-quality Arabic marketing copy
- Writes like a senior creative strategist, not a chatbot

## Target Users

- Marketing teams  
- Creative strategists  
- Brand managers  

## Tech Stack

- **Cycls**: agent runtime, UI, and deployment
- **FastAPI**: web server (via Cycls)
- **OpenAI API**
- **Docker**: containerized execution (handled by Cycls)

## Requirements

- Docker (installed and running)
- An OpenAI API key

## Deploying

```bash
pip install cycls
python main.py
