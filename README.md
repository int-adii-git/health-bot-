# 🩺 Health Kit — AI Health & Wellness Chatbot

**Health Kit** is a simple, smart, and safe AI health chatbot built in Python using **Streamlit** and the **Google GenAI SDK** (`google-genai`).

Built step-by-step following the guide *"Build Your First AI Chatbot"* by Jay Dobariya, Health Kit provides friendly, easy-to-understand health education, wellness suggestions, nutrition tips, and symptom guidance with built-in medical safety disclaimers and multi-turn conversational memory.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+** (Python 3.12 recommended)
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 2. Activate the Virtual Environment
Open your terminal in the `health bot` directory:

- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\activate
  ```
- **Mac / Linux**:
  ```bash
  source .venv/bin/activate
  ```

*(If you ever need to recreate the virtual environment)*:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add Your Gemini API Key
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).
2. Open the `.env` file in the project folder.
3. Replace `paste-your-key-here` with your API key:
   ```env
   GEMINI_API_KEY="AIzaSy..."
   ```
*(Note: You can also enter or update your API key directly inside the Streamlit sidebar!)*

### 4. Verify API Connection (Optional First Step)
Run the verification script from Step 4 of the guide:
```powershell
python hello_gemini.py
```
If your key is valid, you'll see a response from Gemini!

### 5. Run the Chatbot
Launch the Streamlit web app:
```powershell
streamlit run app.py
```
Your default browser will automatically open at:
```
http://localhost:8501
```

---

## ✨ Features Included

- **💬 Conversational Memory**: Remembers previous questions and answers during your chat session (`st.session_state.messages`).
- **🛡️ Medical Safety & Rules**: Persona defined using Role, Task, Context, and Rules to provide concise, friendly guidance with appropriate disclaimers.
- **🥗 Daily Wellness & Nutrition Tips Toggle**: Sidebar toggle that appends actionable daily health habits to responses.
- **🗑️ Clear Chat**: Reset the conversation with one click in the sidebar.
- **🚨 Friendly Error Handling**: Catches invalid API keys (400/401/403) and rate limits (429) gracefully.

---

## 🌐 Deploy to the Internet (Streamlit Community Cloud)

Follow Part 2 of the guide to put Health Kit online for free:

1. Push your code to a GitHub repository:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit of Health Kit chatbot"
   git remote add origin https://github.com/YOUR-USERNAME/health-kit.git
   git push -u origin main
   ```
   *(Your `.env` file is protected by `.gitignore` and will not be uploaded).*

2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app** → **Deploy a public app from GitHub**.
4. Select your repository, branch (`main`), and set the main file path to `app.py`.
5. Under **Advanced settings** → **Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key"
   ```
6. Click **Deploy**. In ~2 minutes, your chatbot will be live at a public URL you can share with anyone!
