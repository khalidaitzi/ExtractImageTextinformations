import streamlit as st
from PIL import Image
import io
import base64
import os
import json
import numpy as np
import uuid
import re

import json

DEFAULT_REGION = "us-east-1"
DEMO_IMAGE = "smart_meter.jpg"

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", DEFAULT_REGION)

client = boto3.client("rekognition", region_name=AWS_DEFAULT_REGION)


def download_button(object_to_download, download_filename, button_text):
    """
    Generates a link to download the given object_to_download.

    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. my.json,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')

    Returns:
    -------
    (str): the anchor tag to download object_to_download

    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')

    """
    object_to_download = json.dumps(object_to_download, ensure_ascii=True, indent=4)
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;

            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = (
        custom_css
        + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'
    )

    return dl_link


def pil_image_to_byte_array(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, "PNG")
    return imgByteArr.getvalue()


@st.cache
def process_image(image_bytes):
    response = client.detect_text(Image={"Bytes": image_bytes})
    return response


st.title("Extract text with AWS rekogniton text extraction")
img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])


if img_file_buffer is not None:
    image_bytes = pil_image_to_byte_array(Image.open(img_file_buffer))
    image_array = np.array(Image.open(img_file_buffer))

else:
    image_bytes = open(DEMO_IMAGE, "rb").read()
    image_array = np.array(Image.open(DEMO_IMAGE))

response = process_image(image_bytes)
extracted_text = [t["DetectedText"] for t in response["TextDetections"]]

st.image(
    image_array, use_column_width=True,
)

st.header("Extracted text")
st.write(extracted_text)

download_button_str = download_button(
    extracted_text, "extracted_text.json", f"Click here to download extracted_text"
)
st.markdown(download_button_str, unsafe_allow_html=True)

st.header("Raw response")
st.write(response)
