import streamlit as st
import pytesseract
from PIL import Image

# Configuration de pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' # chemin vers l'exécutable Tesseract OCR

# Fonction pour extraire le texte d'une image
def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text

# Affichage de l'interface utilisateur
st.title('Extraction d\'informations à partir d\'images')

# Sélection de l'image à traiter
image_file = st.file_uploader('Sélectionnez une image', type=['jpg', 'jpeg', 'png'])

if image_file is not None:
    # Conversion de l'image en objet Image
    image = Image.open(image_file)

    # Affichage de l'image
    st.image(image, caption='Image originale', use_column_width=True)

    # Extraction du texte
    text = extract_text(image)

    # Affichage du texte extrait
    st.subheader('Texte extrait :')
    st.write(text)

    # Extraction des nombres
    numbers = []
    for word in text.split():
        if word.isnumeric():
            numbers.append(int(word))

    # Affichage des nombres extraits
    if len(numbers) > 0:
        st.subheader('Nombres extraits :')
        st.write(numbers)
    else:
        st.warning('Aucun nombre n\'a été extrait de l\'image.')
