import streamlit as st
from transformers import pipeline
from PIL import Image
import datetime

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="My Cozy Fundkiste", layout="wide")

# --- DAS ULTIMATIVE COZY DESIGN (BASIEREND AUF DEINEM BILD) ---
st.markdown("""
    <style>
    /* 1. Hintergrund: Schmale blau-rosa Streifen */
    .stApp {
        background-color: #FFD1DC; 
        background-image: linear-gradient(90deg, #CEF0FF 50%, transparent 50%); 
        background-size: 60px 100%; 
    }

    /* 2. Überall verstreute Früchte im Hintergrund */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            url("https://img.icons8.com/emoji/48/strawberry.png"),
            url("https://img.icons8.com/emoji/48/cherries.png");
        background-repeat: repeat;
        background-position: 0 0, 30px 30px;
        background-size: 150px 150px;
        opacity: 0.2;
        z-index: 0;
    }

    /* 3. Der zentrale helle Rahmen (Main Container) */
    .main-box {
        background-color: #FFF9E5; /* Cremiges Gelb/Weiß */
        padding: 40px;
        border-radius: 50px;
        border: 8px solid #FF8DA1; /* Rosa gepunkteter Rahmen-Effekt via Border */
        outline: 15px solid #FFF9E5;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        max-width: 800px;
        margin: 50px auto;
        position: relative;
        z-index: 5;
        text-align: center;
    }

    /* 4. Dekorative Elemente (Baum und Pflanzen) */
    /* Kirschbaum links */
    .tree-left {
        position: fixed;
        left: 10%;
        bottom: 15%;
        width: 250px;
        z-index: 6;
    }
    /* Erdbeerpflanze rechts */
    .berry-right {
        position: fixed;
        right: 10%;
        bottom: 15%;
        width: 250px;
        z-index: 6;
    }

    /* 5. Styling für Text und Archiv */
    h1, h2, h3, p {
        color: #1A3A5A !important;
        font-family: 'Comic Sans MS', cursive,
