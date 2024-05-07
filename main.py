import streamlit as st
from PIL import Image
from pydub import AudioSegment
from io import BytesIO
import os

# Fungsi untuk melakukan kompresi gambar
def compress_image(image, quality):
    img = image.copy()
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()

# Fungsi untuk melakukan kompresi audio
def compress_audio(audio_bytes, bitrate='64k'):
    audio_buf = BytesIO(audio_bytes)
    audio_buf.seek(0) 
    try:
        audio = AudioSegment.from_file(audio_buf, format="mp3")
        compressed_audio_buf = BytesIO()
        audio.export(compressed_audio_buf, format="mp3", bitrate=bitrate)
        return compressed_audio_buf.getvalue()
    except Exception as e:
        st.error(f"Error: {e}")


# Fungsi untuk menampilkan tombol unduh
def download_button(image_bytes, file_name):
    st.download_button(
        label="Unduh Gambar Kompresi",
        data=image_bytes,
        file_name=file_name,
        mime="image/jpeg"
    )

# Navigasi sidebar
with st.sidebar:
    selected = st.selectbox('Kompresi Gambar & Audio',
                            ['Beranda','Kompresi Gambar', 'Kompresi Audio'])

if selected == 'Beranda':
    st.title('Selamat Datang di Kompresi Gambar dan Audio!')
    
# Halaman kompresi gambar
if selected == 'Kompresi Gambar':
    st.title("Kompresi Gambar")
    st.write("Muat gambar dan kompres dengan kualitas tertentu.")

    uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar Asli", use_column_width=True)

        # Slider untuk memilih kualitas kompresi
        quality = st.slider("Kualitas Kompresi (0-100)", 0, 100, 50)

        if st.button("Kompresi"):
            compressed_image = compress_image(image, quality)
            st.image(compressed_image, caption="Gambar Setelah Kompresi", use_column_width=True)
            st.success("Gambar berhasil dikompresi!")
            download_button(compressed_image, "compressed_image.jpg")

# Halaman kompresi audio
if selected == 'Kompresi Audio':
    st.title('Kompresi Audio')
    st.write("Muat audio dan kompres dengan kualitas tertentu.")

    uploaded_file = st.file_uploader("Pilih file audio", type=["mp3", "wav"], accept_multiple_files=False)

    if uploaded_file is not None:
        st.write('File yang diunggah:', uploaded_file.name)
        
        if st.button('Kompresi'):
            compressed_audio = compress_audio(uploaded_file.getvalue())
            if compressed_audio:
                st.audio(compressed_audio, format='audio/mp3', start_time=0)
                
                st.download_button(
                    label="Unduh Audio Kompresi",
                    data=compressed_audio,
                    file_name="compressed_audio.mp3",
                    mime="audio/mp3"
                )
                st.success("Kompresi audio berhasil!")
