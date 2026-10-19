import os

EXTENSIONES_IMAGEN = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".ase",
    ".gif",
    ".bmp",
    ".tiff",
    ".svg",
)


def renombrar_imagenes_strip(directorio_base):
    archivos_renombrados = 0

    for ruta_actual, carpetas, archivos in os.walk(directorio_base):
        for archivo in archivos:
            if archivo.lower().endswith(EXTENSIONES_IMAGEN):
                if "Strip" in archivo:
                    nuevo_nombre = archivo.replace("Strip", "strip")

                    ruta_original = os.path.join(ruta_actual, archivo)
                    ruta_nueva = os.path.join(ruta_actual, nuevo_nombre)

                    try:
                        os.rename(ruta_original, ruta_nueva)
                        print(f"[RENOMBRADO] {archivo} ahora con strip.")
                        print(
                            f" En la carpeta: {os.path.relpath(ruta_actual, directorio_base)}\n"
                        )
                        archivos_renombrados += 1
                    except Exception as e:
                        print(f"[ERROR DE COMPATIBILIDAD] No se puede renombrar; {archivo}: {e}")

    print("-" * 50)
    print(f"Se renombraron un total de: {archivos_renombrados}"
    )


if __name__ == "__main__":
    
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    renombrar_imagenes_strip(directorio_actual)