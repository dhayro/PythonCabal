import pyautogui
import pygetwindow as gw
import time

import keyboard

from pynput.mouse import Button, Controller
import time
from screen_search import Search

from os import remove

import os.path as path

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image



mouse = Controller()
def raton_posicion (x,y):
    mouse.position = (x, y)
    print('Now we have moved it to {0}'.format(
        mouse.position))
    # Press and release
    # mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)
def raton_posicion (x,y):
    mouse.position = (x, y)
    print('Now we have moved it to {0}'.format(
        mouse.position))
    # Press and release
    # mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)
def buscar_imagen_en_pantalla(imagen_path, confianza=0.9):
    # Cargar la imagen a buscar
    imagen = cv2.imread(imagen_path)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen {imagen_path}")
        return False
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    try:
        # Capturar la pantalla
        captura_pantalla = pyautogui.screenshot()

        # Convertir la captura de pantalla a una imagen OpenCV
        captura_pantalla_np = np.array(captura_pantalla)
        captura_pantalla_cv = cv2.cvtColor(captura_pantalla_np, cv2.COLOR_RGB2BGR)
        captura_pantalla_gris = cv2.cvtColor(captura_pantalla_cv, cv2.COLOR_BGR2GRAY)

        # Buscar la imagen en la captura de pantalla
        coincidencias = cv2.matchTemplate(captura_pantalla_gris, imagen_gris, cv2.TM_CCOEFF_NORMED)
        loc = np.where(coincidencias >= confianza)

        if len(loc[0]) > 0:
            # Obtener la mejor coincidencia
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(coincidencias)
            x, y = max_loc

            # Obtener las dimensiones de la imagen
            ancho, alto = imagen_gris.shape[::-1]

            # Calcular el centro de la coincidencia
            centro_x = x + ancho // 2
            centro_y = y + alto // 2

            # Dibujar un rectángulo alrededor de la coincidencia (para depuración)
            cv2.rectangle(captura_pantalla_cv, (x, y), (x + ancho, y + alto), (0, 255, 0), 2)
            cv2.imwrite('debug_captura.png', captura_pantalla_cv)

            print(f"Imagen encontrada en ({centro_x}, {centro_y})")
            return centro_x, centro_y
        else:
            print("No se encontró la imagen en la pantalla")
            return False

    except Exception as e:
        print(f"Error durante la búsqueda de la imagen: {e}")
        return False

def obtener_centro_ventana(nombre_proceso):
    try:
        ventana = gw.getWindowsWithTitle(nombre_proceso)[0]
        centro_x = ventana.left + ventana.width / 2
        centro_y = ventana.top + ventana.height / 2
        return centro_x, centro_y
    except IndexError:
        return None
def imagenhp():
    search = buscar_imagen_en_pantalla("otros/nucleo.png")
    principal = buscar_imagen_en_pantalla("otros/principal.png")
    if search == False:
        return False

    # Capturar directamente la región de interés
    if principal:
        x, y = int(search[0])-63, int(search[1])-687
    else:
        x, y = int(search[0])-63, int(search[1])-679
    screenshot = pyautogui.screenshot(region=(x, y, 156, 15))
    screenshot.save('captura/hp_screenshot.png')
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Convertir a espacio de color HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definir rangos de color rojo y verde en HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])

    # Crear máscaras para los colores rojo y verde
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Calcular los porcentajes de rojo y verde por separado
    total_pixels = mask_red.size
    red_percentage = (np.sum(mask_red == 255) / total_pixels) * 100
    green_percentage = (np.sum(mask_green == 255) / total_pixels) * 100

    # Sumar los porcentajes
    total_percentage = red_percentage + green_percentage


    # print(f"Porcentaje de HP: {total_percentage:.2f}% (Rojo: {red_percentage:.2f}%, Verde: {green_percentage:.2f}%)")
    return total_percentage

