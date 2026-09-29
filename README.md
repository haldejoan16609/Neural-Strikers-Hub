# ⚡ Neural Strikers — AI Kit & Content Hub

**Track:** Media, Content & Digital Experiences  
**Event:** Hack2skill AI Builder Cup 2026  
**Built With:** Streamlit, Vertex AI (Gemini 1.5 Pro & Imagen 3), Python, Docker, Google Cloud Run

---

## 📌 Project Overview
**Neural Strikers — AI Kit & Content Hub** is an AI-powered media creation suite built for esports teams, athletic brands, and digital creators. The platform leverages Google Cloud's Vertex AI to simultaneously generate high-fidelity 3D athletic kit concepts and full-fledged multi-channel marketing campaigns in real time.

---

## ✨ Key Features
- **🎨 3D Kit Concept Rendering:** Generates ultra-realistic 3D jersey concepts on mannequins using **Imagen 3 on Vertex AI**, applying custom textures, neon accents, and cybernetic patterns.
- **📖 Cinematic Kit Reveal Narrative:** Uses **Gemini 1.5 Pro** to write compelling design lore, dynamic reveal stories, and team origin ethos.
- **📱 Automated Social Media Campaigning:** Automatically constructs ready-to-publish captions with required event hashtags (`#PromptYourJersey`, `#AIBuilderCup`, `#Hack2Skill`, `#NeuralStrikers`).
- **💡 Demo Simulation Fallback Mode:** Allows reviewers to test and evaluate the UI/UX layout even prior to entering GCP service credentials.

---

## 🏗️ Architecture & Tech Stack

- **Frontend:** Streamlit (Custom Dark-Mode UI with Cyan/Gold Cybernetic Aesthetic)
- **AI Models (Backend):**
  - **Text & Campaign Generation:** `gemini-1.5-pro` via Vertex AI SDK
  - **Visual Asset Rendering:** `imagen-3.0-generate-001` via Vertex AI SDK
- **Deployment & Infrastructure:** Dockerized container deployed on **Google Cloud Run**

---

## 🚀 Local Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed along with the [Google Cloud SDK](https://cloud.google.com/sdk).

### 2. Clone Repository
```bash
git clone [https://github.com/haldejoan16609/Neural-Strikers-Hub.git](https://github.com/haldejoan16609/Neural-Strikers-Hub.git)
cd Neural-Strikers-Hub
