from pydub import AudioSegment, silence
import gc
import os
from typing import List, Optional

# Detecta silencios en el audio y lo divide en segmentos
def detect_silences(audio: AudioSegment, silence_thresh: int, min_silence_len: int) -> List[AudioSegment]:
    return silence.split_on_silence(audio, silence_thresh=silence_thresh, min_silence_len=min_silence_len)

# Ajusta la velocidad de reproducción del audio
def adjust_speed(audio: AudioSegment, speed: float) -> AudioSegment:
    return audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed)
    })

# Repite un segmento de audio un número específico de veces con pausas entre repeticiones
def repeat_segment(audio: AudioSegment, num_repetitions: int, pause_duration: int) -> AudioSegment:
    pause = AudioSegment.silent(duration=pause_duration)
    repeated_audio = AudioSegment.empty()
    for _ in range(num_repetitions):
        repeated_audio += audio + pause
    return repeated_audio

# Superpone música de fondo al audio principal
def overlay_background_music(audio: AudioSegment, bg_music: AudioSegment, volume: int, fade_in: int, fade_out: int) -> AudioSegment:
    volume_db = -30 + (volume * 3)  # Convierte el volumen de 0-10 a decibelios
    bg_music = bg_music + volume_db
    bg_music_loop = bg_music * (len(audio) // len(bg_music) + 1)
    bg_music_loop = bg_music_loop[:len(audio)]
    bg_music_loop = bg_music_loop.fade_in(fade_in).fade_out(fade_out)
    return audio.overlay(bg_music_loop)

# Carga un archivo de audio MP3
def load_audio(file_path: str) -> AudioSegment:
    return AudioSegment.from_file(file_path, format="mp3")

# Guarda un AudioSegment como archivo MP3
def save_audio(audio: AudioSegment, file_path: str):
    audio.export(file_path, format="mp3")

# Edita el audio: detecta silencios, ajusta la velocidad y repite segmentos
def edit_audio(audio: AudioSegment, silence_thresh: int, min_silence_len: int, speed: float, num_repetitions: int, pause_duration: int) -> AudioSegment:
    segments = detect_silences(audio, silence_thresh, min_silence_len)
    edited_audio = AudioSegment.empty()
    for segment in segments:
        processed_segment = adjust_speed(segment, speed)
        processed_segment = repeat_segment(processed_segment, num_repetitions, pause_duration)
        edited_audio += processed_segment
    return edited_audio

# Función principal para procesar el audio
def process_audio(input_file: str, create_mp3_files: bool, background_music: Optional[str], 
                  silence_thresh: int, min_silence_len: int, speed: float, num_repetitions: int, 
                  pause_duration: int, affirmations_per_file: int, start_silence: int, end_silence: int, 
                  bg_fade_in: int, bg_fade_out: int, bg_volume: int, alias_edit_suffix: str):
    audio = load_audio(input_file)
    
    if background_music:
        bg_music = load_audio(background_music)
    
    start_silence_seg = AudioSegment.silent(duration=start_silence)
    end_silence_seg = AudioSegment.silent(duration=end_silence)

    if create_mp3_files:
        _process_multiple_files(audio, input_file, silence_thresh, min_silence_len, speed, num_repetitions, 
                                pause_duration, affirmations_per_file, start_silence_seg, end_silence_seg, 
                                bg_music if background_music else None, bg_fade_in, bg_fade_out, bg_volume, alias_edit_suffix)
    else:
        _process_single_file(audio, input_file, silence_thresh, min_silence_len, speed, num_repetitions, 
                             pause_duration, start_silence_seg, end_silence_seg, 
                             bg_music if background_music else None, bg_fade_in, bg_fade_out, bg_volume, alias_edit_suffix)

# Procesa el audio y lo divide en múltiples archivos
def _process_multiple_files(audio: AudioSegment, input_file: str, silence_thresh: int, min_silence_len: int, 
                            speed: float, num_repetitions: int, pause_duration: int, affirmations_per_file: int, 
                            start_silence: AudioSegment, end_silence: AudioSegment, bg_music: Optional[AudioSegment], 
                            bg_fade_in: int, bg_fade_out: int, bg_volume: int, alias_edit_suffix: str):
    segments = detect_silences(audio, silence_thresh, min_silence_len)
    total_segments = len(segments)
    for i in range(0, total_segments, affirmations_per_file):
        sub_audio = start_silence
        for segment in segments[i:i+affirmations_per_file]:
            processed_segment = edit_audio(segment, silence_thresh, min_silence_len, speed, num_repetitions, pause_duration)
            sub_audio += processed_segment
        sub_audio += end_silence
        
        if bg_music:
            sub_audio = overlay_background_music(sub_audio, bg_music, bg_volume, bg_fade_in, bg_fade_out)
        
        file_name, file_extension = os.path.splitext(input_file)
        edited_file_name = f"{file_name}_{alias_edit_suffix}_{(i // affirmations_per_file) + 1}{file_extension}"
        save_audio(sub_audio, edited_file_name)
        print(f"Archivo editado guardado como: {edited_file_name}")
        
        del sub_audio
        gc.collect()

# Procesa el audio y lo guarda como un único archivo
def _process_single_file(audio: AudioSegment, input_file: str, silence_thresh: int, min_silence_len: int, 
                         speed: float, num_repetitions: int, pause_duration: int, start_silence: AudioSegment, 
                         end_silence: AudioSegment, bg_music: Optional[AudioSegment], bg_fade_in: int, 
                         bg_fade_out: int, bg_volume: int, alias_edit_suffix: str):
    edited_audio = start_silence + edit_audio(audio, silence_thresh, min_silence_len, speed, num_repetitions, pause_duration) + end_silence
    
    if bg_music:
        edited_audio = overlay_background_music(edited_audio, bg_music, bg_volume, bg_fade_in, bg_fade_out)
    
    file_name, file_extension = os.path.splitext(input_file)
    edited_file_name = f"{file_name}_{alias_edit_suffix}{file_extension}"
    save_audio(edited_audio, edited_file_name)
    print(f"Archivo editado guardado como: {edited_file_name}")