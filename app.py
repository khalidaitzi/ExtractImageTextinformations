import easyocr as ocr  # OCR
import streamlit as st  # Web App
from PIL import Image  # Image Processing
import numpy as np  # Image Processing
import gtts
import base64
from ocr import add_space

page_bg_img = """
<style>
    [data-testid="stAppViewContainer"]{
        background-image: linear-gradient(294deg, #07062E,#225580 0%,#1C104E);
    }
</style>
"""

css = """
.css-1x8cf1d {
    # background-color : #29e319;
    padding: 12px 35px;
    border-radius: 30px;
    background-image: linear-gradient(87deg,#82829A,#363557);
    border: unset;
    outline: unset;
}
.css-1x8cf1d:hover{
    color : #29e319;
    background-image: linear-gradient(87deg,#363557,#82829A);
}
.row-widget{
    text-align: center;
}
.css-81oif8 {
    color: white;
}
.css-fg4pbf{
    color: white;  
}
.css-rvekum{
    color: white !important;
}
.st-dc{
    color: white;
}
"""

# or `visibility: hidden;`

# st.markdown(f'<img src="text extraction from image/text_extract_proj/image/TechSmith-Blog-ExtractText.png" class="img-fluid">', unsafe_allow_html=True)
image = Image.open('image/TechSmith-Blog-ExtractText.png')
st.image(image, width=120) 

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# title
# st.title("Text Extraction from Images")
page_title = '<p style="font-family:sans-serif; color: #29e319; font-size: 42px;">Text Extraction from Images</p>'
st.markdown(page_title, unsafe_allow_html=True)

# subtitle
#st.markdown("## Text Extraction From Image")

st.markdown(page_bg_img,unsafe_allow_html=True)

# image uploader
# st.markdown(Browse file ,unsafe_allow_html=True)
image = st.file_uploader(label="Upload your image here",
                         type=['png', 'jpg', 'jpeg'])

@st.cache
def load_model():
    reader = ocr.Reader(['en','hi'], model_storage_directory='.')
    return reader

reader = load_model()  # load model
final_text = None
if image is not None:
    input_image = Image.open(image)  # read image
    st.image(input_image)  # display image

    with st.spinner("🤖 AI is at Work! "): # Run spinner while extracting text.

        result = reader.readtext(np.array(input_image))

        result_text = []  # empty list for results

        for text in result:
            result_text.append(text[1])
            #result_text.append("\n")
        final_text = ' '.join(result_text)
        final_text = add_space(final_text)
        st.success("Here you go! Below is the extracted text👇🏻")
        st.code(final_text, language=None)
        image_file_name = image.name if image.name else st.empty()
        st.download_button(
            label="Download",
            data=final_text,
            file_name="extracted_text_from_" + image_file_name + ".txt"
        )
    # Text to Audio part......................................................................
    # Supporting variables
    form_holder = st.empty()
    yes_text = "Yes, I want to hear the Audio."
    no_text = "No, I'm good."
    with form_holder.form("Need audio"):
        # st.write("Text to Audio")
        text_audio = '<p style="font-family:sans-serif; color: #29e319; font-size: 42px;">Text to Audio</p>'
        st.markdown(text_audio, unsafe_allow_html=True)

        audio_required = st.radio("Do You wish to convert the text to audio?", 
            (yes_text, no_text))

        # Every form must have a submit button.
        with st.spinner("🔊Preparing the audio.."):# Run spinner while converting text to speech.
            
            submitted = st.form_submit_button("Submit")
            #form_holder.empty()
            if submitted and audio_required == yes_text:
                tts = gtts.gTTS(final_text)
                audio_file_name = "my_audio.mp3"
                tts.save(audio_file_name)
                with open(audio_file_name, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/mp3')
        #else:
        #    form_holder.empty()
else:
    st.write("Upload an Image")
    
