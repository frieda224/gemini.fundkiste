import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# Seite konfigurieren
st.set_page_config(page_title="KI-Fundbüro & Archiv", layout="wide")

# 1. ARCHIV-SPEICHER INITIALISIEREN
# Session State sorgt dafür, dass die Liste während der Sitzung bestehen bleibt
if 'archiv' not in st.session_state:
    st.session_state['archiv'] = []

# 2. KI-MODELL LADEN (MobileNetV2 - schnell und effizient)
@st.cache_resource
def load_classifier():
    return pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

classifier = load_classifier()

# --- UI DESIGN ---
st.title("📦 Das digitale Fundbüro")
st.markdown("Lade ein Foto hoch. Die KI erkennt es und fügt es dem öffentlichen Archiv hinzu.")

# Layout mit zwei Spalten: Links Upload, Rechts aktuelles Ergebnis
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Neues Fundstück scannen...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Vorhersage
    with st.spinner('KI analysiert...'):
        predictions = classifier(image)
        result_label = predictions[0]['label']
        conf = predictions[0]['score']

    with col2:
        st.image(image, caption="Hochgeladenes Bild", width=300)
        st.success(f"Erkannt als: **{result_label}** ({conf:.1%})")
        
        # Button zum Speichern im Archiv
        if st.button("Ab ins Archiv damit!"):
            # Eintrag erstellen
            eintrag = {
                "bild": image,
                "name": result_label,
                "zeit": datetime.datetime.now().strftime("%H:%M:%S"),
                "sicherheit": f"{conf:.1%}"
            }
            # Ganz oben in die Liste einfügen
            st.session_state.archiv.insert(0, eintrag)
            st.toast("Im Archiv gespeichert!")

# --- ARCHIV SEKTION ---
st.divider()
st.header("📂 Fundkisten-Archiv")

if not st.session_state.archiv:
    st.info("Das Archiv ist noch leer. Scanne den ersten Gegenstand!")
else:
    # Raster für das Archiv (3 Bilder pro Zeile)
    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.archiv):
        with cols[idx % 3]:
            st.image(item["bild"], use_container_width=True)
            st.caption(f"**Was:** {item['name']}  \n**Wann:** {item['zeit']} (KI-Konfidenz: {item['sicherheit']})")
            st.write("---")
