import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

# Load environment variables from .env
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Health Kit - AI Health Assistant",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Header Section ---
st.title("🩺 Health Kit")
st.caption("Your personal AI health & wellness assistant — friendly, safe, and practical advice.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Health Kit Settings")

    # API Key retrieval (.env / Streamlit secrets / Manual entry fallback)
    env_api_key = os.getenv("GEMINI_API_KEY", "")
    if env_api_key == "paste-your-key-here":
        env_api_key = ""

    # Allow user to input or override API key in sidebar if not set in .env
    user_api_key = st.text_input(
        "Gemini API Key",
        value=env_api_key,
        type="password",
        placeholder="Enter your Gemini API key...",
        help="Get a free API key at https://aistudio.google.com/apikey",
    )

    # Model selection (using gemini-3.5-flash-lite from the PDF guide)
    model_choice = st.selectbox(
        "AI Model",
        options=["gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-flash-latest"],
        index=0,
        help="Fast and capable models from Google Gemini",
    )

    # Feature Toggle: Wellness & Nutrition Mode (matches Quiz mode from guide)
    wellness_mode = st.toggle(
        "🥗 Wellness & Nutrition Tips",
        value=True,
        help="Appends practical lifestyle or nutrition tips after each answer.",
    )

    st.divider()

    # Clear Chat Button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        ### ⚠️ Medical Disclaimer
        **Health Kit** provides general wellness and educational information only. 
        It is **not** a substitute for professional medical advice, diagnosis, or treatment. 
        For any urgent health symptoms or emergencies, please consult a qualified physician or emergency room immediately.
        """
    )

# --- Validate API Key ---
api_key = user_api_key.strip() if user_api_key else ""
if not api_key:
    st.error("🔑 **Gemini API Key is missing!**")
    st.info(
        """
        To use Health Kit:
        1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).
        2. Paste it in the `.env` file (`GEMINI_API_KEY=your_key_here`) or type it in the sidebar field on the left.
        """
    )
    st.stop()

# Initialize Gemini Client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize Gemini client: {e}")
    st.stop()

# --- System Instruction (Health Kit Persona) ---
# Follows Role / Task / Context / Rules as outlined in Prompt 3 of the PDF
SYSTEM_PROMPT = """
Role: You are "Health Kit", a warm, empathetic, and knowledgeable AI health and wellness assistant.
Task: Help users understand general health, fitness, nutrition, hydration, sleep hygiene, and healthy daily habits.
Context: You are talking to users seeking accessible, everyday guidance to live a healthier lifestyle.
Rules:
1. Explain concepts simply and clearly in under 150-200 words.
2. Safety first: Always remind users to consult a doctor or healthcare professional for clinical diagnoses, prescriptions, or severe symptoms.
3. If unsure or if a question requires clinical diagnosis, say: "I'm not sure. Please consult a qualified doctor or healthcare professional."
4. If a question is off-topic (unrelated to health, fitness, wellness, or nutrition), politely redirect the user back to health topics.
5. End your response with one encouraging follow-up check question or a healthy habit check-in.
""".strip()

if wellness_mode:
    SYSTEM_PROMPT += "\nSpecial Mode: After providing the explanation, append a short section titled '💡 Daily Health Kit Tips' with 2 simple, actionable wellness or nutrition tips."

# --- Initialize Chat History (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Conversation History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input & Response Generation ---
user_input = st.chat_input("Ask Health Kit about symptoms, fitness, nutrition, or wellness...")

if user_input:
    # 1. Display User Message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Build Multi-Turn History for Gemini
    contents = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=m["content"])],
            )
        )

    # 3. Call Gemini with System Prompt & Full History
    with st.spinner("🩺 Health Kit is thinking..."):
        try:
            response = client.models.generate_content(
                model=model_choice,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                ),
            )
            bot_reply = response.text

            # Display Bot Message
            with st.chat_message("assistant"):
                st.markdown(bot_reply)

            # Store in session state
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        except errors.APIError as e:
            # Polish and error handling from Prompt 4 in the guide
            error_code = getattr(e, "code", None)
            if error_code in [400, 401, 403]:
                st.error("❌ **Invalid Gemini API Key**: Please check that your key is active and correctly copied from Google AI Studio.")
            elif error_code == 429:
                st.error("⏳ **Rate Limit Exceeded (429)**: The free Gemini API quota was reached. Please wait a minute or create a new project in Google AI Studio for a fresh quota.")
            else:
                st.error(f"⚠️ **Gemini API Error ({error_code})**: {e.message}")
        except Exception as e:
            st.error(f"⚠️ **Unexpected Error**: {str(e)}")
