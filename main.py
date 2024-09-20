from pydub import AudioSegment, silence
import sys
import os
import gc
from abc import ABC, abstractmethod
from typing import List, Optional

# Clase base abstracta para todos los procesadores de audio
class AudioProcessor(ABC):
    @abstractmethod
    def process(self, audio: AudioSegment) -> AudioSegment:
        # Método abstracto que debe ser implementado por las subclases
        pass

# Clase para detectar y dividir el audio en segmentos basados en silencios
class SilenceDetector:
    def __init__(self, silence_thresh: int, min_silence_len: int):
        self.silence_thresh = silence_thresh  # Umbral de silencio en dB
        self.min_silence_len = min_silence_len  # Duración mínima del silencio en ms

    def detect_silences(self, audio: AudioSegment) -> List[AudioSegment]:
        # Divide el audio en segmentos basados en silencios detectados
        return silence.split_on_silence(audio, silence_thresh=self.silence_thresh, min_silence_len=self.min_silence_len)

# Clase para ajustar la velocidad de reproducción del audio
class SpeedAdjuster(AudioProcessor):
    def __init__(self, speed: float):
        self.speed = speed  # Factor de velocidad (e.g., 0.8 para 80% de la velocidad original)

    def process(self, audio: AudioSegment) -> AudioSegment:
        # Ajusta la velocidad de reproducción del audio
        return audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * self.speed)
        })

# Clase para repetir segmentos de audio con pausas entre repeticiones
class Repeater(AudioProcessor):
    def __init__(self, num_repetitions: int, pause_duration: int):
        self.num_repetitions = num_repetitions  # Número de veces que se repite cada segmento
        self.pause = AudioSegment.silent(duration=pause_duration)  # Silencio entre repeticiones

    def process(self, audio: AudioSegment) -> AudioSegment:
        # Repite el segmento de audio el número especificado de veces, con pausas entre repeticiones
        repeated_audio = AudioSegment.empty()
        for _ in range(self.num_repetitions):
            repeated_audio += audio + self.pause
        return repeated_audio