def funcionvida():
    global stop_flag, tiempo_inicio
    last_print_time = time.time()
    print_interval = 2  # Imprimir cada 2 segundos

    # Configuración de cooldowns (en segundos)
    cooldown_f5 = 60
    cooldown_f6 = 180

    # Tiempo del último uso de cada habilidad
    last_use_f5 = 0
    last_use_f6 = 0

    def use_skill(skill_number, ctrl_number):
        keyboard.press_and_release(skill_number)
        time.sleep(0.5)
        keyboard.press_and_release(ctrl_number)
        print(f"Habilidad {skill_number} usada")
        return time.time()

    while not stop_flag and not keyboard.is_pressed('delete'):
        current_time = time.time()
        if current_time - last_print_time >= print_interval:
            tiempo_transcurrido = current_time - tiempo_inicio
            last_print_time = current_time

        vida = imagenhp()
        if vida != False:
            print(f"Nivel de vida actual: {vida}")

            # Usar = cada 6 segundos si la vida es menor o igual a 45
            if vida <= 45:
                keyboard.press_and_release(13)
                print("Usado =")

            # Verificar y usar F6 si es necesario y está disponible
            if vida <= 20 and current_time - last_use_f6 >= cooldown_f6:
                last_use_f6 = use_skill("f6", 80)
                print(f"F6 usado. Próximo uso disponible en {cooldown_f6} segundos.")

            # Verificar y usar F5 si es necesario y está disponible
            elif vida <= 30 and current_time - last_use_f5 >= cooldown_f5:
                last_use_f5 = use_skill("f5", 79)
                print(f"F5 usado. Próximo uso disponible en {cooldown_f5} segundos.")
                time.sleep(0.5)
                vida = imagenhp()

        time.sleep(0.5)  # Reducido el tiempo de espera

    print("funcionvida terminada")

def capturar_pantalla_mostruo(x, y, ancho, alto):
    screenshot = pyautogui.screenshot(region=(x, y, ancho, alto))
    screenshot.save('captura/captura_pantalla_mostruo.png')
    return 'captura/captura_pantalla_mostruo.png'
def imagenmostruo():
    global moustruovida
    search = buscar_imagen_en_pantalla("otros/mostrous.jpg")
    if search == False:
        if path.exists('captura/captura_pantalla_mostruo.png'):
            remove("captura/captura_pantalla_mostruo.png")
        return False
    else:
        imagen_capturada = capturar_pantalla_mostruo(int(search[0])-4, int(search[1])-7, 270, 15)
        image = cv2.imread('captura/captura_pantalla_mostruo.png')

        # Convertir la imagen a espacio de color HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Definir el rango de color amarillo en HSV
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Crear una máscara para el color amarillo
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Calcular el porcentaje de píxeles amarillos
        yellow_pixels = np.sum(mask == 255)
        total_pixels = mask.size

        # Calcular el porcentaje de llenado (amarillo)
        percentage = (yellow_pixels / total_pixels) * 100

        moustruovida=percentage

        return percentage

def capturar_pantalla_hp(x, y, ancho, alto):
    screenshot = pyautogui.screenshot(region=(x, y, ancho, alto))
    # screenshot.show()
    screenshot.save('captura/captura_pantalla_HP.png')
    return 'captura/captura_pantalla_HP.png'

# Ejemplo: Obtener el centro de la ventana del programa "notepad.exe"
nombre_proceso = "cabal"

centro_ventana = obtener_centro_ventana(nombre_proceso)

def mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y, duracion_clic=1):
    try:
        # Obtener la posición actual del ratón
        posicion_actual = pyautogui.position()

        # Realizar clic derecho y mantenerlo presionado
        # pyautogui.mouseDown(button='right')

        # Mover el ratón con desplazamiento
        pyautogui.moveRel(desplazamiento_x, desplazamiento_y, duration=duracion_clic)

        pyautogui.click(button='left')
        print('soy derecha pero me voy a la izquierda')
        # Soltar el clic derecho
        # pyautogui.mouseUp(button='right')

        # Devolver el ratón a su posición original
        # pyautogui.moveTo(posicion_actual[0], posicion_actual[1], duration=duracion_clic)

    except Exception as e:
        print(f"Error: {e}")

# Ejemplo: Mover el ratón hacia la derecha manteniendo clic derecho

