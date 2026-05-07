import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="KI-Blumen-Fundkiste", layout="wide")

# --- DAS PINK-CARTOON-DESIGN (CSS) ---
st.markdown("""
    <style>
    /* Haupt-Hintergrund in Pink */
    .stApp {
        background-color: #FFC0CB; /* Hellpink */
        background-image: 
            /* Linke Seite: Bäume und Blumen */
            url("https://img.icons8.com/illustrations/parallax/512/forest.png"), 
            /* Rechte Seite: Blumen */
            url("https://img.icons8.com/illustrations/parallax/512/flowers.png");
        background-repeat: no-repeat, no-repeat;
        background-position: left bottom, right bottom;
        background-size: 300px, 300px;
        background-attachment: fixed;
    }

    /* Damit der Text auf Pink lesbar bleibt (Dunkelgrau/Schwarz) */
    h1, h2, h3, p, span, label {
        color: #4B0082 !important; /* Indigo für guten Kontrast auf Pink */
        font-family: 'Comic Sans MS', cursive, sans-serif; /* Cartoon-Vibe */
    }

    /* Weiße Boxen für den Inhalt, damit es nicht zu wild aussieht */
    .stFileUploader, .stButton, div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #FF69B4;
    }

    /* Archiv-Karten Styling */
    div[data-testid="column"] {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 10px;
        border-radius: 15px;
        border: 1px solid #FF69B4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ARCHIV INITIALISIEREN ---
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

# --- KI MODELL LADEN ---
@st.cache_resource
def load_model():
    # Wir bleiben bei MobileNetV2 für Geschwindigkeit
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

with st.spinner('Die Blumen-KI erwacht...'):
    classifier = load_model()

# --- APP LAYOUT ---
st.title("🌸 Die Pinke Cartoon-Fundkiste 🌳")
st.write("Lade ein Bild hoch und schau, was die KI darin entdeckt!")

# Hauptbereich
col_main, col_spacer = st.columns([2, 1])

with col_main:
    uploaded_file = st.file_uploader("Finde etwas Neues...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    results = classifier(image)
    label = results[0]['label']
    score = results[0]['score']

    st.image(image, width=400, caption="Dein Fundstück")
    st.success(f"Ergebnis: Das sieht aus wie ein/eine **{label}**!")
    
    if st.button("🌸 In die Blumenwiese (Archiv) speichern"):
        eintrag = {
            "bild": image,
            "name": label,
            "zeit": datetime.datetime.now().strftime("%H:%M"),
        }
        st.session_state.archiv.insert(0, eintrag)
        st.balloons()

# --- ARCHIV ---
st.write("## 📂 Fundstücke in der Wiese")
if not st.session_state.archiv:
    st.write("Noch keine Schätze gefunden.")
else:
    cols = st.columns(4)
    for idx, item in enumerate(st.session_state.archiv):
        with cols[idx % 4]:
            st.image(item["bild"], use_container_width=True)
            st.write(f"**{item['name']}**")
            st.write(f"🕒 {item['zeit']}")
