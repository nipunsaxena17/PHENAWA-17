import streamlit as st
import numpy as np

# Safe import to prevent immediate crashes if libraries are missing
try:
    import cv2
    import mediapipe as mp
    import math
    AI_READY = True
except ImportError:
    AI_READY = False

# ==========================================
# 1. LUXURIOUS UI CONFIGURATION
# ==========================================
st.set_page_config(page_title="PHENAWA", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Premium Ivory Background */
    .stApp { background-color: #FFFFF0; }
    
    /* Elegant Typography */
    h1, h2, h3, p, span, div { 
        color: #0A0A0A !important; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 400;
    }
    
    h1 { font-weight: 700; letter-spacing: -1px; text-transform: uppercase; border-bottom: 2px solid #000; padding-bottom: 10px;}
    h3 { font-weight: 600; text-transform: uppercase; font-size: 14px; letter-spacing: 2px; color: #555 !important;}
    
    /* Minimalist Buttons */
    .stButton>button { 
        width: 100%; 
        background-color: #0A0A0A; 
        color: #FFFFF0 !important; 
        border-radius: 0px; /* Sharp, modern edges */
        border: none;
        padding: 15px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #333333; color: white !important; }
    
    /* Clean Cards */
    .metric-box {
        border: 1px solid #E0E0E0;
        padding: 20px;
        text-align: center;
        background-color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# 2. CORE AI LOGIC (Clean & Simple)
# ==========================================
def analyze_body(image_bytes):
    """Processes the image and returns body type and advice."""
    if not AI_READY:
        return "System Error", ["Please install mediapipe and opencv-python-headless"]
        
    # Initialize MediaPipe
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
    
    # Convert image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Scan
    results = pose.process(img_rgb)
    if not results.pose_landmarks:
        return None, None
        
    landmarks = results.pose_landmarks.landmark
    
    # Calculate simple distances (Shoulders vs Hips)
    l_sh, r_sh = landmarks[11], landmarks[12]
    l_hip, r_hip = landmarks[23], landmarks[24]
    
    shoulder_w = math.sqrt((l_sh.x - r_sh.x)**2 + (l_sh.y - r_sh.y)**2)
    hip_w = math.sqrt((l_hip.x - r_hip.x)**2 + (l_hip.y - r_hip.y)**2)
    
    ratio = shoulder_w / (hip_w if hip_w > 0 else 1)
    
    # Minimalist Logic
    if ratio > 1.2:
        return "Inverted Triangle", ["Wear V-necks.", "Slim-fit shirts.", "Avoid shoulder pads."]
    elif ratio < 0.95:
        return "Rectangle / Slim", ["Wear structured jackets.", "Horizontal stripes.", "Layer your clothing."]
    else:
        return "Balanced Frame", ["Tailored fits.", "Bold patterns.", "Straight-leg trousers."]


# ==========================================
# 3. THE APP EXPERIENCE
# ==========================================
st.title("PHENAWA")
st.markdown("### The AI-Driven Personal Stylist")

st.write("Upload a full-body photo to receive precise, geometry-based styling recommendations.")

# Input
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file is not None:
    with st.spinner("Analyzing geometry..."):
        image_bytes = uploaded_file.read()
        body_type, advice = analyze_body(image_bytes)
        
    if body_type:
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="color: #888;">Detected Profile</h3>
            <h2 style="margin-top: 5px;">{body_type.upper()}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        st.markdown("### Your Style Directives")
        for item in advice:
            st.markdown(f"- **{item}**")
    else:
        st.error("Could not detect a full body. Please ensure shoulders and hips are visible.")
else:
    st.info("Awaiting image upload...")