def capturar_pantalla(x, y, ancho, alto):
    screenshot = pyautogui.screenshot(region=(x, y, ancho, alto))
    screenshot.save('captura/captura_pantalla_SP.png')
    return 'captura/captura_pantalla_SP.png'

def imagen():
    search = Search("sp/7.jpg")
    pos = search.imagesearch()
    if pos[0] == -1:
        if path.exists('captura/captura_pantalla_SP.png'):
            remove("captura/captura_pantalla_SP.png")
        return False
    else:
        return pos
def caminar_raton_posicion (x,y):
    mouse.position = (x, y)
    print('Now we have moved it to {0}'.format(
        mouse.position))
    # Press and release
    # mouse.press(Button.left)
    mouse.release(Button.left)
    posicion_actual = pyautogui.position()
    pyautogui.mouseDown(button='left')
    time.sleep(7)
    pyautogui.mouseUp(button='left')

def mover_raton_clic_izquierdo(desplazamiento_x, desplazamiento_y, duracion_clic=1):
    try:
        # Obtener la posición actual del ratón
        posicion_actual = pyautogui.position()

        # Realizar clic derecho y mantenerlo presionado
        # pyautogui.mouseDown(button='right')

        # Mover el ratón con desplazamiento
        pyautogui.moveRel(desplazamiento_x, desplazamiento_y, duration=duracion_clic)

        pyautogui.click(button='right')

        print('soy izquierda pero me voy a la derecha')

        # Soltar el clic derecho
        # pyautogui.mouseUp(button='right')

        # Devolver el ratón a su posición original
        # pyautogui.moveTo(posicion_actual[0], posicion_actual[1], duration=duracion_clic)

    except Exception as e:
        print(f"Error: {e}")



def imagenmostruos():
    ruta_imagen = 'otros/mostrous.jpg'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        return False
    else:
        print('detecte mostruo')
        return pos

def imagenEca():
    ruta_imagen = 'eca/eca.png'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre eca')
        return False
    else:
        print('encontre eca')
        return pos

def imagenentrar():
    try:
        # Buscar la imagen en la pantalla
        ubicacion = pyautogui.locateOnScreen("otros/enter.png")

        if ubicacion:
            # Obtener las coordenadas del centro de la imagen encontrada
            x, y, ancho, alto = ubicacion
            centro_x = x + ancho // 2
            centro_y = y + alto // 2

            return centro_x, centro_y
        else:
            return False

    except Exception as e:
        return False

def imagennoentrar():
    imagen_a_buscar = "otros/no_entrada.png"  # Reemplaza con la ruta de tu propia imagen
    pos = buscar_imagen_en_pantalla(imagen_a_buscar)
    if pos== False:
        return False
    else:
        return pos


def imageniniciar():
    try:
        # Buscar la imagen en la pantalla
        ruta_imagen = 'otros/iniciar.png'
        pos = buscar_imagen_en_pantalla(ruta_imagen)
        if pos == False:
            print('no encontre iniciar')
            return False
        else:
            print('encontre iniciar')
            return pos

    except Exception as e:
        print('error al encontre iniciar')
        return False
def imagenterminar():
    try:
        # Buscar la imagen en la pantalla
        ruta_imagen = 'otros/terminar.png'
        pos = buscar_imagen_en_pantalla(ruta_imagen)
        if pos == False:
            return False
        else:
            return pos

    except Exception as e:
        print('error al encontre iniciar')
        return False
def imagendado():
    try:
        # Buscar la imagen en la pantalla
        ubicacion = pyautogui.locateOnScreen("otros/dado.png")

        if ubicacion:
            # Obtener las coordenadas del centro de la imagen encontrada
            x, y, ancho, alto = ubicacion
            centro_x = x + ancho // 2
            centro_y = y + alto // 2

            return centro_x, centro_y
        else:
            return False

    except Exception as e:
        return False
