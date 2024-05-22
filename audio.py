from pydub import AudioSegment
import speech_recognition as sr

# Ruta del archivo MP3
audio_file_path = "C:/Users/Gaboo/OneDrive/Escritorio/audios/test.mp3"
converted_file_path = "C:/Users/Gaboo/OneDrive/Escritorio/audios/test.wav"

# Convertir MP3 a WAV
audio = AudioSegment.from_mp3(audio_file_path)
audio.export(converted_file_path, format="wav")

# Inicializar el reconocedor
recognizer = sr.Recognizer()

# Transcribir el archivo de audio
with sr.AudioFile(converted_file_path) as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data, language="es-ES")

print(text)