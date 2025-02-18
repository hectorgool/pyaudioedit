from pydub import AudioSegment, silence
import gc
import os
from typing import List, Optional
import tempfile

def detect_silences(audio: AudioSegment, silence_thresh: int, min_silence_len: int) -> List[tuple]:
    return silence.detect_silence(audio, silence_thresh=silence_thresh, min_silence_len=min_silence_len)

def adjust_speed(audio: AudioSegment, speed: float) -> AudioSegment:
    return audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed)
    })

def repeat_segment(audio: AudioSegment, num_repetitions: int, pause_duration: int) -> AudioSegment:
    pause = AudioSegment.silent(duration=pause_duration)
    return sum((audio + pause for _ in range(num_repetitions)), AudioSegment.empty())

def overlay_background_music(audio: AudioSegment, bg_music: AudioSegment, volume: int, fade_in: int, fade_out: int) -> AudioSegment:
    gc.collect()  # Liberar memoria antes de procesar
    
    volume_db = -60 + (volume * 6)
    bg_music = bg_music + volume_db
    bg_music_loop = bg_music[:len(audio)].fade_in(fade_in).fade_out(fade_out)
    return audio.overlay(bg_music_loop)

def load_audio(file_path: str) -> AudioSegment:
    gc.collect()  # Liberar memoria antes de cargar un archivo
    return AudioSegment.from_file(file_path, format="mp3")

def save_audio(audio: AudioSegment, file_path: str):
    audio.export(file_path, format="mp3")

def edit_audio(audio: AudioSegment, silence_thresh: int, min_silence_len: int, speed: float, num_repetitions: int, pause_duration: int) -> AudioSegment:
    gc.collect()  # Liberar memoria antes de procesar el audio
    silences = detect_silences(audio, silence_thresh, min_silence_len)
    edited_audio = AudioSegment.empty()
    last_end = 0
    
    for start, end in silences:
        segment = audio[last_end:start]
        processed_segment = adjust_speed(segment, speed)
        processed_segment = repeat_segment(processed_segment, num_repetitions, pause_duration)
        edited_audio += processed_segment
        last_end = end
    
    if last_end < len(audio):
        segment = audio[last_end:]
        processed_segment = adjust_speed(segment, speed)
        processed_segment = repeat_segment(processed_segment, num_repetitions, pause_duration)
        edited_audio += processed_segment
    
    gc.collect()
    return edited_audio

def process_audio(input_file: str, create_mp3_files: bool, background_music: Optional[str], 
                  silence_thresh: int, min_silence_len: int, speed: float, num_repetitions: int, 
                  pause_duration: int, affirmations_per_file: int, start_silence: int, end_silence: int, 
                  bg_fade_in: int, bg_fade_out: int, bg_volume: int, alias_edit_suffix: str):
    audio = load_audio(input_file)
    
    bg_music = None
    if background_music:
        bg_music = load_audio(background_music)
    
    start_silence_seg = AudioSegment.silent(duration=start_silence)
    end_silence_seg = AudioSegment.silent(duration=end_silence)

    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
        edited_audio = start_silence_seg
        for i in range(0, len(audio), 60000):  # Procesar en fragmentos de 60 segundos
            segment = audio[i:i+60000]
            processed_segment = edit_audio(segment, silence_thresh, min_silence_len, speed, num_repetitions, pause_duration)
            edited_audio += processed_segment
        edited_audio += end_silence_seg
        
        if bg_music:
            edited_audio = overlay_background_music(edited_audio, bg_music, bg_volume, bg_fade_in, bg_fade_out)
        
        save_audio(edited_audio, temp_file.name)
    
    file_name, file_extension = os.path.splitext(input_file)
    edited_file_name = f"{file_name}_{alias_edit_suffix}{file_extension}"
    os.rename(temp_file.name, edited_file_name)
    print(f"Archivo editado guardado como: {edited_file_name}")
    
    del edited_audio, audio, bg_music
    gc.collect()
