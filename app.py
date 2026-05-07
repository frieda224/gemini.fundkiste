import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="Erdbeer-KI-Fundkiste", layout="wide")

# --- DAS ERDBEER-STREIFEN-DESIGN (CSS) ---
st.markdown("""
    <style>
    /* 1. Hintergrund: Hellrosa mit hellblauen Streifen */
    .stApp {
        background-color: #FFD1DC; /* Hellrosa */
        background-image: linear-gradient(90deg, rgba(173, 216, 230, 0.4) 50%, transparent 50%); /* Hellblaue Streifen */
        background-size: 80px 80px;
        position: relative;
    }

    /* 2. Erdbeeren im Hintergrund (fixiert) */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        /* Nutzt ein Erdbeer-Muster von einem Icon-Provider */
        background-image: url("https://img.icons8.com/emoji/96/strawberry.png");
        background-repeat: repeat;
        background-size: 150px;
        opacity: 0.2; /* Dezent im Hintergrund */
        z-index: 0;
        pointer-events: none;
    }

    /* 3. Dunkelblaue Schrift für alles */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #00008B !important; /* Dunkelblau (DarkBlue) */
        font-family: 'Comic Sans MS', cursive, sans-serif;
        font-weight: bold;
    }

    /* 4. Weiße Box für die Bedienung, damit man trotz Streifen alles erkennt */
    .main-container {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 40px;
        border-radius: 25px;
        border: 4px solid #00008B;
        z-index: 10;
        position: relative;
    }

    /* Styling für den Datei-Uploader und Buttons */
    .stFileUploader, .stButton>button {
        border: 2px solid #00008B !important;
        border-radius: 10px;
    }
    
    .stButton>button {
        background-color: #00008B !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ARCHIV & KI LOGIK ---
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

@st.cache_resource
def load_model():
    # Schnelles Modell von Google
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

classifier = load_model()

# --- APP INHALT ---
# Wir packen alles in ein Div mit der Klasse 'main-container' für das Design
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.title("🍓 Die Erdbeer-Streifen Fundkiste 🍓")
st.write("Scanne ein Objekt und die KI sortiert es ins Archiv!")

uploaded_file = st.file_uploader("Bild hier reinwerfen...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    with st.spinner('KI analysiert...'):
        res = classifier(img)
        label = res[0]['label']
    
    col_img, col_txt = st.columns([1, 1])
    with col_img:
        st.image(img, width=300, caption="Dein Fundstück")
    with col_txt:
        st.subheader(f"Erkannt als: {label}")
        if st.button("Ab ins Erdbeer-Archiv!"):
            st.session_state.archiv.insert(0, {
                "img": img, 
                "name": label, 
                "time": datetime.datetime.now().strftime("%H:%M")
            })
            st.balloons()

st.markdown('</div>', unsafe_allow_html=True)

# --- ARCHIV SEKTION ---
st.write("---")
st.header("📂 Das Archiv")

if st.session_state.archiv:
    cols = st.columns(4)
    for i, item in enumerate(st.session_state.archiv):
        with cols[i % 4]:
            # Archiv-Karten auch mit weißem Hintergrund für Lesbarkeit
            st.markdown('<div style="background:rgba(255,255,255,0.7); padding:10px; border-radius:10px; border:2px solid #00008B;">', unsafe_allow_html=True)
            st.image(item["img"], use_container_width=True)
            st.write(f"**{item['name']}**")
            st.write(f"🕒 {item['time']}")
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.write("Noch keine Erdbeeren... äh, Fundstücke hier!")
