import sys
import pyaudioedit

# Configuración de parámetros para el procesamiento de audio
SILENCE_MILLISECONDS = 500
NUM_REPETITIONS = 3
PAUSE_MILLISECONDS = 5000
SPEED_REPRODUCTION = 0.9
AFFIRMATIONS_PER_AUDIO_FILE = 15
START_SILENCE = 2000
END_SILENCE = 2000
AUDIO_BACKGROUND_FADE_IN = 2000
AUDIO_BACKGROUND_FADE_OUT = 2000
VOLUME_BACKGROUND = 3
SWITCH_CREATE_MP3_FILES = "m"
ALIAS_EDIT_SUFFIX = "etsy"

def main():
    if len(sys.argv) < 2:
        print("Por favor, proporciona el nombre del archivo .mp3 a editar como argumento.")
        return

    input_file = sys.argv[1]
    create_mp3_files = False
    background_music = None

    if len(sys.argv) > 2:
        if sys.argv[2].lower() == SWITCH_CREATE_MP3_FILES:
            create_mp3_files = True
        elif len(sys.argv) > 3 and sys.argv[3].lower() == SWITCH_CREATE_MP3_FILES:
            background_music = sys.argv[2]
            create_mp3_files = True
        else:
            background_music = sys.argv[2]

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

if __name__ == "__main__":
    main()

#example
#python3 main.py 45abundancia.mp3 delta_25m.mp3