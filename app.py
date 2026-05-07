import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="Magische KI-Fundkiste", layout="wide")

# --- DAS ULTIMATIVE DESIGN (CSS ANIMATIONEN) ---
st.markdown("""
    <style>
    /* 1. Pinker Hintergrund mit drehenden Sternen */
    .stApp {
        background-color: #FFC0CB;
        background-image: url("https://www.transparenttextures.com/patterns/stardust.png"); /* Sterne Textur */
        animation: rotateStars 100s linear infinite;
    }

    @keyframes rotateStars {
        from { background-position: 0 0; }
        to { background-position: 1000px 1000px; }
    }

    /* 2. Große Bäume im Hintergrund (Links und Rechts) */
    .stApp::before {
        content: "";
        position: fixed;
        bottom: 0;
        left: -50px;
        width: 400px;
        height: 600px;
        background-image: url("https://img.icons8.com/illustrations/parallax/512/tree.png");
        background-size: contain;
        background-repeat: no-repeat;
        z-index: 0;
        opacity: 0.8;
    }

    .stApp::after {
        content: "";
        position: fixed;
        bottom: 0;
        right: -50px;
        width: 400px;
        height: 600px;
        background-image: url("https://img.icons8.com/illustrations/parallax/512/tree.png");
        background-size: contain;
        background-repeat: no-repeat;
        transform: scaleX(-1); /* Spiegeln für die rechte Seite */
        z-index: 0;
        opacity: 0.8;
    }

    /* 3. Wachsende Blumen Animation */
    @keyframes grow {
        from { transform: scale(0) translateY(100px); }
        to { transform: scale(1) translateY(0); }
    }

    .flower-container {
        position: fixed;
        bottom: 0;
        width: 100%;
        display: flex;
        justify-content: space-around;
        z-index: 1;
        pointer-events: none;
    }

    .flower {
        width: 80px;
        height: 80px;
        background-image: url("https://img.icons8.com/illustrations/parallax/512/flowers.png");
        background-size: contain;
        background-repeat: no-repeat;
        animation: grow 3s ease-out forwards;
    }

    /* 4. Content lesbar machen */
    .main-card {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 30px;
        border-radius: 30px;
        border: 5px solid #FF69B4;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        z-index: 10;
        position: relative;
    }
    
    h1, p { color: #8B008B !important; font-family: 'Comic Sans MS', cursive; }
    </style>
    
    <!-- Blumen Container im HTML -->
    <div class="flower-container">
        <div class="flower" style="animation-delay: 0.5s;"></div>
        <div class="flower" style="animation-delay: 1.2s;"></div>
        <div class="flower" style="animation-delay: 0.2s;"></div>
        <div class="flower" style="animation-delay: 1.8s;"></div>
        <div class="flower" style="animation-delay: 0.8s;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- ARCHIV & KI LOGIK ---
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

@st.cache_resource
def load_model():
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

classifier = load_model()

# --- APP INHALT ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.title("🌟 Magische Fundkiste im Wald 🌳")
st.write("Lade ein Bild hoch – die KI und die Natur helfen dir beim Suchen!")

uploaded_file = st.file_uploader("Was hast du gefunden?", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    res = classifier(img)
    label = res[0]['label']
    
    st.image(img, width=350)
    st.subheader(f"Gefunden: {label}")
    
    if st.button("✨ Ins Archiv legen"):
        st.session_state.archiv.insert(0, {"img": img, "name": label, "time": datetime.datetime.now().strftime("%H:%M")})
        st.balloons()
st.markdown('</div>', unsafe_allow_html=True)

# --- ARCHIV UNTEN ---
st.write("---")
st.header("📂 Archiv der Fundstücke")
if st.session_state.archiv:
    cols = st.columns(4)
    for i, item in enumerate(st.session_state.archiv):
        with cols[i % 4]:
            st.image(item["img"], use_container_width=True)
            st.write(f"**{item['name']}** ({item['time']})")
