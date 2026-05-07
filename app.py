import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="Erdbeer-Fundkiste", layout="wide")

# --- DAS DESIGN (BREITE STREIFEN & DUNKELBLAU) ---
st.markdown("""
    <style>
    /* Hintergrund: Hellrosa mit SEHR BREITEN hellblauen Streifen */
    .stApp {
        background-color: #FFD1DC; 
        background-image: linear-gradient(90deg, #ADD8E6 50%, transparent 50%);
        background-size: 300px 300px; /* Hier stellen wir die Breite ein (150px pro Farbe) */
    }

    /* Erdbeeren als Muster über das Ganze */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://img.icons8.com/emoji/96/strawberry.png");
        background-repeat: repeat;
        background-size: 120px;
        opacity: 0.15;
        z-index: 0;
        pointer-events: none;
    }

    /* Dunkelblaue Schrift und Comic Sans */
    h1, h2, h3, p, span, label, div {
        color: #00008B !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    /* Weiße Box für bessere Lesbarkeit */
    .main-box {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 30px;
        border-radius: 20px;
        border: 5px solid #00008B;
        margin-top: 20px;
    }

    /* Buttons anpassen */
    .stButton>button {
        background-color: #00008B !important;
        color: white !important;
        border-radius: 15px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KI LOGIK ---
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

# Wir nutzen ein sehr leichtes Modell, damit es schnell lädt
@st.cache_resource
def load_ki():
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

# Lade-Anzeige für die Schüler
with st.spinner('Erdbeer-KI wird warmgelaufen...'):
    classifier = load_ki()

# --- APP INHALT ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("🍓 Die breite Streifen-Fundkiste 🍓")
st.write("Dunkelblaue Schrift & Erdbeeren – Alles bereit!")

datei = st.file_uploader("Bild hier hochladen", type=["jpg", "jpeg", "png"])

if datei:
    bild = Image.open(datei)
    ergebnis = classifier(bild)
    name = ergebnis[0]['label']
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(bild, width=300)
    with col2:
        st.subheader(f"Gefunden: {name}")
        if st.button("Ab ins Archiv!"):
            eintrag = {
                "bild": bild,
                "name": name,
                "zeit": datetime.datetime.now().strftime("%H:%M")
            }
            st.session_state.archiv.insert(0, eintrag)
            st.balloons()

st.markdown('</div>', unsafe_allow_html=True)

# --- ARCHIV ---
st.write("### 📂 Fundstücke")
if st.session_state.archiv:
    spalten = st.columns(4)
    for i, item in enumerate(st.session_state.archiv):
        with spalten[i % 4]:
            st.markdown('<div style="background:white; padding:10px; border-radius:10px; border:2px solid #00008B;">', unsafe_allow_html=True)
            st.image(item["bild"], use_container_width=True)
            st.write(f"**{item['name']}**")
            st.write(f"🕒 {item['zeit']}")
            st.markdown('</div>', unsafe_allow_html=True)
