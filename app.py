import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-STYLING (DAS BUNTE) ---
st.set_page_config(page_title="KI-Fundkiste", layout="wide")

# Hier passiert die Magie: Wir injizieren CSS für den bunten Hintergrund
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(315deg, #4f2991 3%, #7dc4ff 38%, #36cfcc 68%, #a92ed3 98%);
        background-size: 400% 400%;
        color: white;
    }
    /* Stil für die Karten im Archiv */
    .stCard {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 15px;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 20px;
    }
    h1, h2, h3, p {
        color: white !important;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ARCHIV INITIALISIEREN ---
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

# --- KI MODELL ---
@st.cache_resource
def load_model():
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

with st.spinner('KI-Power wird geladen...'):
    classifier = load_model()

# --- HAUPTSEITE ---
st.title("📦 Die bunte KI-Fundkiste")
st.write("Scan dein Fundstück und lass die KI entscheiden!")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Bild hochladen...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    results = classifier(image)
    label = results[0]['label']
    score = results[0]['score']

    with col2:
        st.image(image, caption="Scan läuft...", width=300)
        st.success(f"Gefunden: **{label}** ({score:.1%})")
        
        if st.button("Ins öffentliche Archiv speichern"):
            eintrag = {
                "bild": image,
                "name": label,
                "zeit": datetime.datetime.now().strftime("%H:%M"),
                "sicherheit": f"{score:.1%}"
            }
            st.session_state.archiv.insert(0, eintrag)
            st.balloons()

# --- ARCHIV ANZEIGEN ---
st.divider()
st.header("📂 Letzte Funde")

if not st.session_state.archiv:
    st.write("Noch keine Funde gespeichert.")
else:
    # Archiv in 4 Spalten anzeigen
    cols = st.columns(4)
    for idx, item in enumerate(st.session_state.archiv):
        with cols[idx % 4]:
            st.image(item["bild"], use_container_width=True)
            st.markdown(f"**{item['name']}**  \n🕒 {item['zeit']} ({item['sicherheit']})")
            st.write("---")

Dein Projektbericht und der Code sind nun fertig! Viel Erfolg im Informatikunterricht. Lass mich wissen, wenn du noch eine Änderung wünscht!
