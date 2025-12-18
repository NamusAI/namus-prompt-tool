import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIG (MUST BE FIRST) ---
st.set_page_config(page_title="Omni-Prompt Architect", page_icon="🧬", layout="wide")

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp {background-color: #050505; color: #00ff41;}
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #111; color: #e0e0e0; border: 1px solid #333;
    }
    .stButton>button {
        background-color: #00ff41; color: black; font-weight: bold; border: none;
        padding: 15px; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. API SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")

# --- 4. SYSTEM CHECK (DEBUGGER) ---
# This sidebar will tell you EXACTLY which models are available to you
with st.sidebar:
    st.header("System Status")
    if api_key:
        genai.configure(api_key=api_key)
        try:
            st.success("API Key Detected")
            if st.button("Check Available Models"):
                st.write("Google allows you to use:")
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        st.code(m.name)
        except Exception as e:
            st.error(f"API Error: {e}")
    else:
        st.error("No API Key found in Secrets")

# --- 5. MAIN APP ---
st.title("🧬 OMNI-PROMPT ARCHITECT")
st.markdown("**House of Namus** | Universal Logic for Generative Video, Image & Avatar.")

col1, col2, col3 = st.columns(3)
with col1:
    category = st.selectbox("1. Category", ["Video Generation", "Image Generation", "Avatar/Script"])
with col2:
    target_model = st.selectbox("2. Target Model", ["OpenAI Sora", "Kling AI", "Runway Gen-3", "Midjourney v6", "Flux 1.1 Pro", "Synthesia"])
with col3:
    aspect_ratio = st.selectbox("3. Spec", ["16:9 (Cinematic)", "9:16 (Viral)", "1:1 (Square)"])

user_input = st.text_area("Concept Input:", height=100)

if st.button("INITIATE SEQUENCE"):
    if not api_key:
        st.error("API Key missing.")
    elif not user_input:
        st.warning("Input required.")
    else:
        genai.configure(api_key=api_key)
        
        # --- TRYING THE STANDARD MODEL NAME ---
        # If this fails, check the Sidebar to see what name you SHOULD use.
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            system_instruction = f"""
            Act as an expert prompt engineer for {target_model}.
            Rewrite this concept: "{user_input}"
            Context: {category}, {aspect_ratio}.
            Provide only the prompt.
            """
            
            with st.spinner("Processing..."):
                response = model.generate_content(system_instruction)
                st.code(response.text, language="markdown")
                
        except Exception as e:
            st.error(f"Model Error: {e}")
            st.info("Tip: Use the sidebar 'Check Available Models' button to see valid names.")