def imagenok():
    try:
        # Buscar la imagen en la pantalla
        ubicacion = pyautogui.locateOnScreen("otros/ok.png")

        if ubicacion:
            # Obtener las coordenadas del centro de la imagen encontrada
            x, y, ancho, alto = ubicacion
            centro_x = x + ancho // 2
            centro_y = y + alto // 2

            return centro_x, centro_y
        else:
            return False

    except Exception as e:
        return False
def imagensalir():
    try:
        # Buscar la imagen en la pantalla
        ubicacion = pyautogui.locateOnScreen("otros/salir.png")

        if ubicacion:
            # Obtener las coordenadas del centro de la imagen encontrada
            x, y, ancho, alto = ubicacion
            centro_x = x + ancho // 2
            centro_y = y + alto // 2

            return centro_x, centro_y
        else:
            return False

    except Exception as e:
        return False

# while True:
#     imagen_a_buscar_puente = "key/puente.png"  # Reemplaza con la ruta de tu propia imagen
#     puente = buscar_imagen_en_pantalla(imagen_a_buscar_puente)
#     if puente!=False:
#         print('te halle')
#         break
#     keyboard.press_and_release("alt+1")
#     time.sleep(1)
#     keyboard.press_and_release("alt+2")

def click_raton_posicion (x,y):
    mouse.position = (x, y)
    print('Now we have moved it to {0}'.format(
        mouse.position))
    # Press and release
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)
time.sleep(3)
stop_flag = False
time.sleep(2)

def ejecutar_imagenhp_periodicamente():
    while True:
        hp_percentage = imagenhp()
        if hp_percentage is not False:
            print(f"Porcentaje de HP: {hp_percentage:.2f}%")
        else:
            print("No se pudo detectar la barra de HP")

        time.sleep(2)  # Esperar 2 segundos antes de la próxima ejecución

# Iniciar la ejecución periódica
# ejecutar_imagenhp_periodicamente()
tiempo_inicio = time.time()
# funcionvida()

def funcionBM_optimizada():
    global stop_flag, bm3WI1

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM optimizada en ejecución")
        time.sleep(0.3)  # Reduced sleep time

       

        bm2WI = buscar_imagen_en_pantalla("otros/bm2WI.png")
        bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
        bm3WI = buscar_imagen_en_pantalla("otros/bm3WI.png")
        bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
        mago = buscar_imagen_en_pantalla("otros/mago.png")

        if bm2WI1 and not mago:
            for _ in range(6):
                keyboard.press_and_release("6")
                keyboard.press_and_release("space")
                time.sleep(0.2)

                if not buscar_imagen_en_pantalla("otros/bm2WI1.png"):
                    break
        elif bm3WI1:
            habilidades = [
                {"tecla": "6", "cooldown": 0.5, "casting": 0.9, "ultimo_uso": 0},
                {"tecla": "6", "cooldown": 0.5, "casting": 0.9, "ultimo_uso": 0},
                {"tecla": "5", "cooldown": 0.5, "casting": 0.9, "ultimo_uso": 0},
                {"tecla": "6", "cooldown": 0.5, "casting": 0.9, "ultimo_uso": 0},
                {"tecla": "7", "cooldown": 0, "casting": 1.7, "ultimo_uso": 0},
                {"tecla": "7", "cooldown": 0, "casting": 1.7, "ultimo_uso": 0},
                {"tecla": "7", "cooldown": 0, "casting": 1.7, "ultimo_uso": 0},
            ]

            while True:
                if not buscar_imagen_en_pantalla("otros/comentarios1.png"):
                    keyboard.press_and_release("6")
                    keyboard.press_and_release("space")
                    time.sleep(0.2)

                    if not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                        break
                else:
                    ahora = time.time()
                    for hab in habilidades:
                        if ahora - hab["ultimo_uso"] >= hab["cooldown"]:
                            keyboard.press_and_release(hab["tecla"])
                            print(f"Presionando {hab['tecla']} - Casting {hab['casting']}s")
                            hab["ultimo_uso"] = time.time()
                            time.sleep(hab["casting"])
                            keyboard.press_and_release("space")
                            if not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                                break
                if not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                   break

            # ataque_count = 0
            # max_ataques = 10

            # while ataque_count < max_ataques:
            #     print('ataque BM3 con monstruos')
            #     keyboard.press_and_release("6")
            #     keyboard.press_and_release("space")
            #     time.sleep(0.1)

            #     if not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
            #         break

            #     ataque_count += 1
        else:
            print('ataque normal con monstruos')
            for tecla in ["2", "3", "4", "8"]:
                keyboard.press_and_release(tecla)
                keyboard.press_and_release("space")
                time.sleep(0.2)

                if buscar_imagen_en_pantalla("otros/bm3WI1.png") or not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                    keyboard.press_and_release("space")
                    time.sleep(0.2)
                    break

    print("funcionBM optimizada terminada")


