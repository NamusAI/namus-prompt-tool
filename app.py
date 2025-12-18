import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="Omni-Prompt Architect", page_icon="🧬", layout="wide")

# --- STYLING (House of Namus Tech-Noir) ---
st.markdown("""
<style>
    .stApp {background-color: #050505; color: #00ff41;}
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #111; color: #e0e0e0; border: 1px solid #333;
    }
    .stButton>button {
        background-color: #00ff41; color: black; font-weight: bold; border: none;
        padding: 15px; text-transform: uppercase; letter-spacing: 2px;
        width: 100%; transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #00ff41;
    }
    h1 {font-family: 'Courier New', monospace; color: white; letter-spacing: -2px;}
    .footer {position: fixed; bottom: 10px; width: 100%; text-align: center; color: #444; font-size: 10px;}
</style>
""", unsafe_allow_html=True)

# --- API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY")

# --- UI HEADER ---
st.title("🧬 OMNI-PROMPT ARCHITECT")
st.markdown("**House of Namus** | Universal Logic for Generative Video, Image & Avatar.")

# --- CONTROLS ---
col1, col2, col3 = st.columns(3)

with col1:
    category = st.selectbox("1. Category", ["Video Generation", "Image Generation", "Avatar/Script"])

with col2:
    if category == "Video Generation":
        target_model = st.selectbox("2. Target Model", [
            "OpenAI Sora", "Kling AI", "Runway Gen-3", "Luma Dream Machine", 
            "Google Veo", "Hailuo (MiniMax)", "Pika Labs", "Ray (Ray-2)"
        ])
    elif category == "Image Generation":
        target_model = st.selectbox("2. Target Model", [
            "Nano Banana (Google)", "Midjourney v6", "Adobe Firefly 3", 
            "Flux 1.1 Pro", "SeaArt / Seedream", "Stable Diffusion 3"
        ])
    else:
        target_model = st.selectbox("2. Target Model", ["Synthesia", "HeyGen"])

with col3:
    if category == "Avatar/Script":
        aspect_ratio = st.selectbox("3. Tone", ["Professional", "Casual/Viral", "Dramatic", "Educational"])
    else:
        aspect_ratio = st.selectbox("3. Ratio", ["16:9 (Cinematic)", "9:16 (Viral/Reels)", "1:1 (Square)", "2.35:1 (Anamorphic)"])

user_input = st.text_area("Concept Input:", height=120, placeholder="e.g., A cyberpunk samurai walking in rain...")

# --- LOGIC ENGINE ---
if st.button("INITIATE SEQUENCE"):
    if not api_key:
        st.error("SYSTEM ERROR: API Key missing in Settings.")
    elif not user_input:
        st.warning("INPUT REQUIRED.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # --- THE MASTER SYSTEM PROMPT ---
        system_instruction = f"""
        ROLE: Expert Prompt Engineer for Generative AI.
        TARGET MODEL: {target_model}
        CATEGORY: {category}
        PARAMETER: {aspect_ratio}
        USER CONCEPT: "{user_input}"
        
        INSTRUCTIONS PER MODEL:
        
        [VIDEO MODELS - SORA, VEO, KLING, HAILUO, RUNWAY]
        - Structure: [Subject + Action] + [Environment] + [Camera Movement] + [Lighting/Atmosphere] + [Technical Specs].
        - FOR SORA/VEO: Emphasize "temporal consistency", "physics compliance", and "photorealism".
        - FOR KLING/HAILUO: Use keywords "Motion strength: High", "Slow motion", "4k resolution".
        - FOR RUNWAY: Use camera terms: "Truck left", "Zoom in", "Rack focus".
        - FOR LUMA: Focus on "Loopable" or "Keyframe" logic if applicable.
        
        [IMAGE MODELS - NANO BANANA, FLUX, FIREFLY]
        - FOR NANO BANANA: Focus on high-fidelity text rendering and sharp details.
        - FOR FIREFLY: "Commercial stock photography", "perfect lighting", "clean composition".
        - FOR FLUX: "Texture heavy", "natural skin", "cinematic blur".
        
        [AVATAR MODELS - SYNTHESIA, HEYGEN]
        - DO NOT generate an image prompt. Generate a **SCRIPT**.
        - Include [GESTURE] tags in brackets. Example: "Welcome [NOD], today we discuss..."
        - Tone: {aspect_ratio}.
        
        OUTPUT FORMAT:
        Provide ONLY the final prompt/script text. No intro/outro.
        """
        
        with st.spinner("Compiling Neural Instructions..."):
            try:
                response = model.generate_content(system_instruction)
                st.subheader(":: OUTPUT DATA ::")
                st.code(response.text, language="markdown")
                st.success(f"Optimized for {target_model}")
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown('<div class="footer">Engineered by House of Namus</div>', unsafe_allow_html=True)
