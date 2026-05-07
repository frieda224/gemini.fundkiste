import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="Fundkiste", layout="wide")

# --- DESIGN: HELLBLAU & ERDBEEREN OHNE KÄSTEN ---
st.markdown("""
    <style>
    /* Hintergrund: Hellblau mit schmalen Streifen */
    .stApp {
        background-color: #E0F2F7; 
        background-image: linear-gradient(90deg, #F0F9FF 50%, transparent 50%); 
        background-size: 40px 100%; 
    }

    /* Erdbeeren direkt auf dem Hintergrund */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url("https://img.icons8.com/emoji/48/strawberry.png");
        background-repeat: repeat;
        background-size: 100px 100px;
        opacity: 0.15;
        z-index: 0;
        pointer-events: none;
    }

    /* Dekoration: Baum und Pflanze an den Seiten */
    .tree-left {
        position: fixed;
        left: 2%;
        bottom: 5%;
        width: 180px;
        z-index: 1;
    }
    .berry-right {
        position: fixed;
        right: 2%;
        bottom: 5%;
        width: 180px;
        z-index: 1;
    }

    /* Text-Farben (Dunkelblau) */
    h1, h2, h3, p, label, .stMarkdown {
        color: #003366 !important;
        font-family: 'Arial', sans-serif;
    }

    /* Buttons */
    .stButton>button {
        background-color: #FF4D6D !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 20px !important;
    }

    /* Archiv-Elemente (einfache weiße Boxen, nicht durchsichtig) */
    .archiv-item {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #003366;
        margin-bottom: 10px;
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
    # Lädt das Modell ohne Anmeldung direkt von Hugging Face
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

with st.spinner('Fundkiste wird geladen...'):
    classifier = load_ki()

# --- APP INHALT ---
st.title("🍓 Fundkiste")
st.write("Lade ein Foto hoch, um den Gegenstand zu identifizieren.")

# Upload Bereich
uploaded_file = st.file_uploader("Bild wählen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    res = classifier(img)
    label = res[0]['label'].split(',')[0].title().replace('_', ' ')
    
    col_img, col_info = st.columns(2)
    with col_img:
        st.image(img, width=300)
    with col_info:
        st.subheader(f"Erkannt: {label}")
        if st.button("Ins Archiv speichern"):
            st.session_state.archiv.insert(0, {
                "img": img, 
                "name": label, 
                "time": datetime.datetime.now().strftime("%H:%M")
            })
