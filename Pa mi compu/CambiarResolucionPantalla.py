import ctypes
import os
import sys
import time

# Flags requeridos para forzar el modo exclusivo tipo videojuego
CDS_FULLSCREEN = 0x00000004
DISP_CHANGE_SUCCESSFUL = 0

DM_PELSWIDTH = 0x00080000
DM_PELSHEIGHT = 0x00100000
DM_DISPLAYFREQUENCY = 0x00400000


class DEVMODE(ctypes.Structure):
  _fields_ = [
      ("dmDeviceName", ctypes.c_wchar * 32),
      ("dmSpecVersion", ctypes.c_ushort),
      ("dmDriverVersion", ctypes.c_ushort),
      ("dmSize", ctypes.c_ushort),
      ("dmDriverExtra", ctypes.c_ushort),
      ("dmFields", ctypes.c_ulong),
      ("dmPositionX", ctypes.c_long),
      ("dmPositionY", ctypes.c_long),
      ("dmDisplayOrientation", ctypes.c_ulong),
      ("dmDisplayFixedOutput", ctypes.c_ulong),
      ("dmColor", ctypes.c_short),
      ("dmDuplex", ctypes.c_short),
      ("dmYResolution", ctypes.c_short),
      ("dmTTOption", ctypes.c_short),
      ("dmCollation", ctypes.c_short),
      ("dmFormName", ctypes.c_wchar * 32),
      ("dmLogPixels", ctypes.c_ushort),
      ("dmBitsPerPel", ctypes.c_ulong),
      ("dmPelsWidth", ctypes.c_ulong),
      ("dmPelsHeight", ctypes.c_ulong),
      ("dmDisplayFlags", ctypes.c_ulong),
      ("dmDisplayFrequency", ctypes.c_ulong),
      ("dmICMMaxValue", ctypes.c_ulong),
      ("dmICMIntent", ctypes.c_ulong),
      ("dmMediaType", ctypes.c_ulong),
      ("dmPanningWidth", ctypes.c_ulong),
      ("dmPanningHeight", ctypes.c_ulong),
  ]


def es_administrador():
  try:
    return ctypes.windll.shell32.IsUserAnAdmin()
  except:
    return False


def cambiar_resolucion_estilo_juego(ancho, alto, hz):
  devmode = DEVMODE()
  devmode.dmSize = ctypes.sizeof(DEVMODE)
  devmode.dmPelsWidth = ancho
  devmode.dmPelsHeight = alto
  devmode.dmDisplayFrequency = hz
  devmode.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT | DM_DISPLAYFREQUENCY

  # Aplicamos utilizando el modo exclusivo tipo pantalla completa de juegos
  resultado = ctypes.windll.user32.ChangeDisplaySettingsW(
      ctypes.byref(devmode), CDS_FULLSCREEN
  )
  time.sleep(0.5)

  if resultado == DISP_CHANGE_SUCCESSFUL:
    print(
        f"\n[ÉXITO] Resolución cambiada a {ancho}x{alto} @ {hz}Hz (Modo"
        " Exclusivo)."
    )
  else:
    print(
        f"\n[AVISO] Windows devolvió el código de error: {resultado}. Es"
        " posible que el driver gráfico de Ghost Spectre no permita esta"
        " frecuencia."
    )


def main():
  if not es_administrador():
    print(
        "[!] ATENCIÓN: Este script requiere privilegios de Administrador para"
        " forzar resoluciones en Windows 11."
    )
    print(
        "[!] Por favor, vuelve a abrir la terminal haciendo clic derecho y"
        " selecciona 'Ejecutar como administrador'."
    )
    input("\nPresiona ENTER para salir...")
    sys.exit()

  resoluciones_preset = [
      ("1360x768 (Nativa Ideal) - 60Hz", 1360, 768, 60),
      ("1360x768 (Nativa Máxima) - 75Hz", 1360, 768, 75),
      ("1280x800 - 60Hz", 1280, 800, 60),
      ("1280x768 - 60Hz", 1280, 768, 60),
      ("1280x768 - 75Hz", 1280, 768, 75),
      ("1280x720 (HD) - 60Hz", 1280, 720, 60),
      ("1024x768 (4:3) - 60Hz", 1024, 768, 60),
      ("1024x768 (4:3) - 75Hz", 1024, 768, 75),
  ]

  opcion_personalizada = len(resoluciones_preset) + 1

  while True:
    os.system("cls" if os.name == "nt" else "clear")
    print("=== Cambiador de Resolución Estilo Videojuego (Ghost Spectre Fix) ===")

    for i, (nombre, _, _, _) in enumerate(resoluciones_preset, 1):
      print(f" {i}. {nombre}")

    print(f" {opcion_personalizada}. Personalizado (Ancho, Alto y Hz)")
    print(" 0. Salir")

    opcion = input(
        f"\nSelecciona una opción (0-{opcion_personalizada}): "
    ).strip()

    if opcion == "0":
      print("Saliendo...")
      break

    if opcion.isdigit():
      num = int(opcion)

      if 1 <= num <= len(resoluciones_preset):
        _, ancho, alto, hz = resoluciones_preset[num - 1]
        print(f"\nForzando pantalla completa a {ancho}x{alto} a {hz}Hz...")
        cambiar_resolucion_estilo_juego(ancho, alto, hz)
        input("\nPresiona ENTER para volver al menú...")

      elif num == opcion_personalizada:
        print("\n--- Modo Personalizado ---")
        input_ancho = input("Ingresa el Ancho (ej. 1360): ").strip()
        input_alto = input("Ingresa el Alto (ej. 768): ").strip()
        input_hz = input("Ingresa los Hz (ej. 60 o 75): ").strip()

        if (
            input_ancho.isdigit()
            and input_alto.isdigit()
            and input_hz.isdigit()
        ):
          cambiar_resolucion_estilo_juego(
              int(input_ancho), int(input_alto), int(input_hz)
          )
        else:
          print("\n[Error] Debes ingresar valores numéricos válidos.")
        input("\nPresiona ENTER para volver al menú...")
      else:
        print("\n[Aviso] Opción fuera de rango.")
        time.sleep(1.5)
    else:
      print("\n[Aviso] Entrada no válida.")
      time.sleep(1.5)


if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(f"\n[ERROR CRÍTICO]: {e}")
    input("\nEl programa se detuvo. Presiona ENTER para salir...")
