import ctypes
import os
import subprocess
import sys


def es_administrador():
  """Verifica si el script se está ejecutando con permisos de administrador."""
  try:
    return ctypes.windll.shell32.IsUserAnAdmin()
  except:
    return False


def ejecutar_comando(comando):
  """Ejecuta un comando en la terminal y muestra el resultado."""
  print(f"\n[Ejecutando] {comando}")
  resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
  if resultado.stdout:
    print(resultado.stdout.strip())
  if resultado.stderr:
    print(f"Mensaje/Error: {resultado.stderr.strip()}")
  return resultado.returncode


def main():
  if not es_administrador():
    print(
        "Este script requiere permisos de administrador para modificar la"
        " licencia."
    )
    print("Reiniciando el script con privilegios elevados...")
    # Reejecuta el script como administrador
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

  print("Activador de Windows 10")
  print("==================================================")
  print("Selecciona la versión de Windows 10 que utilizas:")
  print("1. Windows 10 Home")
  print("2. Windows 10 Home N")
  print("3. Windows 10 Pro")
  print("4. Windows 10 Pro N")
  print("5. Windows 10 Education")
  print("6. Windows 10 Education N")
  print("7. Windows 10 Enterprise")
  print("8. Windows 10 Enterprise N")

  opcion = input("Ingresa el número de tu versión (1-8): ").strip()
  claves = {
      "1": ("Windows 10 Home", "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99"),
      "2": ("Windows 10 Home N", "3KHY7-WNT83-DGQKR-F7HPP-842HM"),
      "3": ("Windows 10 Pro", "W269N-WFGWX-YVC9B-4J6C9-T83GX"),
      "4": ("Windows 10 Pro N", "MH37W-N47XK-V7XM9-C7227-GCQG9"),
      "5": ("Windows 10 Education", "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2"),
      "6": ("Windows 10 Education N", "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ"),
      "7": ("Windows 10 Enterprise", "NPPR9-FWDCX-D2C8J-H872K-2YT43"),
      "8": ("Windows 10 Enterprise N", "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4"),
  }

  if opcion not in claves:
    print("Opción no válida. Ejecuta el script nuevamente.")
    input("\nPresiona Enter para salir...")
    return

  nombre_version, clave = claves[opcion]
  print(f"\n[+] Versión seleccionada: {nombre_version}")
  print(f"[+] Clave a utilizar: {clave}")
  servidor_kms = "kms.digiboy.ir"  # o "s8.slitaz.org" / "kms9.digiboy.ir"

  print("\n Paso 1: Instalando la clave de producto")
  ejecutar_comando(f"cscript //nologo %windir%\\system32\\slmgr.vbs /ipk {clave}")

  print("\n Paso 2: Configurando el servidor KMS")
  ejecutar_comando(
      f"cscript //nologo %windir%\\system32\\slmgr.vbs /skms {servidor_kms}"
  )

  print("\n Paso 3: Activando el sistema operativo")
  ejecutar_comando(
      f"cscript //nologo %windir%\\system32\\slmgr.vbs /ato"
  )

  print(" Proceso finalizado. Comprueba el estado en Configuración.")
  input("\nPresiona Enter para salir...")


if __name__ == "__main__":
  main()