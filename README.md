# Procesador de Audio

Este script de Python procesa archivos de audio MP3, aplicando varias transformaciones como detección de silencios, ajuste de velocidad, repetición de segmentos y superposición de música de fondo.

## Características

- Detección y división de audio basada en silencios
- Ajuste de velocidad de reproducción
- Repetición de segmentos de audio
- Superposición de música de fondo (opcional)
- Procesamiento en modo de archivo único o múltiples archivos

## Requisitos

- Python 3.6+
- pydub

## Instalación

1. Clona este repositorio o descarga el script.
2. Instala las dependencias:

```
pip install pydub
```

## Uso

Ejecuta el script desde la línea de comandos:

```
python background.py <archivo_entrada.mp3> [archivo_fondo.mp3] [m]
```

- `<archivo_entrada.mp3>`: El archivo de audio MP3 que deseas procesar (obligatorio).
- `[archivo_fondo.mp3]`: Archivo de música de fondo MP3 (opcional).
- `[m]`: Agrega este flag para crear múltiples archivos MP3 de salida (opcional).

## Configuración

Puedes ajustar las siguientes constantes al principio del script:

- `SILENCE_MILLISECONDS`: Duración mínima de silencio para dividir el audio (500 ms por defecto).
- `NUM_REPETITIONS`: Número de repeticiones de cada segmento de audio (9 por defecto).
- `PAUSE_MILLISECONDS`: Pausa entre repeticiones (4000 ms por defecto).
- `SPEED_REPRODUCTION`: Velocidad de reproducción (0.8 por defecto, rango 0.5 a 2.0).
- `AFFIRMATIONS_PER_AUDIO_FILE`: Número de segmentos por archivo en modo múltiple (15 por defecto).
- `START_SILENCE`: Silencio al inicio de cada archivo (3000 ms por defecto).
- `END_SILENCE`: Silencio al final de cada archivo (3000 ms por defecto).
- `AUDIO_BACKGROUND_FADE_IN`: Duración del fade-in para el audio de fondo (2000 ms por defecto).
- `AUDIO_BACKGROUND_FADE_OUT`: Duración del fade-out para el audio de fondo (2000 ms por defecto).
- `VOLUME_BACKGROUND`: Volumen del audio de fondo (2 por defecto, rango 0 a 10).

## Estructura del Código

El código sigue los principios SOLID:

- **Single Responsibility Principle**: Cada clase tiene una única responsabilidad.
- **Open/Closed Principle**: Las clases están abiertas para extensión pero cerradas para modificación.
- **Liskov Substitution Principle**: Las subclases pueden ser sustituidas por sus clases base.
- **Interface Segregation Principle**: Se utilizan interfaces pequeñas y específicas.
- **Dependency Inversion Principle**: Las dependencias se invierten mediante inyección de dependencias.

### Clases Principales

- `AudioProcessor`: Clase base abstracta para procesadores de audio.
- `SilenceDetector`: Detecta silencios en el audio.
- `SpeedAdjuster`: Ajusta la velocidad de reproducción del audio.
- `Repeater`: Repite segmentos de audio.
- `BackgroundMusicOverlay`: Superpone música de fondo.
- `AudioFileHandler`: Maneja la carga y guardado de archivos de audio.
- `AudioEditor`: Coordina el proceso de edición de audio.
- `AudioBatchProcessor`: Procesa lotes de audio, ya sea en un solo archivo o en múltiples.

## Licencia

[Incluir información de licencia aquí]

## Contribuciones

[Instrucciones para contribuir al proyecto]

## Contacto

[Información de contacto o enlaces a perfiles relevantes]