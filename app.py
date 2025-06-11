from flask import Flask, render_template, request, session, jsonify, send_file
import google.generativeai as genai
import os
from gtts import gTTS
import io
import speech_recognition as sr
from flask_cors import CORS

app = Flask(__name__)
#app.secret_key = os.environ.get('SECRET_KEY')
app.secret_key = 'IL4LbtIP4r'

CORS(app)  # Permite solicitudes desde cualquier origen

# Configuración de Gemini
GOOGLE_API_KEY = os.environ.get(
    'GEMINI_API_KEY', 'AIzaSyBNon2WMYLCQgyQWcoK8R_dzM3w1Cgc6Tw')  # Reemplaza con tu clave real
genai.configure(api_key=GOOGLE_API_KEY)

def get_chat_session():
    if 'chat' not in session:
        model = genai.GenerativeModel('gemini-2.0-flash')
        session['chat'] = model.start_chat(history=[]).history
    return genai.GenerativeModel('gemini-2.0-flash').start_chat(history=session['chat'])

@app.route('/')
def home():
    return render_template('asistente.html')

@app.route('/api/chat', methods=['POST'])
def chat_handler():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"status": "error", "message": "Mensaje vacío"}), 400
            
        chat = get_chat_session()
        response = chat.send_message(
            f"Responde como asistente de voz virtual usando texto plano sin formato. "
            f"Evita Markdown, HTML, listas con viñetas o símbolos especiales. "
            f"Pregunta: {user_message}"
        )
        
        # Almacenar la última respuesta en la sesión
        session['last_response'] = response.text
        
        # Convertir respuesta a audio
        tts = gTTS(text=response.text, lang='es')
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        
        return jsonify({
            "response": response.text,
            "status": "success",
            "audio_url": "/api/audio_response"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/audio_response', methods=['GET'])
def audio_response():
    try:
        # Obtener la última respuesta de la sesión
        last_response = session.get('last_response', 'No hay respuesta disponible')
        
        tts = gTTS(text=last_response, lang='es')
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        
        return send_file(
            audio_file,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='respuesta.mp3'
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({"status": "error", "message": "No se recibió audio"}), 400
            
        audio_file = request.files['audio']
        
        # Verificar que el archivo tenga un nombre y extensión
        if audio_file.filename == '':
            return jsonify({"status": "error", "message": "Archivo de audio no válido"}), 400
        
        # Crear directorio temporal si no existe
        if not os.path.exists('temp'):
            os.makedirs('temp')
            
        temp_path = os.path.join("temp", "temp_audio.ogg")
        wav_path = os.path.join("temp", "temp_audio.wav")
        
        audio_file.save(temp_path)
        
        # Convertir a WAV
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(temp_path)
            audio.export(wav_path, format="wav")
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Error al convertir audio: {str(e)}"
            }), 400
            
        # Transcribir
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='es-ES')
        except sr.UnknownValueError:
            return jsonify({
                "status": "error",
                "message": "No se pudo entender el audio"
            }), 400
        except sr.RequestError as e:
            return jsonify({
                "status": "error",
                "message": f"Error en el servicio de reconocimiento: {str(e)}"
            }), 500
            
        # Eliminar archivos temporales
        try:
            os.remove(temp_path)
            os.remove(wav_path)
        except:
            pass
            
        return jsonify({"status": "success", "text": text})
        
    except Exception as e:
        # Limpiar archivos temporales si existen
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        if 'wav_path' in locals() and os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except:
                pass
            
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
