import numpy as np
from kokoro import KPipeline
import soundfile as sf
import torch
def main():
    input_file = "texto_spanish.md"
    output_file = "audio_output.wav"
    
    # Cargar el texto desde el archivo 'texto_spanish.md'
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo '{input_file}'. Verifica la ruta y el nombre.")
        return
    except Exception as e:
        print("Error al leer el archivo:", e)
        return

    # Crear el pipeline con el código de idioma en español
    pipeline = KPipeline(lang_code='es')  # Asegúrate de que lang_code coincida con la voz

    # Generar audio a partir del texto.
    # Si el texto es muy largo, el pipeline podría generar varios fragmentos.
    generator = pipeline(
        text,
        voice='ef_dora',  # Cambia la voz según tus preferencias
        speed=1,
        split_pattern=r'\n+'  # Separa por saltos de línea para evitar sobrecargar el modelo
    )

    audio_chunks = []
    for i, (gs, ps, audio) in enumerate(generator):
        print(f"Procesando segmento {i+1}...")
        audio_chunks.append(audio)

    if audio_chunks:
        # Concatenar todos los fragmentos de audio en uno solo
        combined_audio = np.concatenate(audio_chunks)
        
        # Guardar el audio en un único archivo WAV
        sf.write(output_file, combined_audio, 24000)
        print(f"El audio completo se guardó en '{output_file}'.")
    else:
        print("No se generó audio.")

if __name__ == "__main__":
    main()
