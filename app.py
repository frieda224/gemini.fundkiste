import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="Cozy Strawberry Box", layout="wide")

# --- COZY SWEET DESIGN (CSS) ---
st.markdown("""
    <style>
    /* 1. Hintergrund: Weiche, breite Streifen in Cozy-Farben */
    .stApp {
        background-color: #FFF0F5; /* Lavender Blush (sehr sanftes Rosa) */
        background-image: linear-gradient(90deg, #E0F2F7 50%, transparent 50%); /* Sehr helles Pastellblau */
        background-size: 240px 240px;
        position: relative;
    }

    /* 2. Erdbeeren über den gesamten Hintergrund verteilt */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://img.icons8.com/emoji/96/strawberry.png");
        background-repeat: repeat;
        background-size: 100px;
        opacity: 0.12; /* Dezent und gemütlich */
        z-index: 0;
        pointer-events: none;
    }

    /* 3. Cozy Typography: Dunkelblau, aber weicher */
    h1, h2, h3, p, span, label, div {
        color: #2C3E50 !important; /* Ein sanfteres Dunkelblau-Grau */
        font-family: 'Quicksand', 'Segoe UI', sans-serif;
    }

    /* 4. Die "Main Card" - Weich und abgerundet */
    .main-box {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 40px;
        border-radius: 40px; /* Super abgerundet für Cozy-Look */
        border: 2px solid #D1E8E2;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-top: 20px;
        z-index: 10;
        position: relative;
    }

    /* Styling für den Datei-Uploader */
    .stFileUploader {
        border: 2px dashed #B8D8D8 !important;
        border-radius: 20px;
        background: #F9FFFF;
    }

    /* Der Button - Sweet & Rounded */
    .stButton>button {
        background-color: #FFB7C5 !important; /* Sanftes Erdbeer-Rosa */
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        background-color: #FFA4B5 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KI LOGIK ---
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

@st.cache_resource
def load_ki():
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

with st.spinner('Dein gemütliches Fundbüro wird vorbereitet...'):
    classifier = load_ki()

# --- APP INHALT ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("🍓 My Cozy Fundkiste")
st.write("Lade ein Bild hoch und lass uns schauen, was du Schönes gefunden hast.")

datei = st.file_uploader("", type=["jpg", "jpeg", "png"])

if datei:
    bild = Image.open(datei)
    ergebnis = classifier(bild)
    name = ergebnis[0]['label'].replace('_', ' ').title() # Schönere Formatierung
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(bild, use_container_width=True, caption="Dein Fundstück")
    with col2:
        st.subheader(f"Gefunden: {name}")
        if st.button("Ab ins Archiv"):
            eintrag = {
                "bild": bild,
                "name": name,
                "zeit": datetime.datetime.now().strftime("%H:%M")
            }
            st.session_state.archiv.insert(0, eintrag)
            st.toast("Gespeichert! ✨")

st.markdown('</div>', unsafe_allow_html=True)

# --- ARCHIV ---
st.write("---")
st.subheader("☁️ Gesammelte Schätze")

if st.session_state.archiv:
    spalten = st.columns(4)
    for i, item in enumerate(st.session_state.archiv):
        with spalten[i % 4]:
            st.markdown('<div style="background:white; padding:15px; border-radius:25px; border:1px solid #FFD1DC; margin-bottom:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.02);">', unsafe_allow_html=True)
            st.image(item["bild"], use_container_width=True)
            st.write(f"**{item['name']}**")
            st.write(f"<small>{item['zeit']} Uhr</small>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Noch ist die Kiste leer. Zeit für den ersten Fund!")
