import subprocess

def translate_text(input_text):
    """
    Construye el prompt para traducir el fragmento de texto y llama al modelo gemma3:4b mediante Ollama.
    Se envía el prompt por entrada estándar.
    """
    prompt = (
        "Please accurately translate the following text from English to Spanish without summarizing. "
        "Please preserve the Markdown formatting. "
        "Translate all the content to Spanish:\n\n" + input_text
    )
    
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma3:4b"],
            input=prompt,               # Se envía el prompt vía stdin
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el modelo:", e.stderr)
        return None

    return result.stdout

def main():
    # Intentamos leer el archivo de entrada
    try:
        with open("texto_2.md", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("No se encontró el archivo 'texto_2.md'. Verifica la ruta y el nombre.")
        return

    translated_parts = []
    chunk_size = 50  # Número de líneas por bloque
    total_lines = len(lines)

    # Procesamos el archivo en bloques de 50 líneas
    for i in range(0, total_lines, chunk_size):
        chunk = lines[i:i+chunk_size]
        chunk_text = ''.join(chunk)
        print(f"Translating lines {i+1} to {min(i+chunk_size, total_lines)}...")
        
        translation = translate_text(chunk_text)
        if translation is None:
            print(f"Error en la traducción del bloque de líneas {i+1} a {min(i+chunk_size, total_lines)}")
            return
        
        translated_parts.append(translation)
    
    # Unimos todas las traducciones en un solo texto
    final_translation = "\n".join(translated_parts)
    
    # Guardamos la traducción completa en un archivo de salida
    with open("texto_spanish.md", "w", encoding="utf-8") as f:
        f.write(final_translation)
    
    print("La traducción se completó exitosamente y se guardó en 'texto_spanish.md'.")

if __name__ == "__main__":
    main()
