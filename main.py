import sys
import pyaudioedit

# Configuración de parámetros para el procesamiento de audio
SILENCE_MILLISECONDS = 500  # Duración mínima de silencio para dividir el audio
NUM_REPETITIONS = 3  # Número de repeticiones de cada segmento de audio
PAUSE_MILLISECONDS = 4000  # Duración de la pausa entre repeticiones
SPEED_REPRODUCTION = 0.9  # Factor de velocidad de reproducción
AFFIRMATIONS_PER_AUDIO_FILE = 15  # Número de segmentos por archivo en modo múltiple
START_SILENCE = 2000  # Duración del silencio al inicio de cada archivo
END_SILENCE = 2000  # Duración del silencio al final de cada archivo
AUDIO_BACKGROUND_FADE_IN = 2000  # Duración del fade-in para el audio de fondo
AUDIO_BACKGROUND_FADE_OUT = 2000  # Duración del fade-out para el audio de fondo
VOLUME_BACKGROUND = 3  # Volumen del audio de fondo (rango: 0 a 10)
SWITCH_CREATE_MP3_FILES = "m"  # Flag para activar el modo de múltiples archivos
ALIAS_EDIT_SUFFIX = "etsy"  # Sufijo para los archivos editados

def main():
    # Verifica si se proporcionó el nombre del archivo de entrada
    if len(sys.argv) < 2:
        print("Por favor, proporciona el nombre del archivo .mp3 a editar como argumento.")
    else:
        input_file = sys.argv[1]
        create_mp3_files = False
        background_music = None

        # Procesa los argumentos de la línea de comandos
        if len(sys.argv) > 2:
            if sys.argv[2].lower() == SWITCH_CREATE_MP3_FILES:
                create_mp3_files = True
            elif len(sys.argv) > 3 and sys.argv[3].lower() == SWITCH_CREATE_MP3_FILES:
                background_music = sys.argv[2]
                create_mp3_files = True
            else:
                background_music = sys.argv[2]

        # Llama a la función principal de procesamiento de audio
        pyaudioedit.process_audio(
            input_file=input_file,
            create_mp3_files=create_mp3_files,
            background_music=background_music,
            silence_thresh=-50,
            min_silence_len=SILENCE_MILLISECONDS,
            speed=SPEED_REPRODUCTION,
            num_repetitions=NUM_REPETITIONS,
            pause_duration=PAUSE_MILLISECONDS,
            affirmations_per_file=AFFIRMATIONS_PER_AUDIO_FILE,
            start_silence=START_SILENCE,
            end_silence=END_SILENCE,
            bg_fade_in=AUDIO_BACKGROUND_FADE_IN,
            bg_fade_out=AUDIO_BACKGROUND_FADE_OUT,
            bg_volume=VOLUME_BACKGROUND,
            alias_edit_suffix=ALIAS_EDIT_SUFFIX
        )

# Ejecuta la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()

#example
#python3 main.py 45abundancia.mp3 delta_25m.mp3