import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="My Cozy Fundkiste", layout="wide")

# --- DAS ULTIMATIVE COZY DESIGN ---
st.markdown("""
    <style>
    /* 1. Hintergrund: Schmale blau-rosa Streifen */
    .stApp {
        background-color: #FFD1DC; 
        background-image: linear-gradient(90deg, #CEF0FF 50%, transparent 50%); 
        background-size: 60px 100%; 
    }

    /* 2. Überall verstreute Früchte im Hintergrund */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            url("https://img.icons8.com/emoji/48/strawberry.png"),
            url("https://img.icons8.com/emoji/48/cherries.png");
        background-repeat: repeat;
        background-position: 0 0, 30px 30px;
        background-size: 150px 150px;
        opacity: 0.2;
        z-index: 0;
    }

    /* 3. Der zentrale helle Rahmen (Main Container) */
    .main-box {
        background-color: #FFF9E5; 
        padding: 40px;
        border-radius: 50px;
        border: 8px solid #FF8DA1; 
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        max-width: 800px;
        margin: 50px auto;
        position: relative;
        z-index: 5;
        text-align: center;
    }

    /* 4. Dekorative Elemente */
    .tree-left {
        position: fixed;
        left: 5%;
        bottom: 10%;
        width: 200px;
        z-index: 6;
    }
    .berry-right {
        position: fixed;
        right: 5%;
        bottom: 10%;
        width: 200px;
        z-index: 6;
    }

    h1, h2, h3, p {
        color: #1A3A5A !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    .stButton>button {
        background-color: #E63946 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 10px 30px !important;
        font-size: 20px !important;
        border: none !important;
    }

    .archive-card {
        background: white;
        padding: 15px;
        border-radius: 20px;
        border: 2px solid #FFD1DC;
        margin-bottom: 20px;
    }
    </style>

    <img src="https://img.icons8.com/illustrations/parallax/512/tree.png" class="tree-left">
    <img src="https://img.icons8.com/illustrations/parallax/512/strawberry.png" class="berry-right">
    """, unsafe_allow_html=True)

# --- KI LOGIK ---
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

@st.cache_resource
def load_ki():
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

classifier = load_ki()

# --- APP INHALT ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.markdown("<h1>🍓🍒 My Cozy Fundkiste</h1>", unsafe_allow_html=True)
st.write("Willkommen in deinem gemütlichen Fundbüro! Scanne einen Schatz und wir sagen dir, was es ist.")

uploaded_file = st.file_uploader("Datei hochladen", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    img = Image.open(uploaded_file)
    res = classifier(img)
    label = res[0]['label'].split(',')[0].title()
    
    st.image(img, width=300)
    st.subheader(f"Gefunden: {label}")
    
    if st.button("🍓 Ins Archiv legen"):
        st.session_state.archiv.insert(0, {
            "img": img, 
            "name": label, 
            "time": datetime.datetime.now().strftime("%H:%M")
        })
        st.balloons()

st.markdown('</div>', unsafe_allow_html=True)

# --- ARCHIV ---
st.markdown("<h2 style='text-align: center;'>Archive</h2>", unsafe_allow_html=True)

if st.session_state.archiv:
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.archiv):
        with cols[i % 3]:
            st.markdown('<div class="archive-card">', unsafe_allow_html=True)
            st.image(item["img"], use_container_width=True)
            st.markdown(f"**Gefunden: {item['name']}**")
