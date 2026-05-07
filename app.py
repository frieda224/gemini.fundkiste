import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="My Cozy Fundkiste", layout="wide")

# --- COZY DESIGN (HELLBLAU & NUR ERDBEEREN) ---
st.markdown("""
    <style>
    /* 1. Hintergrund: Hellblau mit sanften Streifen */
    .stApp {
        background-color: #E0F2F7; /* Sanftes Hellblau */
        background-image: linear-gradient(90deg, #F0F9FF 50%, transparent 50%); 
        background-size: 60px 100%; 
    }

    /* 2. Nur Erdbeeren im Hintergrund verstreut */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url("https://img.icons8.com/emoji/48/strawberry.png");
        background-repeat: repeat;
        background-size: 150px 150px;
        opacity: 0.15;
        z-index: 0;
        pointer-events: none;
    }

    /* 3. Der zentrale helle Rahmen (Main Container) */
    .main-box {
        background-color: #FFFDF5; 
        padding: 40px;
        border-radius: 50px;
        border: 8px solid #FFB7C5; /* Weiches Rosa für den Rahmen */
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        max-width: 800px;
        margin: 50px auto;
        position: relative;
        z-index: 5;
        text-align: center;
    }

    /* 4. Dekorative Elemente an den Seiten */
    .tree-left {
        position: fixed;
        left: 5%;
        bottom: 10%;
        width: 220px;
        z-index: 6;
    }
    .berry-right {
        position: fixed;
        right: 5%;
        bottom: 10%;
        width: 220px;
        z-index: 6;
    }

    /* Schrift-Styling */
    h1, h2, h3, p {
        color: #2C3E50 !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #FF8DA1 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 10px 40px !important;
        font-size: 20px !important;
        border: none !important;
        font-weight: bold;
    }

    /* Archiv Karten */
    .archive-card {
        background: white;
        padding: 15px;
        border-radius: 25px;
        border: 2px solid #E0F2F7;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
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

with st.spinner('Deine Fundkiste wird vorbereitet...'):
    classifier = load_ki()

# --- APP INHALT ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.markdown("<h1>🍓 My Cozy Fundkiste</h1>", unsafe_allow_html=True)
st.write("Lade ein Foto hoch und lass die KI dein Fundstück benennen!")

uploaded_file = st.file_uploader("Bild auswählen", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    img = Image.open(uploaded_file)
    res = classifier(img)
    label = res[0]['label'].split(',')[0].title().replace('_', ' ')
    
    st.image(img, width=320)
    st.subheader(f"Gefunden: {label}")
    
    if st.button("🍓 Ins Archiv legen"):
        st.session_state.archiv.insert(0, {
            "img": img, 
            "name": label, 
            "time": datetime.datetime.now().strftime("%H:%M")
        })
        st.balloons()
        st.toast("Erfolgreich gespeichert! ✨")

st.markdown('</div>', unsafe_allow_html=True)

# --- ARCHIV ---
st.markdown("<h2 style='text-align: center; margin-top: 30px;'>☁️ Letzte Schätze</h2>", unsafe_allow_html=True)

if st.session_state.archiv:
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.archiv):
        with cols[i % 3]:
            st.markdown('<div class="archive-card">', unsafe_allow_html=True)
            st.image(item["img"], use_container_width=True)
            st.markdown(f"<p style='margin: 10px 0 0 0;'><b>{item['name']}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<small style='color: #888;'>🕒 {item['time']} Uhr</small>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Noch keine Fundstücke im Archiv.")