# Clase para superponer música de fondo al audio principal
class BackgroundMusicOverlay(AudioProcessor):
    def __init__(self, bg_music: AudioSegment, volume: int, fade_in: int, fade_out: int):
        self.bg_music = bg_music  # Audio de fondo
        self.volume = volume  # Volumen del audio de fondo (0-10)
        self.fade_in = fade_in  # Duración del fade in en ms
        self.fade_out = fade_out  # Duración del fade out en ms

    def process(self, audio: AudioSegment) -> AudioSegment:
        # Ajusta el volumen y superpone la música de fondo al audio principal
        volume_db = -30 + (self.volume * 3)  # Mapea 0-10 a -30dB a 0dB
        bg_music = self.bg_music + volume_db
        bg_music_loop = bg_music * (len(audio) // len(bg_music) + 1)
        bg_music_loop = bg_music_loop[:len(audio)]
        bg_music_loop = bg_music_loop.fade_in(self.fade_in).fade_out(self.fade_out)
        return audio.overlay(bg_music_loop)

# Clase para manejar la carga y guardado de archivos de audio
class AudioFileHandler:
    @staticmethod
    def load_audio(file_path: str) -> AudioSegment:
        # Carga un archivo de audio MP3
        return AudioSegment.from_file(file_path, format="mp3")

    @staticmethod
    def save_audio(audio: AudioSegment, file_path: str):
        # Guarda un AudioSegment como archivo MP3
        audio.export(file_path, format="mp3")

# Clase principal para editar audio
class AudioEditor:
    def __init__(self, silence_detector: SilenceDetector, processors: List[AudioProcessor]):
        self.silence_detector = silence_detector
        self.processors = processors

    def edit_audio(self, audio: AudioSegment) -> AudioSegment:
        # Procesa el audio: detecta silencios, divide en segmentos y aplica los procesadores
        segments = self.silence_detector.detect_silences(audio)
        edited_audio = AudioSegment.empty()
        for segment in segments:
            processed_segment = segment
            for processor in self.processors:
                processed_segment = processor.process(processed_segment)
            edited_audio += processed_segment
        return edited_audio

# Clase para procesar audio en lotes (single file o multiple files)
class AudioBatchProcessor:
    def __init__(self, editor: AudioEditor, file_handler: AudioFileHandler, 
                 start_silence: int, end_silence: int, affirmations_per_file: int):
        self.editor = editor
        self.file_handler = file_handler
        self.start_silence = AudioSegment.silent(duration=start_silence)
        self.end_silence = AudioSegment.silent(duration=end_silence)
        self.affirmations_per_file = affirmations_per_file

    def process_audio(self, input_file: str, create_mp3_files: bool, background_music: Optional[str] = None):
        # Procesa el audio de entrada, opcionalmente con música de fondo y en modo de múltiples archivos
        audio = self.file_handler.load_audio(input_file)
        
        if background_music:
            bg_music = self.file_handler.load_audio(background_music)
            self.editor.processors.append(BackgroundMusicOverlay(bg_music, VOLUME_BACKGROUND, AUDIO_BACKGROUND_FADE_IN, AUDIO_BACKGROUND_FADE_OUT))

        if create_mp3_files:
            self._process_multiple_files(audio, input_file)
        else:
            self._process_single_file(audio, input_file)

    def _process_multiple_files(self, audio: AudioSegment, input_file: str):
        # Procesa el audio y lo divide en múltiples archivos
        segments = self.editor.silence_detector.detect_silences(audio)
        total_segments = len(segments)
        for i in range(0, total_segments, self.affirmations_per_file):
            sub_audio = self.start_silence
            for segment in segments[i:i+self.affirmations_per_file]:
                sub_audio += self.editor.edit_audio(segment)
            sub_audio += self.end_silence
            
            file_name, file_extension = os.path.splitext(input_file)
            edited_file_name = f"{file_name}_{ALIAS_EDIT_SUFFIX}_{(i // self.affirmations_per_file) + 1}{file_extension}"
            self.file_handler.save_audio(sub_audio, edited_file_name)
            print(f"Archivo editado guardado como: {edited_file_name}")
            
            del sub_audio
            gc.collect()

    def _process_single_file(self, audio: AudioSegment, input_file: str):
        # Procesa el audio y lo guarda como un único archivo
        edited_audio = self.start_silence + self.editor.edit_audio(audio) + self.end_silence
        
        file_name, file_extension = os.path.splitext(input_file)
        edited_file_name = f"{file_name}_{ALIAS_EDIT_SUFFIX}{file_extension}"
        self.file_handler.save_audio(edited_audio, edited_file_name)
        print(f"Archivo editado guardado como: {edited_file_name}")

# Configuración
SILENCE_MILLISECONDS = 500  # Duración mínima de silencio para dividir el audio
NUM_REPETITIONS = 9  # Número de repeticiones de cada segmento de audio
PAUSE_MILLISECONDS = 4000  # Duración de la pausa entre repeticiones
SPEED_REPRODUCTION = 0.8  # Factor de velocidad de reproducción
AFFIRMATIONS_PER_AUDIO_FILE = 15  # Número de segmentos por archivo en modo múltiple
START_SILENCE = 3000  # Duración del silencio al inicio de cada archivo
END_SILENCE = 3000  # Duración del silencio al final de cada archivo
AUDIO_BACKGROUND_FADE_IN = 2000  # Duración del fade-in para el audio de fondo
AUDIO_BACKGROUND_FADE_OUT = 2000  # Duración del fade-out para el audio de fondo
VOLUME_BACKGROUND = 3  # Volumen del audio de fondo (rango: 0 a 10)
SWITCH_CREATE_MP3_FILES = "m"  # Flag para activar el modo de múltiples archivos
ALIAS_EDIT_SUFFIX = "ed"  # Sufijo para los archivos editados

if __name__ == "__main__":
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

        # Configura y ejecuta el procesamiento de audio
        silence_detector = SilenceDetector(-50, SILENCE_MILLISECONDS)
        processors = [
            SpeedAdjuster(SPEED_REPRODUCTION),
            Repeater(NUM_REPETITIONS, PAUSE_MILLISECONDS)
        ]
        editor = AudioEditor(silence_detector, processors)
        file_handler = AudioFileHandler()
        batch_processor = AudioBatchProcessor(editor, file_handler, START_SILENCE, END_SILENCE, AFFIRMATIONS_PER_AUDIO_FILE)
        
        batch_processor.process_audio(input_file, create_mp3_files, background_music)