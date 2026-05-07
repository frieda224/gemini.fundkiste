import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="Cozy Fruit Box", layout="wide")

# --- COZY FRUIT DESIGN (STREIFEN, ERDBEEREN & KIRSCHEN) ---
st.markdown("""
    <style>
    /* Hintergrund: Schmale, sanfte Streifen */
    .stApp {
        background-color: #FFF5F7; /* Ganz zartes Rosa */
        background-image: linear-gradient(90deg, #F0F9FF 50%, transparent 50%); /* Zartes Blau */
        background-size: 40px 40px; /* Schmale Streifen */
        position: relative;
    }

    /* Frucht-Layer: Erdbeeren und Kirschen gemischt */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        /* Zwei Hintergrundbilder: Eines für Erdbeeren, eines für Kirschen */
        background-image: 
            url("https://img.icons8.com/emoji/48/strawberry.png"),
            url("https://img.icons8.com/emoji/48/cherries.png");
        background-repeat: repeat, repeat;
        /* Versetzte Positionierung, damit sie sich mischen */
        background-position: 0 0, 40px 40px; 
        background-size: 120px 120px;
        opacity: 0.12;
        z-index: 0;
        pointer-events: none;
    }

    /* Schrift und Cozy-Look */
    h1, h2, h3, p, label {
        color: #3D3D3D !important;
        font-family: 'Quicksand', sans-serif;
    }

    .main-box {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 30px;
        border-radius: 35px;
        border: 2px solid #FFD1DC;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        z-index: 10;
        position: relative;
        margin-top: 10px;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #FFB7C5 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KI LOGIK ---
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

@st.cache_resource
def load_ki():
    # Nutzt das schnelle MobileNetV2 Modell
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

with st.spinner('Früchte werden sortiert...'):
    classifier = load_ki()

# --- APP INHALT ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("🍓 My Cozy Fruit-Fundkiste 🍒")
st.write("Schmale Streifen, Erdbeeren und Kirschen. Was hast du heute gefunden?")

datei = st.file_uploader("", type=["jpg", "jpeg", "png"])

if datei:
    bild = Image.open(datei)
    ergebnis = classifier(bild)
    # Den Namen des Objekts schön formatieren
    name = ergebnis[0]['label'].split(',')[0].title().replace('_', ' ')
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(bild, use_container_width=True, caption="Dein Fundstück")
    with col2:
        st.subheader(f"G
