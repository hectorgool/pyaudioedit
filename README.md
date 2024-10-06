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

## Ejemplos de Uso

A continuación, se presentan algunos ejemplos de cómo usar el script con diferentes opciones y los resultados esperados:

### 1. Procesamiento básico de un archivo de audio

Comando:
```
python background.py input.mp3
```

Resultado esperado:
- Se creará un nuevo archivo llamado `input_ed.mp3`.
- El audio en `input_ed.mp3` tendrá las siguientes características:
  - Dividido en segmentos basados en silencios.
  - Cada segmento se reproducirá a 0.8x de la velocidad original.
  - Cada segmento se repetirá 9 veces con una pausa de 4 segundos entre repeticiones.
  - Habrá 3 segundos de silencio al inicio y al final del archivo.

### 2. Procesamiento con música de fondo

Comando:
```
python background.py input.mp3 background_music.mp3
```

Resultado esperado:
- Se creará un nuevo archivo llamado `input_ed.mp3`.
- El audio en `input_ed.mp3` tendrá las mismas características que en el ejemplo 1, pero además:
  - Se superpondrá la música de fondo de `background_music.mp3`.
  - La música de fondo tendrá un volumen reducido (nivel 2 de 10).
  - La música de fondo tendrá un fade-in de 2 segundos al inicio y un fade-out de 2 segundos al final.

### 3. Procesamiento en modo de múltiples archivos

Comando:
```
python background.py input.mp3 m
```

Resultado esperado:
- Se crearán múltiples archivos: `input_ed_1.mp3`, `input_ed_2.mp3`, etc.
- Cada archivo contendrá hasta 15 segmentos procesados (según el valor de `AFFIRMATIONS_PER_AUDIO_FILE`).
- Cada archivo tendrá las mismas características de procesamiento que en el ejemplo 1.

### 4. Procesamiento en modo de múltiples archivos con música de fondo

Comando:
```
python background.py input.mp3 background_music.mp3 m
```

Resultado esperado:
- Se crearán múltiples archivos: `input_ed_1.mp3`, `input_ed_2.mp3`, etc.
- Cada archivo tendrá las mismas características que en el ejemplo 3, pero además:
  - Incluirá la música de fondo de `background_music.mp3` con las características descritas en el ejemplo 2.

Nota: En todos los casos, el script mostrará mensajes en la consola indicando el progreso y los nombres de los archivos creados.