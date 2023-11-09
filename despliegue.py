import os
import sys
import threading
import signal

def cambiar_rama_y_desplegar(rama_objetivo):
    # Verificar la rama actual
    resultado = os.popen('git rev-parse --abbrev-ref HEAD').read().strip()
    rama_actual = resultado.strip()

    # Cambiar de rama si es necesario
    if rama_actual != rama_objetivo:
        print(f'Cambiando a la rama {rama_objetivo}')
        os.system(f'git checkout {rama_objetivo}')
    
    # Hacer un hard reset en la rama actual
    print('Haciendo git reset --hard')
    os.system('git reset --hard')

    # Ejecutar el servidor Django en un hilo
    server_thread = threading.Thread(target=ejecutar_servidor)
    server_thread.start()

def ejecutar_servidor():
    # Ejecutar el servidor Django
    os.system('python manage.py runserver')

if __name__ == "__main__":
    # Configurar el manejo de la señal de interrupción (CTRL-C)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Verificar la cantidad de argumentos
    if len(sys.argv) != 2:
        print("Uso: python despliegue.py <ambiente>")
        sys.exit(1)

    ambiente = sys.argv[1]

    # Verificar el ambiente y realizar el despliegue correspondiente
    if ambiente == 'produccion':
        cambiar_rama_y_desplegar('main')
    elif ambiente == 'desarrollo':
        cambiar_rama_y_desplegar('development')
    else:
        print("Ambiente no válido. Use 'produccion' o 'desarrollo'")
        sys.exit(1)
