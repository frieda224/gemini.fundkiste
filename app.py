import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="Cozy Strawberry Box", layout="wide")

# --- COZY SWEET DESIGN MIT SCHMALEN STREIFEN ---
st.markdown("""
    <style>
    /* Hintergrund: Schmale, sanfte Streifen */
    .stApp {
        background-color: #FFF5F7; /* Ganz zartes Rosa */
        background-image: linear-gradient(90deg, #F0F9FF 50%, transparent 50%); /* Zartes Blau */
        background-size: 40px 40px; /* Breite der Streifen (20px pro Farbe) */
        position: relative;
    }

    /* Erdbeeren im Hintergrund auf den Streifen */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://img.icons8.com/emoji/48/strawberry.png");
        background-repeat: repeat;
        background-size: 80px;
        opacity: 0.1;
        z-index: 0;
        pointer-events: none;
    }

    /* Schrift und Look */
    h1, h2, h3, p, label {
        color: #4A4A4A !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main-box {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 30px;
        border: 1px solid #FFD1DC;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        z-index: 10;
        position: relative;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #FFB7C5 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KI LOGIK ---
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

# Wir nutzen das allerschnellste Modell für Web-Apps
@st.cache_resource
def load_ki():
    try:
        return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")
    except:
        return None

# Lade-Animation
with st.spinner('Erdbeer-Kiste wird vorbereitet...'):
    classifier = load_ki()

# --- APP INHALT ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("🍓 My Cozy Fundkiste")
st.write("Schmale Streifen & Cozy Vibes. Lade ein Foto hoch!")

datei = st.file_uploader("", type=["jpg", "jpeg", "png"])

if datei and classifier:
    bild = Image.open(datei)
    ergebnis = classifier(bild)
    name = ergebnis[0]['label'].split(',')[0].title()
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(bild, use_container_width=True)
    with col2:
        st.subheader(f"Gefunden: {name}")
        if st.button("Ab ins Archiv"):
            st.session_state.archiv.insert(0, {
                "bild": bild,
                "name": name,
                "zeit": datetime.datetime.now().strftime("%H:%M")
            })
            st.toast("Gespeichert!")

st.markdown('</div>', unsafe_allow_html=True)

# --- ARCHIV ---
st.write("---")
if st.session_state.archiv:
    cols = st.columns(4)
    for i, item in enumerate(st.session_state.archiv):
        with cols[i % 4]:
            st.markdown('<div style="background:white; padding:10px; border-radius:15px; border:1px solid #EEE;">', unsafe_allow_html=True)
            st.image(item["bild"], use_container_width=True)
            st.write(f"**{item['name']}**")
            st.markdown('</div>', unsafe_allow_html=True)
