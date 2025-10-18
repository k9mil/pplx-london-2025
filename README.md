# space

We found purchasing furniture & home accesories tedious; which is why we built space with the help of Perplexity. The space product allows us to speak via natural language to an ElevenLabs agent which guides us through the tedious process of buying furniture & showcasing how it would look like in our room.

In our personal experience we found that:

- It takes a lot of mental effort & time to find what we actually want
- It's hard to envision what the furniture would look like in our personal room

Which is why we built space. Traditional image generation tools can generate images of a given space and modify the product, but the products it generates don't exist in the real world. We solved this problem.

![space Product](https://github.com/user-attachments/assets/813acdc2-2c01-4ce4-b969-53fe1a209e93)

## 🎬 Demo
https://github.com/user-attachments/assets/19f0a34c-018f-42ee-a929-1c33e59e9dde

## 🎯 Project Overview

_space_ streamlines the furtniture purchasing experience, by:

- Gathering images from the users' room of choice
- Conduct intelligent consultations with users through natural language
- Extracting requirements from the user of their preferences
- Doing a wide scan of the net with the help of Perplexity to scan for URLs of our products
- Extracting data of the products via the use of Jina AI

## 💻 Tech Stack

- [Perplexity](https://www.perplexity.ai/) – searching the web
- [Cursor](https://cursor.com/) – for rapid prototyping
- [Python](https://www.python.org/) – backend language
- [FastAPI](https://fastapi.tiangolo.com/) – backend framework
- [TypeScript](https://www.typescriptlang.org/) – frontend language
- [React](https://react.dev/) – frontend framework
- [JinaAI](https://jina.ai/) – product extraction
- [shadcn/ui](https://ui.shadcn.com/) – the standard for components

## 🚀 Running the Project

### Quick Start (Frontend Only)

The backend is deployed on Cloud Run, so you only need to run the frontend locally:

```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

Visit `http://localhost:5173` to use the app.

### Full Local Development (Optional)

Only needed if you're developing backend features.

**Environment Variables:**

Create a `.env` file in the `backend` directory:

```bash
# Required
PERPLEXITY_API_KEY=your-perplexity-key

# Optional (for Google Cloud features)
GCS_BUCKET_NAME=your-bucket-name
GCP_PROJECT_ID=your-project-id
GCS_CREDENTIALS_PATH=path/to/service-account-key.json
```

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
# Runs on http://localhost:8000
```

## Team

- <a href="https://www.linkedin.com/in/kamilzak00/">Kamil Zak</a>
- <a href="https://www.linkedin.com/in/fabian-salge/">Fabian Salge</a>
- <a href="https://uk.linkedin.com/in/emma-rattray-bb026b143">Emma Rattray</a>
- <a href="https://fr.linkedin.com/in/maxime-brun-insa">Maxime Brun</a>