import streamlit as st
from transformers import pipeline
from PIL import Image

# Setup der Seite
st.set_page_config(page_title="KI-Fundkiste", page_icon="📦")

st.title("📦 Die intelligente Fundkiste")
st.write("Lade ein Foto eines Gegenstands hoch, und die KI sagt dir, was es ist!")

# Modell laden (wird beim ersten Mal von Hugging Face heruntergeladen)
# Wir nutzen "image-classification" mit einem bewährten Modell
@st.cache_resource # Verhindert, dass das Modell bei jedem Klick neu geladen wird
def load_model():
    return pipeline("image-classification", model="google/vit-base-patch16-224")

with st.spinner('KI-Gehirn wird gestartet...'):
    classifier = load_model()

# Datei-Upload
uploaded_file = st.file_uploader("Wähle ein Bild aus...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Bild anzeigen
    image = Image.open(uploaded_file)
    st.image(image, caption='Dein Fundstück', use_container_width=True)
    
    st.write("---")
    st.subheader("Analyse läuft...")
    
    # Vorhersage treffen
    results = classifier(image)
    
    # Ergebnis ausgeben
    best_match = results[0]
    label = best_match['label']
    score = best_match['score']
    
    st.success(f"Ich bin mir zu {score:.2%} sicher: Das ist ein **{label}**.")
    
    # Optional: Weitere Möglichkeiten anzeigen
    with st.expander("Was könnte es sonst noch sein?"):
        for i in range(1, len(results)):
            st.write(f"- {results[i]['label']} ({results[i]['score']:.2%})")
