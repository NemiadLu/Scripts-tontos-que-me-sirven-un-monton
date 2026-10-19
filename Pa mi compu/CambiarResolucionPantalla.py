import ctypes
import os
import sys
import time

CDS_TEMPORARY = 0
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
      ("dmropic", ctypes.c_ulong),
      ("dmPanningWidth", ctypes.c_ulong),
      ("dmPanningHeight", ctypes.c_ulong),
  ]


def mostrar_mensaje(titulo, texto, tipo=0):
  icono = 0x10 if tipo == 16 else (0x40 if tipo == 64 else 0x0)
  ctypes.windll.user32.MessageBoxW(0, texto, titulo, 0x40000 | icono)


def cambiar_resolucion(ancho, alto, hz):
  devmode = DEVMODE()
  devmode.dmSize = ctypes.sizeof(DEVMODE)
  devmode.dmPelsWidth = ancho
  devmode.dmPelsHeight = alto
  devmode.dmDisplayFrequency = hz
  devmode.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT | DM_DISPLAYFREQUENCY

  resultado = ctypes.windll.user32.ChangeDisplaySettingsW(
      ctypes.byref(devmode), CDS_TEMPORARY
  )
  time.sleep(1)

  if resultado == DISP_CHANGE_SUCCESSFUL:
    mostrar_mensaje(
        "¡Éxito!",
        f"Resolución aplicada correctamente:\n-> {ancho}x{alto} a {hz}Hz",
        tipo=64,
    )
  else:
    mostrar_mensaje(
        "Error de Modo",
        f"Windows devolvió el código: {resultado}\n(El monitor sigue"
        " rechazando esta combinación exacta de Hz).",
        tipo=16,
    )


def main():
  resoluciones_preset = [
      ("1360x768 (Nativa Ideal) - 60Hz", 1360, 768, 60),
      ("1360x768 (Nativa Máxima) - 75Hz", 1360, 768, 75),
      ("1280x800 (Solicitada) - 60Hz", 1280, 800, 60),
      ("1280x768 (Solicitada) - 60Hz", 1280, 768, 60),
      ("1280x768 (Solicitada) - 75Hz", 1280, 768, 75),
      ("1280x720 (HD) - 60Hz", 1280, 720, 60),
      ("1024x768 (4:3) - 60Hz", 1024, 768, 60),
      ("1024x768 (4:3) - 75Hz", 1024, 768, 75),
  ]

  while True:
    os.system("cls" if os.name == "nt" else "clear")
    print("Cambiador Ideal - Basado en un LG Flatron W1642S (56-75Hz)")
    print("==========================================================")

    for i, (nombre, _, _, _) in enumerate(resoluciones_preset, 1):
      print(f" {i}. {nombre}")

    print(
        f" {len(resoluciones_preset) + 1}. Personalizado (Elegir Ancho, Alto y"
        " Hz)"
    )
    print(" 0. Salir")

    opcion = input(
        f"\nSelecciona una opción (0-{len(resoluciones_preset) + 1}): "
    ).strip()

    if opcion == "0":
      print("Saliendo...")
      break

    if opcion.isdigit():
      num = int(opcion)

      if 1 <= num <= len(resoluciones_preset):
        _, ancho, alto, hz = resoluciones_preset[num - 1]
        print(f"\nAplicando {ancho}x{alto} a {hz}Hz...")
        cambiar_resolucion(ancho, alto, hz)

      elif num == len(resoluciones_preset) + 1:
        print("\nModo Personalizado")
        input_ancho = input("Ingresa el Ancho (ej. 1360): ").strip()
        input_alto = input("Ingresa el Alto (ej. 768): ").strip()
        input_hz = input("Ingresa los Hz (ej. 60 o 75): ").strip()

        if (
            input_ancho.isdigit()
            and input_alto.isdigit()
            and input_hz.isdigit()
        ):
          cambiar_resolucion(
              int(input_ancho), int(input_alto), int(input_hz)
          )
        else:
          mostrar_mensaje(
              "Error", "Debes ingresar valores numéricos válidos.", tipo=16
          )
      else:
        mostrar_mensaje("Aviso", "Opción fuera de rango.", tipo=16)
    else:
      mostrar_mensaje("Aviso", "Entrada no válida. Ingresa un número.", tipo=16)


if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(f"\n[ERROR CRÍTICO ENCONTRADO]: {e}")
    input(
        "\nEl programa se detuvo. Presiona ENTER para cerrar esta ventana..."
    )