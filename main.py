import sys
import os
import pyaudioedit
import json

# Obtener la ruta del directorio donde se encuentra este script
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "audio_config.json")

# Función para cargar configuraciones desde un archivo JSON
def load_config(json_path):
    with open(json_path, 'r') as config_file:
        return json.load(config_file)

def main():
    if not os.path.exists(config_path):
        print(f"Error: No se encontró el archivo de configuración {config_path}")
        return
    
    config = load_config(config_path)

    if len(sys.argv) < 2:
        print("Por favor, proporciona el nombre del archivo .mp3 a editar como argumento.")
        return

    input_file = sys.argv[1]
    create_mp3_files = False
    background_music = None

    if len(sys.argv) > 2:
        if sys.argv[2].lower() == config["SWITCH_CREATE_MP3_FILES"]:
            create_mp3_files = True
        elif len(sys.argv) > 3 and sys.argv[3].lower() == config["SWITCH_CREATE_MP3_FILES"]:
            background_music = sys.argv[2]
            create_mp3_files = True
        else:
            background_music = sys.argv[2]

    # Llamada a la función de procesamiento con los valores desde el archivo JSON
    pyaudioedit.process_audio(
        input_file=input_file,
        create_mp3_files=create_mp3_files,
        background_music=background_music,
        silence_thresh=-50,
        min_silence_len=config["SILENCE_MILLISECONDS"],
        speed=config["SPEED_REPRODUCTION"],
        num_repetitions=config["NUM_REPETITIONS"],
        pause_duration=config["PAUSE_MILLISECONDS"],
        affirmations_per_file=config["AFFIRMATIONS_PER_AUDIO_FILE"],
        start_silence=config["START_SILENCE"],
        end_silence=config["END_SILENCE"],
        bg_fade_in=config["AUDIO_BACKGROUND_FADE_IN"],
        bg_fade_out=config["AUDIO_BACKGROUND_FADE_OUT"],
        bg_volume=config["VOLUME_BACKGROUND"],
        alias_edit_suffix=config["ALIAS_EDIT_SUFFIX"]
    )

if __name__ == "__main__":
    main()

# example usage: 
# python3 main.py 45abundancia.mp3 delta_25m.mp3
