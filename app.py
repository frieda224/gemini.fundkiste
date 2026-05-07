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
        background-color: #FFF5F7; 
        background-image: linear-gradient(90deg, #F0F9FF 50%, transparent 50%); 
        background-size: 40px 40px; 
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
        background-image: 
            url("https://img.icons8.com/emoji/48/strawberry.png"),
            url("https://img.icons8.com/emoji/48/cherries.png");
        background-repeat: repeat, repeat;
        background-position: 0 0, 20px 20px; 
        background-size: 100px 100px;
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
        width: 100%;
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
st.write("Schmale Streifen, Erdbeeren und Kirschen. Lade dein Foto hoch!")

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
        # Hier ist die korrigierte Stelle
        st.subheader(f"Gefunden: {name}")
        
        if st.button("Ab ins Früchte-Archiv"):
            eintrag = {
                "bild": bild,
                "name": name,
                "zeit": datetime.datetime.now().strftime("%H:%M")
            }
            st.session_state.archiv.insert(0, eintrag)
            st.toast("Im Archiv gespeichert! ✨")
            st.balloons()

st.markdown('</div>', unsafe_allow_html=True)

# --- ARCHIV ---
st.write("---")
st.subheader("☁️ Letzte Funde")

if st.session_state.archiv:
    cols = st.columns(4)
    for i, item in enumerate(st.session_state.archiv):
        with cols[i % 4]:
            st.markdown('<div style="background:white; padding:15px; border-radius:20px; border:1px solid #FFE4E1; margin-bottom: 15px;">', unsafe_allow_html=True)
            st.image(item["bild"], use_container_width=True)
            st.write(f"**{item['name']}**")
            st.write(f"<small>{item['zeit']} Uhr</small>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Noch ist die Kiste leer. Zeit für den ersten Fund!")
