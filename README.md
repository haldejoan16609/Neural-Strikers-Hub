# ⚡ Neural Strikers — AI Kit & Content Hub
### Hack2skill AI Builder Cup 2026 | Track: Media, Content & Digital Experiences

An end-to-end generative AI web application that produces 3D photorealistic athletic kits using **Imagen 3 on Vertex AI** and complete brand reveal narratives, lore, and high-impact social media campaigns using **Gemini 1.5 Pro on Vertex AI**.

---

## 🌟 Key Features

- **Cybernetic Dark Mode UI**: Modern Streamlit frontend styled with neon cyan and gold athletic accents.
- **Imagen 3 Visuals Engine**: Generates 3D studio product renders of jerseys with customizable fabric textures and themes.
- **Gemini 1.5 Pro Story & Social Studio**: Crafts dynamic press releases, team origin stories, and multi-platform social captions with official hashtags:
  - `#PromptYourJersey`
  - `#AIBuilderCup`
  - `#Hack2Skill`
- **Side-by-Side Presentation**: Direct visual and narrative comparison with one-click PNG downloads and copyable campaign text.
- **Built-in Demo Simulation Mode**: Allows instant testing of UI/UX workflows even before configuring GCP credentials.

---

## 🚀 Quickstart & Setup

### 1. Prerequisites
- Python 3.10+ installed
- Google Cloud Platform (GCP) account with Vertex AI API enabled

### 2. Clone / Open Directory
```bash
cd "Neural Strikers Documents"
```

### 3. Create and Activate Virtual Environment (Recommended)
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Authenticate with Google Cloud
Set up Application Default Credentials (ADC) for Vertex AI access:
```bash
gcloud auth application-default login
gcloud config set project YOUR_GCP_PROJECT_ID
```

*(Ensure the Vertex AI API is enabled on your project)*:
```bash
gcloud services enable aiplatform.googleapis.com
```

### 6. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🐳 Docker & Containerization

### Build with Docker:
From the project root:
```bash
docker build -f docker/Dockerfile -t neural-strikers-hub .
```

### Run with Docker:
```bash
docker run -p 8080:8080 neural-strikers-hub
```

### Or using Docker Compose:
```bash
docker compose up --build
```

### Deploy to Google Cloud Run:
```bash
gcloud run deploy neural-strikers-hub \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📂 Project Structure
```
.
├── app.py                  # Main Streamlit application with Vertex AI backend
├── requirements.txt        # Project dependencies (streamlit, google-cloud-aiplatform, Pillow)
├── docker/
│   └── Dockerfile          # Container configuration for Cloud Run / Docker
├── docker-compose.yml      # Docker Compose setup referencing docker/Dockerfile
├── .dockerignore           # Build exclusions
└── README.md               # Setup, execution, and architectural guide
```
