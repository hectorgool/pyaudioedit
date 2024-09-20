from pydub import AudioSegment, silence
import sys
import os
import gc

# Constantes configurables
SILENCE_MILLISECONDS = 500  # Duración de la pausa para dividir el audio
NUM_REPETITIONS = 9  # Número de repeticiones de cada fragmento de audio
PAUSE_MILLISECONDS = 4000  # Pausa entre la repetición de cada fragmento
SPEED_REPRODUCTION = 0.8  # Velocidad de reproducción (rango permitido: 0.5 a 2.0)
AFFIRMATIONS_PER_AUDIO_FILE = 15  # Número de fragmentos por archivo si CREATE_MP3_FILES está activado
START_SILENCE = 3000  # Silencio al inicio de cada archivo de audio
END_SILENCE = 3000  # Silencio al final de cada archivo de audio
AUDIO_BACKGROUND_FADE_IN = 2000  # Duración del fade-in para el audio de fondo
AUDIO_BACKGROUND_FADE_OUT = 2000  # Duración del fade-out para el audio de fondo
VOLUME_BACKGROUND = -9  # Volumen del audio de fondo (umbral permitido: -30 a 0 dB), estaba en: -15
SWITCH_CREATE_MP3_FILES = "m"
ALIAS_EDIT_SUFFIX = "ed"

def process_audio(file_path, create_mp3_files, background_music=None):
    # Load the audio file
    audio = AudioSegment.from_file(file_path, format="mp3")
    
    # Load the background music file if provided
    bg_music = None
    if background_music:
        bg_music = AudioSegment.from_file(background_music, format="mp3")
        bg_music = bg_music - abs(VOLUME_BACKGROUND)

    # Detect silences and split the audio into segments
    segments = silence.split_on_silence(audio, silence_thresh=-50, min_silence_len=SILENCE_MILLISECONDS)
    
    # Create silence segments
    start_silence_segment = AudioSegment.silent(duration=START_SILENCE)
    end_silence_segment = AudioSegment.silent(duration=END_SILENCE)
    pause_segment = AudioSegment.silent(duration=PAUSE_MILLISECONDS)

    # Generate the base name of the output file
    file_name, file_extension = os.path.splitext(file_path)
    
    if create_mp3_files:
        total_segments = len(segments)
        for i in range(0, total_segments, AFFIRMATIONS_PER_AUDIO_FILE):
            sub_audio = start_silence_segment

            for j in range(i, min(i + AFFIRMATIONS_PER_AUDIO_FILE, total_segments)):
                segment = segments[j]
                repeated_segment = segment._spawn(segment.raw_data, overrides={
                    "frame_rate": int(segment.frame_rate * SPEED_REPRODUCTION)
                })
                for _ in range(NUM_REPETITIONS):
                    sub_audio += repeated_segment + pause_segment
            
            sub_audio += end_silence_segment

            if bg_music:
                bg_music_loop = bg_music * (len(sub_audio) // len(bg_music) + 1)
                bg_music_loop = bg_music_loop[:len(sub_audio)]
                bg_music_loop = bg_music_loop.fade_in(AUDIO_BACKGROUND_FADE_IN).fade_out(AUDIO_BACKGROUND_FADE_OUT)
                sub_audio = sub_audio.overlay(bg_music_loop)

            edited_file_name = f"{file_name}_{ALIAS_EDIT_SUFFIX}_{(i // AFFIRMATIONS_PER_AUDIO_FILE) + 1}{file_extension}"
            sub_audio.export(edited_file_name, format="mp3")
            print(f"Archivo editado guardado como: {edited_file_name}")
            
            # Clear variables to free memory
            del sub_audio
            gc.collect()
    else:
        edited_audio = start_silence_segment

        for segment in segments:
            repeated_segment = segment._spawn(segment.raw_data, overrides={
                "frame_rate": int(segment.frame_rate * SPEED_REPRODUCTION)
            })
            for _ in range(NUM_REPETITIONS):
                edited_audio += repeated_segment + pause_segment
        
        edited_audio += end_silence_segment

        if bg_music:
            bg_music_loop = bg_music * (len(edited_audio) // len(bg_music) + 1)
            bg_music_loop = bg_music_loop[:len(edited_audio)]
            bg_music_loop = bg_music_loop.fade_in(AUDIO_BACKGROUND_FADE_IN).fade_out(AUDIO_BACKGROUND_FADE_OUT)
            edited_audio = edited_audio.overlay(bg_music_loop)

        ALIAS_EDIT = f"{file_name}_{ALIAS_EDIT_SUFFIX}{file_extension}"
        edited_audio.export(ALIAS_EDIT, format="mp3")
        print(f"Archivo editado guardado como: {ALIAS_EDIT}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporciona el nombre del archivo .mp3 a editar como argumento.")
    else:
        input_file = sys.argv[1]
        create_mp3_files = False
        background_music = None

        if len(sys.argv) > 2:
            if sys.argv[2].lower() == "m":
                create_mp3_files = True
            elif len(sys.argv) > 3 and sys.argv[3].lower() == SWITCH_CREATE_MP3_FILES:
                background_music = sys.argv[2]
                create_mp3_files = True
            else:
                background_music = sys.argv[2]

        process_audio(input_file, create_mp3_files, background_music)
