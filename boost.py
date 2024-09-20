from pydub import AudioSegment, silence
import sys
import os

# Constantes configurables
SILENCE_MILLISECONDS = 200  # Duración de la pausa para dividir el audio
NUM_REPETITIONS = 10  # Número de repeticiones de cada fragmento de audio
PAUSE_MILLISECONDS = 5000  # Pausa entre la repetición de cada fragmento
SPEED_REPRODUCTION = 0.8  # Velocidad de reproducción (rango permitido: 0.5 a 2.0)
NUM_AFFIRMATIONS = 15  # Número de fragmentos por archivo si CREATE_MP3_FILES está activado
SWITCH_CREATE_MP3_FILES = "m"

def process_audio(file_path, create_mp3_files):
    # Cargar el archivo de audio
    audio = AudioSegment.from_file(file_path, format="mp3")
    
    # Detectar silencios y dividir el audio en fragmentos
    segments = silence.split_on_silence(audio, silence_thresh=-50, min_silence_len=SILENCE_MILLISECONDS)
    
    # Crear un nuevo segmento de audio editado
    edited_audio = AudioSegment.empty()
    
    # Crear una pausa de la duración especificada
    pause_segment = AudioSegment.silent(duration=PAUSE_MILLISECONDS)

    # Generar el nombre base del archivo de salida
    file_name, file_extension = os.path.splitext(file_path)
    
    if create_mp3_files:
        # Procesar en grupos de NUM_AFFIRMATIONS
        total_segments = len(segments)
        for i in range(0, total_segments, NUM_AFFIRMATIONS):
            # Crear un nuevo segmento para cada archivo
            sub_audio = AudioSegment.empty()
            
            # Repetir cada fragmento dentro del grupo
            for j in range(i, min(i + NUM_AFFIRMATIONS, total_segments)):
                for _ in range(NUM_REPETITIONS):
                    # Cambiar la velocidad de reproducción
                    repeated_segment = segments[j]._spawn(segments[j].raw_data, overrides={
                        "frame_rate": int(segments[j].frame_rate * SPEED_REPRODUCTION)
                    })
                    sub_audio += repeated_segment + pause_segment

            # Guardar el archivo editado por grupos
            edited_file_name = f"{file_name}_edit_{(i // NUM_AFFIRMATIONS) + 1}{file_extension}"
            sub_audio.export(edited_file_name, format="mp3")
            print(f"Archivo editado guardado como: {edited_file_name}")
    else:
        # Repetir cada fragmento de audio según NUM_REPETITIONS
        for segment in segments:
            for _ in range(NUM_REPETITIONS):
                # Cambiar la velocidad de reproducción
                repeated_segment = segment._spawn(segment.raw_data, overrides={
                    "frame_rate": int(segment.frame_rate * SPEED_REPRODUCTION)
                })
                edited_audio += repeated_segment + pause_segment

        # Guardar el archivo completo editado
        ALIAS_EDIT = f"{file_name}_edit{file_extension}"
        edited_audio.export(ALIAS_EDIT, format="mp3")
        print(f"Archivo editado guardado como: {ALIAS_EDIT}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporciona el nombre del archivo .mp3 a editar como argumento.")
    else:
        input_file = sys.argv[1]
        CREATE_MP3_FILES = len(sys.argv) > 2 and sys.argv[2].lower() == SWITCH_CREATE_MP3_FILES
        process_audio(input_file, CREATE_MP3_FILES)
