import streamlit as st
from PIL import Image
import os
from io import BytesIO
from streamlit_option_menu import option_menu
from pydub import AudioSegment
import pickle
import numpy as np

# Function to load the model and scaler
@st.cache(allow_output_mutation=True)
def load_model_and_scaler():
    with open("pipe.pkl", "rb") as f:
        loaded_model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return loaded_model, scaler

# Load the model and scaler
loaded_model, scaler = load_model_and_scaler()

# Navigasi sidebar
with st.sidebar:
    selected = option_menu('Kompresi Gambar & Audio',
                           ['Beranda','Kompresi Gambar', 'Kompresi Audio'],
                           default_index=0)

if (selected == 'Beranda'):
    st.title('Selamat Datang di Kompresi Gambar dan Audio!')
    
# halaman kompresi gambar
if (selected == 'Kompresi Gambar'):
    def kompresi_gambar():
        st.title("Kompresi Gambar")
        st.write("Muat gambar dan kompres dengan kualitas tertentu.")

        uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar Asli", use_column_width=True)

            # Slider untuk memilih kualitas kompresi
            quality = st.slider("Kualitas Kompresi (0-100)", 0, 100, 50)

            if st.button("Kompresi"):
                compressed_image = compress_image(image, quality)
                st.image(compressed_image, caption="Gambar Setelah Kompresi", use_column_width=True)
                st.success("Gambar berhasil dikompresi!")
                download_button(compressed_image)

    def download_button(image_bytes):
        st.download_button(
            label="Unduh Gambar Kompresi",
            data=image_bytes,
            file_name="compressed_image.jpg",
            mime="image/jpeg"
        )

    def compress_image(image, quality):
        img = image.copy()
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        byte_im = buf.getvalue()
        return byte_im
    
    if __name__ == "__main__":
        kompresi_gambar()


# Fungsi untuk melakukan kompresi audio
def compress_audio(audio_bytes, bitrate='64k'):
    audio = AudioSegment.from_file(BytesIO(audio_bytes))
    compressed_audio = audio.export(format="mp3", bitrate=bitrate)
    return compressed_audio

if selected == 'Kompresi Audio':
    st.title('Kompresi Audio')
    st.write("Muat audio dan kompres dengan kualitas tertentu.")

    uploaded_file = st.file_uploader("Pilih file audio", type=["mp3", "wav"])

    if uploaded_file is not None:
        st.write('File yang diunggah:', uploaded_file.name)
        
        if st.button('Kompresi'):
            compressed_audio = compress_audio(uploaded_file.getvalue())
            
            compressed_audio_bytes = compressed_audio.read()
            
            st.audio(compressed_audio_bytes, format='audio/mp3', start_time=0)
            
            st.download_button(
                label="Unduh Audio Kompresi",
                data=compressed_audio_bytes,
                file_name="compressed_audio.mp3",
                mime="audio/mp3"
            )
            
            st.success("Kompresi audio berhasil!")