# funcionBM_optimizada()
def vida_estancada(vida_anterior, vida_actual, ciclos_sin_bajar, umbral=1, max_ciclos=10):
    """
    Retorna True si la vida del monstruo no ha bajado en los últimos ciclos.
    - umbral: diferencia mínima para considerar que la vida bajó.
    - max_ciclos: cantidad de ciclos permitidos sin bajar la vida.
    """
    print(f"[DEBUG] vida_anterior: {vida_anterior}, vida_actual: {vida_actual}, ciclos_sin_bajar: {ciclos_sin_bajar}")
    if vida_actual is False:
        print("[DEBUG] No hay barra de vida detectada.")
        return True  # No hay barra de vida, salir del combate
    if vida_actual < vida_anterior - umbral:
        print("[DEBUG] La vida bajó.")
        return False  # La vida bajó
    ciclos_sin_bajar += 1
    print(f"[DEBUG] La vida NO bajó, ciclos_sin_bajar incrementado a {ciclos_sin_bajar}")
    if ciclos_sin_bajar >= max_ciclos:
        print("[DEBUG] Se alcanzó el máximo de ciclos sin bajar la vida.")
        return True
    return False

time.sleep(0.5)
vida_anterior = None
ciclos_sin_bajar = 0

while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
    print("Iniciando ciclo kong1")  
    vida_actual = imagenmostruo()
    print(f"[DEBUG] vida_actual detectada: {vida_actual}")

    if vida_anterior is None:
        vida_anterior = vida_actual
        ciclos_sin_bajar = 0
        print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
    else:
        if vida_actual < vida_anterior - 1:
            print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
            vida_anterior = vida_actual
            ciclos_sin_bajar = 0
        else:
            ciclos_sin_bajar += 1
            print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
            if ciclos_sin_bajar >= 3:
                print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                break

    time.sleep(0.5)  # Ajusta el tiempo según tu necesidad
# piso8 = buscar_imagen_en_pantalla("acheron/piso5.png")
# if piso8!=False:
#     # raton_posicion (piso8[0]+30, piso8[1]-120)
#     raton_posicion (piso8[0]+50, piso8[1]+150)
# centro_ventana = obtener_centro_ventana(nombre_proceso)
# if centro_ventana:
#     print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
#     raton_posicion(centro_ventana[0]-330, centro_ventana[1]+120)
# nombre_proceso = "cabal"
# centro_ventana3 = obtener_centro_ventana(nombre_proceso)
# if centro_ventana3:
#     print(f"El centro de la ventana3 de {nombre_proceso} es ({centro_ventana3[0]}, {centro_ventana3[1]}).")
#     raton_posicion (centro_ventana3[0]+(20), centro_ventana3[1]-(-190))
#     # desplazamiento_x = 130  # Ajusta según sea necesario
#     # desplazamiento_y = 0
#     # mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y)

#     # desplazamiento_x = 130  # Ajusta según sea necesario
#     # desplazamiento_y = 0
#     # mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y)
#     posicion_actual = pyautogui.position()
#     pyautogui.click(button='left')
#     time.sleep(0.5)
#     keyboard.press_and_release("space")
#     time.sleep(0.5)
#     keyboard.press_and_release(".")
#     time.sleep(0.5)
#     keyboard.press_and_release(",")
#     time.sleep(0.9)
#     keyboard.press_and_release(".")
#     time.sleep(0.5)
    
#     keyboard.press_and_release("z")