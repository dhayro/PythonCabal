import pyautogui
import cv2
import numpy as np
import time
import keyboard
from pynput.mouse import Button, Controller
import ctypes
import threading
import concurrent.futures
import os.path as path
from os import remove
from screen_search import Search
import logging
import math

# Constantes
VK_CAPITAL = 0x14
mouse = Controller()
stop_flag = False

def forzar_deshabilitar_bloq_mayus():
    caps_lock_state = ctypes.windll.user32.GetKeyState(VK_CAPITAL)
    if caps_lock_state & 1:
        ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, 2, 0)
        print("Bloq Mayús ha sido deshabilitado.")
    else:
        print("Bloq Mayús ya estaba deshabilitado.")

def buscar_imagen_en_pantalla(imagen_path, confianza=0.9):
    global nombre_proceso
    # Cargar la imagen a buscar
    imagen = cv2.imread(imagen_path)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen {imagen_path}")
        return False
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    try:
        # Obtener la ventana específica
        ventana = gw.getWindowsWithTitle(nombre_proceso)[0]
        if not ventana:
            print(f"No se encontró la ventana '{nombre_proceso}'")
            return False

        # Obtener las coordenadas y dimensiones de la ventana
        left, top, width, height = ventana.left, ventana.top, ventana.width, ventana.height

        # Capturar la pantalla solo de la ventana específica
        captura_pantalla = pyautogui.screenshot(region=(left, top, width, height))

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

            # Ajustar las coordenadas al sistema de coordenadas global
            centro_x_global = left + centro_x
            centro_y_global = top + centro_y

            print(f"Imagen encontrada en ({centro_x_global}, {centro_y_global})")
            return centro_x_global, centro_y_global
        else:
            # print("No se encontró la imagen en la ventana")
            return False

    except Exception as e:
        print(f"Error durante la búsqueda de la imagen: {e}")
        return False


def raton_posicion(x, y):
    mouse.position = (x, y)
    print(f'Movido a {mouse.position}')
    mouse.release(Button.left)
    time.sleep(0.5)

def funciologin():
    global stop_flag, contardg, dungeon, terminar, nombre_proceso, tiempo_inicio, bosfinal, conteocabal, terminando, atacar

    imagenes = {
        'failconect': "login/failconect.png",
        'failconectserver': "login/failconectserver.png",
        'cabal': "login/cabal.png",
        'endsesion': "login/endsesion.png",
        'error': "login/error.png",
        'okerror': "login/okerror.png",
        'disconected': "login/disconected.png",
        'caballogin': "login/caballogin.png",
        'account_login': "login/account-login.bmp",
        'server_select': "login/server-select.bmp",
        'duallogin': "login/duallogin.png",
        'tyes': "login/tyes.png",
        'character_list': "login/character-list.bmp",
        'sub_pass': "login/sub-pass.bmp",
        'ok': "login/ok.png"
    }

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funciologin en ejecución")
        time.sleep(0.5)

        for nombre, ruta in imagenes.items():
            pos = buscar_imagen_en_pantalla(ruta)
            if pos:
                print(f"Encontrada imagen: {nombre} en posición {pos}")
                if nombre in ['failconect', 'failconectserver', 'disconected']:
                    print(f"Haciendo clic en {nombre}")
                    raton_posicion(pos[0], pos[1] + 135)
                    pyautogui.click()
                elif nombre == 'endsesion':
                    print("Haciendo clic en endsesion")
                    raton_posicion(pos[0] + 90, pos[1])
                    pyautogui.click()
                elif nombre in ['okerror', 'caballogin']:
                    print(f"Haciendo clic en {nombre}")
                    raton_posicion(pos[0], pos[1])
                    pyautogui.click()
                elif nombre == 'cabal':
                    print("Cabal detectado, actualizando variables")
                    conteocabal, dungeon, atacar = 1, 0, 0
                    # Continuar con el proceso de login
                    continue
                elif nombre == 'account_login':
                    print("Ingresando credenciales")
                    raton_posicion(pos[0], pos[1] + 50)
                    pyautogui.click()
                    for _ in range(15):
                        keyboard.press_and_release("backspace")
                    forzar_deshabilitar_bloq_mayus()
                    keyboard.write("dhayro")
                    time.sleep(0.5)
                    raton_posicion(pos[0], pos[1] + 90)
                    pyautogui.click()
                    time.sleep(0.5)
                    keyboard.write("Dhakongto2710")
                    time.sleep(0.5)
                    keyboard.press_and_release("enter")
                    time.sleep(2)
                elif nombre == 'duallogin':
                    print("Manejando dual login")
                    tyes = buscar_imagen_en_pantalla(imagenes['tyes'])
                    if tyes:
                        raton_posicion(tyes[0], tyes[1])
                        pyautogui.click()
                        time.sleep(8)
                elif nombre == 'server_select':
                    print("Seleccionando canal")
                    channel_pos = buscar_imagen_en_pantalla("login/channel/9.bmp")
                    if channel_pos:
                        raton_posicion(channel_pos[0], channel_pos[1])
                        pyautogui.click(clicks=2, interval=0.1)
                        time.sleep(1.5)
                elif nombre == 'character_list':
                    print("Seleccionando personaje")
                    raton_posicion(pos[0], pos[1] + 75)
                    pyautogui.click(clicks=2, interval=0.1)
                    sub_pass = buscar_imagen_en_pantalla(imagenes['sub_pass'])
                    time.sleep(1)
                    if sub_pass:
                        print("Ingresando sub-password")
                        numeros = ["1", "0", "0", "5", "9", "3"]
                        for num in numeros:
                            imagen_a_buscar_pass = f"login/number/{num}.bmp"
                            pass_pos = buscar_imagen_en_pantalla(imagen_a_buscar_pass)
                            if pass_pos:
                                raton_posicion(pass_pos[0], pass_pos[1])
                                pyautogui.click()
                                time.sleep(0.5)
                        ok = buscar_imagen_en_pantalla(imagenes['ok'])
                        if ok:
                            raton_posicion(ok[0], ok[1])
                            pyautogui.click()
                # No salimos del bucle for aquí, para que continúe verificando otras imágenes
        else:
            # Si no se encontró ninguna imagen, esperamos un poco antes de volver a intentar
            print("No se encontró ninguna imagen conocida. Esperando...")
            time.sleep(2)

    print("funciologin terminada")

def imagenSP():
    try:
        search = Search("sp/7.jpg")
        pos = search.imagesearch()

        if pos[0] == -1:
            if path.exists('captura/captura_pantalla_SP.png'):
                remove("captura/captura_pantalla_SP.png")
                logging.info("Removed existing SP screenshot")
            logging.debug("SP image not found")
            return False
        else:
            logging.info(f"SP image found at position: {pos}")
            return pos
    except Exception as e:
        logging.error(f"Error in imagenSP function: {str(e)}")
        return False

import pyautogui
import logging
import os

def capturar_pantalla(x, y, ancho, alto):
    try:
        # Ensure the directory exists
        os.makedirs('captura', exist_ok=True)

        # Capture the screenshot
        screenshot = pyautogui.screenshot(region=(x, y, ancho, alto))

        # Save the screenshot
        file_path = 'captura/captura_pantalla_SP.png'
        screenshot.save(file_path)

        logging.info(f"Screenshot captured and saved to {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"Error capturing screenshot: {str(e)}")
        return None

# from functools import lru_cache

# @lru_cache(maxsize=None)
# def buscar_imagen_en_pantalla_cached(imagen_path):
#     return buscar_imagen_en_pantalla(imagen_path)

def funcionSP():
    global stop_flag, conteocabal, puerta, contardg, contardgok, cuenta, lanzabuff, wavecuenta, esperandocuenta, dungeon, atacar, contadormostruos1, bosscuenta, tiempo_transcurrido

    last_print_time = time.time()
    last_buff_time = time.time()
    print_interval = 5  # Print every 5 seconds
    buff_interval = 10  # Check buff every 10 seconds

    while not stop_flag and not keyboard.is_pressed('delete'):
        current_time = time.time()
        ctns = []  # Inicializar ctns como una lista vacía

        # # Buscar y activar buff SP si es necesario (cada 10 segundos)
        # if current_time - last_buff_time >= buff_interval:
        #     if lanzabuff == 1:
        #         bufsp = buscar_imagen_en_pantalla_cached("otros/bufsp.png")
        #         if bufsp:
        #             keyboard.press_and_release("f8")
        #     last_buff_time = current_time
        if lanzabuff == 1:
            bufsp = buscar_imagen_en_pantalla("otros/bufsp.png")
            if bufsp != False:
                keyboard.press_and_release("f8")
        # Buscar y procesar imagen SP
        sp = imagenSP()
        if sp:
            img_path = capturar_pantalla(sp[0], sp[1], 65, 10)
            img = cv2.imread(img_path)
            if img is not None:
                grises = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                bordes = cv2.Canny(grises, 100, 800)
                ctns, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Activar habilidad si no hay SP
                # if len(ctns) == 0:
                #     keyboard.press_and_release("-")
                bossok = buscar_imagen_en_pantalla("eca/boss.png")
                if len(ctns)==0 and bossok:
                    keyboard.press_and_release("-")

        # Imprimir información de estado cada 5 segundos
        if current_time - last_print_time >= print_interval:
            print(f"funcionSP en ejecución\n"
                  f"Número de sp: {len(ctns)}, conteocabal: {conteocabal}, DG1: {contardg}, DGOK: {contardgok}\n"
                  f"cuentaboss: {bosscuenta}, cuentawave: {wavecuenta}, esperandocuenta: {esperandocuenta}\n"
                  f"dungeon: {dungeon}, atacar: {atacar}, contadormostruos1: {contadormostruos1}")
            last_print_time = current_time

        time.sleep(0.05)  # Reduced sleep time

    print("funcionSP terminada")

from os import path, remove
import matplotlib.pyplot as plt


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

        return percentage
def funcionmostruo():
    global stop_flag, contadormostruos1, bosfinal, dungeon, puerta, terminar, bosdetectado,esperandocuenta
    global terminando, lanzabuff, puertita, vidamostruo, bos1_namedetectado, fail

    while not stop_flag and not keyboard.is_pressed('delete'):
        salix = buscar_imagen_en_pantalla("otros/salix.png")
        if  not (dungeon == 1 and salix ): #and esperandocuenta<12
            continue

        print("funcionmostruo en ejecución")

        # Realizar todas las búsquedas de imágenes de una vez
        vidamostruo = imagenmostruo()
        fail = buscar_imagen_en_pantalla("otros/fail.png")
        dado = buscar_imagen_en_pantalla("otros/dado.png")
        bossok = buscar_imagen_en_pantalla("eca/boss.png")

        if bossok:
            bosdetectado = 1

        if not fail and not dado and dungeon == 1:
            if vidamostruo:
                contadormostruos1 = 0
                puerta = 0
                print('variable atacar')
                if vidamostruo <= 15 and not bosdetectado:
                    keyboard.press_and_release("z")
            else:
                keyboard.press_and_release("z")
                contadormostruos1 += 1

                # Verificar vida y puerta solo si no se detectó vida antes
                vidamostruo = imagenmostruo()
                puerta = buscar_imagen_en_pantalla("otros/puerta.png")

                if vidamostruo and not puerta:
                    contadormostruos1 = 0

        if puertita:
            contadormostruos1 = 0

        time.sleep(0.1)  # Pequeña pausa para evitar sobrecarga de CPU

    print("funcionmostruo terminada")

def funcionmostruoeca():
    global stop_flag, imagen_presente_esperando, bosdetectado, lanzabuff, esperandocuenta

    bosdetectadovalidar = False
    imagen_presente_esperando = False

    imagenes = {
        'esperando': ["eca/esperando.png", "eca/esperando1.png"],
        'bos1_name': "eca/bos1_name.png",
        'bos1': "eca/bos1.png",
        'bos2_3': "eca/bos2_3.png",
        'bos2_1': "eca/bos2_1.png",
        'caja': "otros/caja.png",
        'caja1': "otros/caja1.png"
    }

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionmostruoeca en ejecución")

        # Buscar imágenes de espera
        esperando = any(buscar_imagen_en_pantalla(img) for img in imagenes['esperando'])

        if esperando and not imagen_presente_esperando:
            esperandocuenta += 1
            print(f"La imagen apareció. Contador: {esperandocuenta}")
            imagen_presente_esperando = True
        elif not esperando and imagen_presente_esperando:
            imagen_presente_esperando = False

        # Buscar y procesar imágenes de jefes y cajas
        for nombre, ruta in imagenes.items():
            if nombre not in ['esperando']:
                resultado = buscar_imagen_en_pantalla(ruta)
                if resultado:
                    if nombre in ['bos1_name', 'bos1', 'bos2_1'] and bosdetectado == 0 and lanzabuff == 1:
                        if nombre == 'bos1_name':
                            raton_posicion(resultado[0], resultado[1] + 10)
                            pyautogui.click(button='left')
                        else:
                            bosdetectado = 1
                        print(f'detecte {nombre}')
                    elif nombre == 'bos2_3' and not bosdetectadovalidar:
                        bosdetectadovalidar = True
                        keyboard.press_and_release("z")
                        print('Detecté bos2_3 y presioné Z una vez')
                    elif nombre in ['caja', 'caja1']:
                        raton_posicion(resultado[0], resultado[1] + 10)
                        pyautogui.click(button='left')
                        print(f'detecte {nombre}')
                elif nombre == 'bos2_3':
                    bosdetectadovalidar = False

        time.sleep(0.1)  # Pequeño retraso para evitar sobrecarga del proceso
    print("funcionmostruoeca terminada")

def obtener_centro_ventana(nombre_proceso):
    try:
        ventana = gw.getWindowsWithTitle(nombre_proceso)[0]
        centro_x = ventana.left + ventana.width / 2
        centro_y = ventana.top + ventana.height / 2
        return centro_x, centro_y
    except IndexError:
        return None

import pygetwindow as gw
def funcionBM():
    global stop_flag, bm3WI1, bm2WI1, pase, contarwave, atacar, contarboss, vidamostruo, central, puerta, dungeon, wavecuenta, nombre_proceso, esperandocuenta, imagen_presente_esperando, bosscuenta, tiempo_transcurrido, tiempo_inicio

    imagen_presente = False

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM en ejecución")

        salix = buscar_imagen_en_pantalla("otros/salix.png")

        if  not (dungeon == 1 and atacar == 1 and salix):
            continue

        tiempo_transcurrido = time.time() - tiempo_inicio

        waveok = buscar_imagen_en_pantalla("eca/waveok.png")

        if waveok and not imagen_presente:
            wavecuenta += 1
            central=0
            print(f"La imagen apareció. Contador: {wavecuenta}")
            imagen_presente = True
            imagen_presente_esperando = False
        elif not waveok and imagen_presente:
            imagen_presente = False

        if dungeon == 1:
            bm2WI = buscar_imagen_en_pantalla("otros/bm2WI.png")
            bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
            bm2WI2 = buscar_imagen_en_pantalla("otros/bm2WI2.png")
            bm3WI = buscar_imagen_en_pantalla("otros/bm3WI.png")
            bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
            bm3WI2 = buscar_imagen_en_pantalla("otros/bm3WI2.png")
            bossok = buscar_imagen_en_pantalla("eca/boss.png")

            if bossok:
                contarboss += 1
                imagen_presente_esperando = False
                if contarboss == 1:
                    bosscuenta += 1
            else:
                contarboss = 0

            if bm3WI and vidamostruo  and (esperandocuenta in [8]) and bossok and not (bm3WI1 or bm2WI1): #, 12, 16, 20
                keyboard.press_and_release("f12")
                time.sleep(0.5)
                keyboard.press_and_release("f12")

            if bm3WI and vidamostruo and (wavecuenta in [8]) and not (bm3WI1 or bm2WI1): #5
                keyboard.press_and_release("f12")
                time.sleep(0.5)
                keyboard.press_and_release("f12")

            # if bm3WI and vidamostruo and (wavecuenta in [9]) and (bm2WI1 or bm3WI1): #9
            #     keyboard.press_and_release("f11")
            #     time.sleep(0.5)
            #     keyboard.press_and_release("f11")
            #     time.sleep(0.5)
            #     keyboard.press_and_release("alt+9")

            waiteca = buscar_imagen_en_pantalla("eca/esperando.png")

            if esperandocuenta in [2,14,15,16,17,18,19,20,21,22] and waiteca and central==0:
                centro_ventanabm3 = obtener_centro_ventana(nombre_proceso)
                print(f"El centro de la ventanabm3 de {nombre_proceso} es ({centro_ventanabm3[0]}, {centro_ventanabm3[1]}).")

                raton_posicion(centro_ventanabm3[0]+150, centro_ventanabm3[1]-200)
                time.sleep(0.5)

                for _ in range(3):
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)


                raton_posicion(centro_ventanabm3[0]+200, centro_ventanabm3[1]+130)
                time.sleep(0.5)

                for _ in range(4):
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)


                raton_posicion(centro_ventanabm3[0]-600, centro_ventanabm3[1])
                time.sleep(0.5)

                for _ in range(2):
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(0.5)


                raton_posicion(centro_ventanabm3[0]+160, centro_ventanabm3[1]+105)
                pyautogui.click(button='left')
                central = 1
                # if esperandocuenta in [8,4, 12, 16, 20]:#4, 12, 16, 20

                #     keyboard.press_and_release("f10")
                #     time.sleep(0.5)
                #     keyboard.press_and_release("f10")
                #     time.sleep(1.5)

            # if esperandocuenta in [4, 8, 12, 16, 20] and not bossok:
            #     bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
            #     if bm3WI1:
            #         raton_posicion(bm3WI1[0], bm3WI1[1]+5)
            #         time.sleep(1)
            #         pyautogui.click(button='right')
            #         # Movemos el ratón hacia abajo después de cada clic
            #         pyautogui.moveRel(0, 2)  # Mueve 15 píxeles hacia abajo
            #         time.sleep(1)
            #         pyautogui.click(button='right')

            if bm2WI and not (bm3WI1 or bm2WI1) and esperandocuenta in [8]:#[4] , 12, 16, 20
                if esperandocuenta <= 16:
                    time.sleep(19)
                keyboard.press_and_release("f10")
                time.sleep(0.5)
                keyboard.press_and_release("f10")
                time.sleep(8)
                keyboard.press_and_release("alt+9")

            # bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
            # bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
            # if (bm2WI1 or bm3WI1) and wavecuenta >= 9:
            #     keyboard.press_and_release("f11")

    print("funcionBM terminada")

def funcionBM2():
    global stop_flag, bm3WI1, dungeon, nombre_proceso, vidamostruo, puerta, atacar, puertita, bosdetectado,esperandocuenta

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM2 en ejecución")
        time.sleep(0.3)  # Reduced sleep time

        salix = buscar_imagen_en_pantalla("otros/salix.png")

        if  not (dungeon == 1 and atacar == 1 and salix and esperandocuenta<12): #and esperandocuenta<12
            continue


        if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
            continue

        if buscar_imagen_en_pantalla("login/cabal.png"):
            continue

        bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
        mago = buscar_imagen_en_pantalla("otros/mago.png")

        if bm2WI1 and mago:
            for _ in range(3):  # Limit the number of attempts
                keyboard.press_and_release("6")
                keyboard.press_and_release("space")
                time.sleep(0.2)

                if not buscar_imagen_en_pantalla("otros/bm2WI1.png"):
                    continue

        print('ataque normal con mostruos')

        for tecla in ["2", "3", "4", "8"]:
            keyboard.press_and_release(tecla)
            keyboard.press_and_release("space")
            time.sleep(0.2)

            if buscar_imagen_en_pantalla("otros/bm3WI1.png") or not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                keyboard.press_and_release("space")
                time.sleep(0.2)
                break

    print("funcionBM2 terminada")


def funcionBM3():
    global stop_flag, bm3WI1, dungeon, vidamostruo, atacar,esperandocuenta

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM3 en ejecución")
        time.sleep(0.5)  # Reducido de 1 a 0.5 segundos

        salix = buscar_imagen_en_pantalla("otros/salix.png")

        if not (vidamostruo and dungeon == 1 and atacar == 1 and salix and esperandocuenta<12) : #and esperandocuenta<12
            continue

        bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
        if not bm3WI1:
            continue

        ataque_count = 0
        max_ataques = 10  # Límite de ataques antes de verificar condiciones nuevamente

        while ataque_count < max_ataques:
            # if buscar_imagen_en_pantalla("login/cabal.png"):
            #     break

            print('ataque BM3 con monstruos')
            keyboard.press_and_release("6")
            keyboard.press_and_release("space")
            time.sleep(0.1)  # Reducido de 0.3 a 0.2 segundos

            if not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                ataque_count =20
                break

            # vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
            # if not vidamostruo:
            #     keyboard.press_and_release("space")
            #     time.sleep(0.3)  # Reducido de 0.5 a 0.3 segundos
            #     break

            ataque_count += 1

    print("funcionBM3 terminada")

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

def click_raton_posicion (x,y):
    mouse.position = (x, y)
    print('Now we have moved it to {0}'.format(
        mouse.position))
    # Press and release
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(0.5)
def funcionfail():
    global stop_flag, esperandocuenta,accion_realizada, bosscuenta, wavecuenta, dungeon, nombre_proceso, tiempo_inicio, puerta, terminando, terminar, lanzabuff, puertita, atacar, muriendo, fail

    def reset_variables():
        global dungeon, esperandocuenta,wavecuenta, bosscuenta, bosdetectado, terminando, lanzabuff, atacar, terminar, contardg, puerta, puertita, muriendo, vidamostruo, fin2, meta, bosfinal, tiempo_inicio
        dungeon = 2
        bosdetectado = terminando = lanzabuff = atacar = bosscuenta = wavecuenta = puerta = puertita  = muriendo = 0
        terminar = fin2 = meta = bosfinal = vidamostruo = False
        tiempo_inicio = time.time()


    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionfail en ejecución")
        time.sleep(1)

        bos2_1 = buscar_imagen_en_pantalla("eca/bos2_1.png")
        if bos2_1!=False or esperandocuenta==12:
            reset_variables()

        fail = buscar_imagen_en_pantalla("otros/fail.png")
        if fail:
            print('fail')
            click_raton_posicion(fail[0], fail[1])
            reset_variables()

        if not accion_realizada:  # Solo ejecutar si aún no se ha realizado la acción
            if dungeon == 2:
                ok = imagenok()
                if ok and buscar_imagen_en_pantalla("otros/fail.png"):
                    print('salir2')
                    click_raton_posicion(ok[0], ok[1])
                    time.sleep(0.5)
                    accion_realizada = True  # Marcar que se ha realizado la acción
                else:
                    imagen_a_buscar_salix = "eca/salix.png"  # Reemplaza con la ruta de tu propia imagen
                    salix = buscar_imagen_en_pantalla(imagen_a_buscar_salix)
                    if salix!=False:
                        click_raton_posicion (salix[0], salix[1])
                        time.sleep(1)
                        imagen_a_buscar_salidg = "eca/salidg.png"  # Reemplaza con la ruta de tu propia imagen
                        salidg = buscar_imagen_en_pantalla(imagen_a_buscar_salidg)
                        if salidg!=False:
                            click_raton_posicion (salidg[0]+130, salidg[1]+55)
                            time.sleep(0.5)
                            esperandocuenta=0
                            accion_realizada = True  # Marcar que se ha realizado la acción

    print("funcionfail terminada")

def buscar_imagen_en_pantalla2(imagen_path, area=None, confianza=0.9):
    imagen = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        print(f"No se pudo cargar la imagen {imagen_path}")
        return False, None

    try:
        captura_pantalla = np.array(pyautogui.screenshot(region=area))
        captura_pantalla_gris = cv2.cvtColor(captura_pantalla, cv2.COLOR_RGB2GRAY)

        coincidencias = cv2.matchTemplate(captura_pantalla_gris, imagen, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(coincidencias)

        if max_val >= confianza:
            imagen_h, imagen_w = imagen.shape
            pos_x = max_loc[0] + (imagen_w // 2)
            pos_y = max_loc[1] + (imagen_h // 2)

            if area:
                return True, (pos_x + area[0], pos_y + area[1])
            else:
                return True, (pos_x, pos_y)
        else:
            return False, None

    except Exception as e:
        print(f"Error al buscar la imagen: {e}")
        return False, None

def ajustar_area_ventana(area):
    margen_superior = 30  # Ajusta según el tamaño de la barra de título
    margen_lateral = 5    # Ajusta según el tamaño de los bordes laterales
    x1, y1, x2, y2 = area
    return (x1 + margen_lateral, y1 + margen_superior, x2 - margen_lateral, y2 - margen_lateral)
import win32gui
def obtener_area_ventana(nombre_proceso):
    try:
        ventana = win32gui.FindWindow(None, nombre_proceso)
        if not ventana:
            raise ValueError(f"Ventana '{nombre_proceso}' no encontrada.")

        rect = win32gui.GetWindowRect(ventana)
        return ajustar_area_ventana(rect)
    except Exception as e:
        print(f"Error al obtener el área de la ventana: {e}")
        return None
#"eca/meta1.png", "eca/meta2.png","eca/meta4.png","eca/meta5.png"
grupos_imagenes = {
    "grupo1": {
        "imagenes": ["eca/meta.png"],
        "accion": lambda posicion: (
            raton_posicion(posicion[0] + 140, posicion[1]),
            keyboard.press_and_release("."),
            time.sleep(1),
            keyboard.press_and_release(","),
            time.sleep(0.9),
            keyboard.press_and_release("."),
            time.sleep(1),
            keyboard.press_and_release(","),
            time.sleep(0.9),
            keyboard.press_and_release("."),
            time.sleep(1),
            keyboard.press_and_release(","),
            time.sleep(0.9),
        )
    },
    # "grupo1_1": {
    #     "imagenes": ["eca/meta3.png"],
    #     "accion": lambda posicion: (
    #         raton_posicion(posicion[0] + 99, posicion[1]),
    #         pyautogui.mouseDown(button='left'),
    #         time.sleep(0.5),
    #         pyautogui.mouseUp(button='left')
    #     )
    # },
    "grupo2": {
        "imagenes": ["eca/fin.png","eca/fin1.png","eca/fin1_1.png","eca/fin1_2.png","eca/fin1_3.png","eca/fin1_4.png"],
        "accion": lambda posicion: (
            raton_posicion(posicion[0] + 70, posicion[1]-100),
            keyboard.press_and_release("."),
            time.sleep(1),
            keyboard.press_and_release(","),
            time.sleep(0.9),
            keyboard.press_and_release("."),
            time.sleep(1),
            keyboard.press_and_release(","),
            time.sleep(0.9),
            keyboard.press_and_release("."),
            time.sleep(1),
            keyboard.press_and_release("z")
        )
    },
    "grupo3": {
        "imagenes": ["eca/fin2.png"],
        "accion": lambda posicion: (
            raton_posicion(posicion[0] + 110, posicion[1] - 100)
        )
    },
    "grupo4": {
        "imagenes": ["eca/fin4.png"],
        "accion": lambda posicion: (
            raton_posicion(posicion[0] + 180, posicion[1] - 100)
        )
    },
}

def buscar_y_actuar_en_ventana(nombre_proceso, grupos_imagenes, intervalo=0.05):
    print("Buscando imágenes en tiempo real en la ventana especificada. Presiona Ctrl+C para detener.")

    coordenadas_guardadas = None
    clic_continuo = False
    ultima_ejecucion_grupo1 = time.time()

    def buscar_en_grupo(grupo, area_ventana):
        for imagen_path in grupos_imagenes[grupo]["imagenes"]:
            encontrado, posicion = buscar_imagen_en_pantalla2(imagen_path, area=area_ventana)
            if encontrado:
                return True, posicion
        return False, None

    while True:
        if buscar_imagen_en_pantalla("login/cabal.png"):
            break

        global lanzabuff, puertita, meta, fail
        area_ventana = obtener_area_ventana(nombre_proceso)
        if not area_ventana:
            continue

        resultados = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(buscar_en_grupo, grupo, area_ventana): grupo
                       for grupo in ["grupo1", "grupo2", "grupo3", "grupo4"]} #, "grupo1_1"
            for future in concurrent.futures.as_completed(futures):
                grupo = futures[future]
                resultados[grupo] = future.result()

        for grupo, (encontrado, posicion) in resultados.items():
            if encontrado:
                print(f"Imagen del grupo {grupo} detectada en la ventana {nombre_proceso}.")
                grupos_imagenes[grupo]["accion"](posicion)

                if grupo in ["grupo1"]: #, "grupo1_1"
                    coordenadas_guardadas = posicion
                    clic_continuo = False
                    grupok = 0 if grupo == "grupo1" else 1
                    ultima_ejecucion_grupo1 = time.time()
                elif grupo == "grupo2":
                    meta = False
                    clic_continuo = False
                    return  # Salimos de la función

        if clic_continuo:
            tiempo_espera = time.time() - ultima_ejecucion_grupo1
            if tiempo_espera > 40:
                clic_continuo = False
            else:
                print(f"Continuando clic en las coordenadas guardadas: {coordenadas_guardadas}")
                offset = 140 if grupok == 0 else 99
                raton_posicion(coordenadas_guardadas[0] + offset, coordenadas_guardadas[1])
                pyautogui.click(button='left')

        if lanzabuff == 1 or puertita == 1 or fail is not False:
            break

        time.sleep(intervalo)
def funcionmuerte():
    global stop_flag, dungeon, nombre_proceso, tiempo_inicio, puerta, grupos_imagenes, muriendo, lanzabuff, terminar, meta, puertita, fail, atacar, contadormostruos1
#, "eca/meta1.png", "eca/meta2.png", "eca/meta3.png"

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionmuerte en ejecución")
        time.sleep(1)

        muerte = buscar_imagen_en_pantalla("otros/wrap-dead.bmp")

        if fail:
            muriendo = 0
            continue

        if muerte and dungeon == 1 and not terminar and not fail:
            print('muerte')
            muriendo = 1
            click_raton_posicion(muerte[0], muerte[1])

            confirmar_muerte = buscar_imagen_en_pantalla("otros/confirmar_muerte.png")
            if confirmar_muerte and not fail:
                print('confirmar_muerte')
                click_raton_posicion(confirmar_muerte[0], confirmar_muerte[1])
                time.sleep(3)
                lanzabuff = atacar = 0

                centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                if centro_ventana2:
                    time.sleep(1)
                    for _ in range(4):
                        keyboard.press("ctrl")
                        keyboard.press_and_release("a")
                        time.sleep(1)
                    keyboard.release("ctrl")
                    time.sleep(1)
                    # buscar_y_actuar_en_ventana(nombre_proceso, grupos_imagenes)
                    centro_ventana3 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana3:
                        print(f"El centro de la ventana3 de {nombre_proceso} es ({centro_ventana3[0]}, {centro_ventana3[1]}).")
                        angulo = math.radians(50)

                        # Calcular desplazamiento en X e Y
                        delta_x = int(350 * math.cos(angulo))
                        delta_y = int(350 * math.sin(angulo))

                        # Calcular nueva posición
                        nueva_x = centro_ventana3[0] + delta_x  # Mover a la derecha
                        nueva_y = centro_ventana3[1] - delta_y  # Mover hacia abajo (por -sin)

                        raton_posicion(nueva_x, nueva_y)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                        
                        imagenes_a_buscar = ["eca/fin.png","eca/fin1.png","eca/fin1_1.png","eca/fin1_2.png","eca/fin1_3.png","eca/fin1_4.png","eca/fin1_5.png","eca/fin1_6.png","eca/fin1_7.png"]
                        encontrada_imagen = False

                        while not encontrada_imagen:
                            for imagen in imagenes_a_buscar:
                                elemento = buscar_imagen_en_pantalla(imagen)
                                if elemento:
                                    angulo = math.radians(165)

                                    # Calcular desplazamiento en X e Y
                                    delta_x = int(350 * math.cos(angulo))
                                    delta_y = int(350 * math.sin(angulo))

                                    # Calcular nueva posición
                                    nueva_x = centro_ventana3[0] + delta_x  # Mover a la derecha
                                    nueva_y = centro_ventana3[1] - delta_y  # Mover hacia abajo (por -sin)

                                    raton_posicion(nueva_x, nueva_y)
                                    keyboard.press_and_release(".")
                                    time.sleep(1)
                                    keyboard.press_and_release(",")
                                    time.sleep(0.9)
                                    keyboard.press_and_release(".")
                                    time.sleep(1)
                                    keyboard.press_and_release(",")
                                    time.sleep(0.9)
                                    keyboard.press_and_release(".")
                                    time.sleep(1)
                                    keyboard.press_and_release("z")
                                    meta = False
                                    encontrada_imagen = True
                                    break

                            if not encontrada_imagen:
                                imagen_a_buscar_piso = "key/piso.png"  # Reemplaza con la ruta de tu propia imagen
                                piso = buscar_imagen_en_pantalla(imagen_a_buscar_piso)
                                time.sleep(0.5)
                                if piso!= False:
                                    print('piso')
                                    click_raton_posicion (piso[0], piso[1])
                                    time.sleep(2)
                                else:
                                    keyboard.press_and_release(",")
                                    time.sleep(0.9)
                                print("No se encontró ninguna imagen en la lista.")

                    centro_ventana2 = False
                    muriendo = 0

    print("funcionmuerte terminada")

def imagennoentrar():
    imagen_a_buscar = "otros/no_entrada.png"  # Reemplaza con la ruta de tu propia imagen
    pos = buscar_imagen_en_pantalla(imagen_a_buscar)
    if pos== False:
        return False
    else:
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

def buscar_y_procesar_imagen(imagenes, offset_x=140, offset_y=0):
    """
    Busca una lista de imágenes en pantalla y, si se encuentra alguna, mueve el ratón y retorna True.
    """
    for imagen in imagenes:
        resultado = buscar_imagen_en_pantalla(imagen)
        if resultado:
            raton_posicion(resultado[0] + offset_x, resultado[1] + offset_y)
            print(f"{imagen} encontrado")
            return True
    return False


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



def funcioiniciar():
    global stop_flag, contardg,accion_realizada, terminar, wavecuenta, esperandocuenta, bosscuenta, dungeon, nombre_proceso, bosdetectado
    global tiempo_inicio, grupos_imagenes, puertita, conteocabal, tronco, tronco2, meta, terminando, pase, atacar, lanzabuff, puerta



    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcioiniciar en ejecución")
        time.sleep(1)

        imagen_a_buscar_salix = "otros/salix.png"  # Reemplaza con la ruta de tu propia imagen
        salix = buscar_imagen_en_pantalla(imagen_a_buscar_salix)
        time.sleep(0.5)
        imagen_a_buscar_iniciar = "otros/iniciar.png"  # Reemplaza con la ruta de tu propia imagen
        iniciar2 = buscar_imagen_en_pantalla(imagen_a_buscar_iniciar)
        time.sleep(0.5)
        if not iniciar2 and dungeon!=2 and  salix and puertita==0 and esperandocuenta < 13:
            dungeon=1
            atacar=1
            lanzabuff=1
        # else:
        #     if puertita==1:
        #         atacar=0
        #         lanzabuff=0

        imagen_a_buscar_confirmasalir = "otros/confirmasalir.png"  # Reemplaza con la ruta de tu propia imagen
        confirmasalir = buscar_imagen_en_pantalla(imagen_a_buscar_confirmasalir)
        time.sleep(0.5)
        if confirmasalir:
            accion_realizada = False
            dungeon=0
            atacar=0
            lanzabuff=0
            esperandocuenta=0
            print("kong27")


        # Handle cerrarmen
        cerrarmen = buscar_imagen_en_pantalla("otros/cerrarmen.png")
        if cerrarmen and dungeon == 0 and not buscar_imagen_en_pantalla("otros/selectdg.png"):
            while True:
                if buscar_imagen_en_pantalla("login/cabal.png"):
                    break
                imagen_a_buscar_salirdg = "otros/salirdg.png"
                salirdg = buscar_imagen_en_pantalla(imagen_a_buscar_salirdg)
                time.sleep(1.5)
                if salirdg != False:
                    print('salirdg1')
                    click_raton_posicion(salirdg[0], salirdg[1])
                click_imagen(cerrarmen)
                cerrarmen = buscar_imagen_en_pantalla("otros/cerrarmen.png")
                if not cerrarmen:
                    break

        # Handle comentarios
        comentarios = buscar_imagen_en_pantalla("otros/comentarios.png")
        puerta = buscar_imagen_en_pantalla("otros/puerta.png")
        if comentarios and puertita == 0 and not meta and not puerta and not buscar_imagen_en_pantalla("otros/selectdg.png"):
            click_imagen(comentarios, offset_y=-10)
            poder = buscar_imagen_en_pantalla("login/poder.png")
            if poder:
                click_imagen(poder)

        # Handle party
        party = buscar_imagen_en_pantalla("otros/party.png")
        party1 = buscar_imagen_en_pantalla("otros/party1.png")
        if party and party1 and dungeon == 0:
            click_imagen(party)

        # Check various login states
        account_login = buscar_imagen_en_pantalla("login/account-login.bmp")
        character_list = buscar_imagen_en_pantalla("login/character-list.bmp")
        recuperardg = buscar_imagen_en_pantalla("otros/recuperardg.png")
        okrecuperar = buscar_imagen_en_pantalla("otros/okrecuperar.png")
        duallogin = buscar_imagen_en_pantalla("login/duallogin.png")

        if okrecuperar and conteocabal == 1:
            click_imagen(okrecuperar)
            time.sleep(4)

        if (dungeon == 0 and not terminar and
            not any([account_login, character_list, recuperardg, duallogin, okrecuperar])):
            centro_ventana = obtener_centro_ventana(nombre_proceso)
            if centro_ventana:
                reset_variables()
                handle_bm_clicks()
                handle_tronco()
                handle_dungeon_selection()

        # Handle dungeo
        dungeo = buscar_imagen_en_pantalla("otros/dungeo.png")
        fail = buscar_imagen_en_pantalla("otros/fail.png")
        #   "eca/meta1.png",
        #         "eca/meta2.png",
        #         "eca/meta3.png"
        if dungeo and not fail:
            # vuelta = 0
            # imagenes_meta = [
            #     "eca/meta.png"
              
            # ]
            # while True:
            #     # Buscar cabal
            #     cabal = buscar_imagen_en_pantalla("login/cabal.png")
            #     if cabal:
            #         print("Cabal encontrado, saliendo del bucle.")
            #         break

            #     time.sleep(0.5)
            #     keyboard.press("ctrl")
            #     keyboard.press_and_release("a")
            #     time.sleep(1.2)
            #     keyboard.release("ctrl")
            #     time.sleep(0.5)
            #     vuelta += 1
            #     time.sleep(0.5)
            #     meta = buscar_imagen_en_pantalla("eca/meta.png")
            #     if meta:
            #         break

            #     # Buscar meta en lista de imágenes
            #     # meta = buscar_y_procesar_imagen(imagenes_meta)
            #     # if meta:
            #     #     break

            #     # Limitar el número de intentos
            #     if vuelta == 6:
            #         print("Se alcanzó el límite de intentos, saliendo del bucle.")
            #         vuelta = 0
            #         break
            iniciar = imageniniciar()
            imagen_a_buscar_cerrarmen = "otros/cerrarmen.png"  # Reemplaza con la ruta de tu propia imagen
            cerrarmen = buscar_imagen_en_pantalla(imagen_a_buscar_cerrarmen)
            time.sleep(0.5)
            imagen_a_buscar_comentarios1 = "otros/comentarios1.png"  # Reemplaza con la ruta de tu propia imagen
            comentarios1 = buscar_imagen_en_pantalla(imagen_a_buscar_comentarios1)
            time.sleep(0.5)
        
                
            if iniciar!= False  and not (comentarios1 and cerrarmen):
                click_raton_posicion(iniciar[0], iniciar[1])
                lanzabuff = 0
                pase = 0
                dungeon = 1
                conteocabal = 0
                esperandocuenta = 0
                contardg += 1
                time.sleep(1)
                for _ in range(4):
                    keyboard.press("ctrl")
                    keyboard.press_and_release("a")
                    time.sleep(1)
                keyboard.release("ctrl")
                time.sleep(1)
                # buscar_y_actuar_en_ventana(nombre_proceso, grupos_imagenes)
                centro_ventana3 = obtener_centro_ventana(nombre_proceso)
                if centro_ventana3:
                    print(f"El centro de la ventana3 de {nombre_proceso} es ({centro_ventana3[0]}, {centro_ventana3[1]}).")
                    angulo = math.radians(50)

                    # Calcular desplazamiento en X e Y
                    delta_x = int(350 * math.cos(angulo))
                    delta_y = int(350 * math.sin(angulo))

                    # Calcular nueva posición
                    nueva_x = centro_ventana3[0] + delta_x  # Mover a la derecha
                    nueva_y = centro_ventana3[1] - delta_y  # Mover hacia abajo (por -sin)

                    raton_posicion(nueva_x, nueva_y)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    
                    imagenes_a_buscar = ["eca/fin.png","eca/fin1.png","eca/fin1_1.png","eca/fin1_2.png","eca/fin1_3.png","eca/fin1_4.png","eca/fin1_5.png","eca/fin1_6.png","eca/fin1_7.png"]
                    encontrada_imagen = False

                    while not encontrada_imagen:
                        for imagen in imagenes_a_buscar:
                            elemento = buscar_imagen_en_pantalla(imagen)
                            if elemento:
                                angulo = math.radians(165)

                                # Calcular desplazamiento en X e Y
                                delta_x = int(350 * math.cos(angulo))
                                delta_y = int(350 * math.sin(angulo))

                                # Calcular nueva posición
                                nueva_x = centro_ventana3[0] + delta_x  # Mover a la derecha
                                nueva_y = centro_ventana3[1] - delta_y  # Mover hacia abajo (por -sin)

                                raton_posicion(nueva_x, nueva_y)
                                keyboard.press_and_release(".")
                                time.sleep(1)
                                keyboard.press_and_release(",")
                                time.sleep(0.9)
                                keyboard.press_and_release(".")
                                time.sleep(1)
                                keyboard.press_and_release(",")
                                time.sleep(0.9)
                                keyboard.press_and_release(".")
                                time.sleep(1)
                                keyboard.press_and_release("z")
                                meta = False
                                encontrada_imagen = True
                                break

                        if not encontrada_imagen:
                            imagen_a_buscar_piso = "key/piso.png"  # Reemplaza con la ruta de tu propia imagen
                            piso = buscar_imagen_en_pantalla(imagen_a_buscar_piso)
                            time.sleep(0.5)
                            if piso!= False:
                                print('piso')
                                click_raton_posicion (piso[0], piso[1])
                                time.sleep(2)
                            else:
                                keyboard.press_and_release(",")
                                time.sleep(0.9)
                            print("No se encontró ninguna imagen en la lista.")

            else:
                imagen_a_buscar_salirdg = "otros/salirdg.png"
                salirdg = buscar_imagen_en_pantalla(imagen_a_buscar_salirdg)
                time.sleep(1.5)
                if salirdg != False:
                    print('salirdg1')
                    click_raton_posicion(salirdg[0], salirdg[1])
        # ... (rest of the dungeo handling logic)

    print("funcioiniciar terminada")

def reset_variables():
    global dungeon, central, esperandocuenta, wavecuenta, bosscuenta, terminando, atacar, cuenta, bosdetectado, terminar, tiempo_inicio
    dungeon = central = esperandocuenta = wavecuenta = bosscuenta = terminando = atacar = cuenta = bosdetectado = 0
    terminar = False
    tiempo_inicio = time.time()

def handle_bm_clicks():
    for bm in ["bm3WI1", "bm2WI1"]:
        imagen = buscar_imagen_en_pantalla(f"otros/{bm}.png")
        if imagen:
            click_imagen(imagen, offset_y=5, button='right', clicks=2)
            time.sleep(1)

def handle_tronco():
    confirmatronco = buscar_imagen_en_pantalla("eca/confirmatronco.png")
    if confirmatronco:
        pyautogui.scroll(-10000)
        click_imagen(confirmatronco, offset_x=-680, offset_y=165)
        time.sleep(3)

def handle_dungeon_selection():
    selectdg = buscar_imagen_en_pantalla("otros/selectdg.png")
    if selectdg:
        dgproceso = buscar_imagen_en_pantalla("otros/dgproceso.png")
        if dgproceso:
            global dungeon, atacar, lanzabuff
            dungeon = atacar = lanzabuff = 1
            time.sleep(0.5)

        eca = imagenEca()
        if eca:
            print('clic eca')
            noentrar = imagennoentrar()
            entrar = imagenentrar()
            time.sleep(2)
            if noentrar:
                print('clic no entrar1')
                global stop_flag
                stop_flag = True
                os.system("shutdown /s /t 10")
                return
            elif entrar:
                click_imagen(entrar)
                print('clic entrar7')
        

        time.sleep(1)

def click_imagen(imagen, offset_x=0, offset_y=0, button='left', clicks=1):
    raton_posicion(imagen[0] + offset_x, imagen[1] + offset_y)
    time.sleep(0.5)
    pyautogui.click(button=button, clicks=clicks)

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
def funcionterminar():

    global stop_flag
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionterminar en ejecución")
        global terminar
        global dungeon
        global bosdetectado
        global vidamostruo
        global puerta
        global terminando
        global esperandocuenta
        global wavecuenta
        global bosscuenta
        global lanzabuff
        global nombre_proceso
        global tiempo_inicio
        global contardgok
        global atacar
        time.sleep(1)
        terminar = imagenterminar()

        if terminar!= False:
                print('Terminando')
                terminando=1
                imagen_a_buscar_bm2WI1 = "otros/bm2WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm2WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2WI1)

                imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                time.sleep(1)
                if bm3WI1!=False:
                    raton_posicion (bm3WI1[0], bm3WI1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    pyautogui.click(button='right')
                    time.sleep(0.5)
                    pyautogui.click(button='right')
                time.sleep(1)
                if bm2WI1!=False:
                    raton_posicion (bm2WI1[0], bm2WI1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    pyautogui.click(button='right')
                    time.sleep(0.5)
                    pyautogui.click(button='right')
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                time.sleep(0.5)
                keyboard.press_and_release("space")
                imagen_a_buscar_bm2WI1 = "otros/bm2WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm2WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2WI1)

                imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                if bm2WI1==False and bm3WI1==False:
                    click_raton_posicion (terminar[0], terminar[1])
                    time.sleep(1.5)

        imagen_a_buscar_dungeo = "otros/dungeo.png"  # Reemplaza con la ruta de tu propia imagen
        dungeo = buscar_imagen_en_pantalla(imagen_a_buscar_dungeo)
        fail = buscar_imagen_en_pantalla("otros/fail.png")
        time.sleep(0.5)
        if dungeo!=False and dungeon==1 and fail!=False:
            dungeon=2
            bosdetectado=0
            terminando=0
            contardgok=contardgok+1
            atacar=0
            esperandocuenta=0
            wavecuenta=0
            bosscuenta=0
            lanzabuff=0
            tiempo_inicio = time.time()
            time.sleep(1.5)

        if dungeon==2 and dungeo!=False:
            imagen_a_buscar_recibir = "otros/recibir.png"  # Reemplaza con la ruta de tu propia imagen
            recibir = buscar_imagen_en_pantalla(imagen_a_buscar_recibir)
            time.sleep(1.5)
            if recibir!= False:
                click_raton_posicion (recibir[0], recibir[1])
            imagen_a_buscar_dado = "otros/dado.png"  # Reemplaza con la ruta de tu propia imagen
            dado = buscar_imagen_en_pantalla(imagen_a_buscar_dado)
            time.sleep(1.5)
            if dado!= False:
                print('salir1')
                click_raton_posicion (dado[0], dado[1])
                time.sleep(0.5)
    print("funcionterminar terminada")

def funcionpuerta():
    global stop_flag

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionpuerta en ejecución")
        global lanzabuff
        global contardg
        global bosfinal
        global dungeon
        global terminar
        global contadormostruos1
        global puertita
        global vidamostruo
        global puerta
        global atacar
        global meta
        global grupo_actual
        global nombre_proceso
        global tiempo_inicio
        global fin2
        time.sleep(1)
        imagen_a_buscar_puerta = "otros/puerta.png"  # Reemplaza con la ruta de tu propia imagen
        puerta = buscar_imagen_en_pantalla(imagen_a_buscar_puerta)
        if puerta != False and dungeon==1:
            print('detecte puerta')
            contadormostruos1=0
            puertita=1
            time.sleep(3)

            keyboard.press_and_release("2")
            keyboard.press_and_release("3")
        else:
            if puertita==1:
                atacar=1
                contadormostruos1=contadormostruos1+1
        centro_ventana3 = obtener_centro_ventana(nombre_proceso)
            # time.sleep(5)
        if centro_ventana3 and puertita==1 and puerta==False and vidamostruo==False:
            keyboard.press_and_release(".")
            time.sleep(1)
            keyboard.press_and_release(",")
            time.sleep(0.9)
            keyboard.press_and_release(".")
            time.sleep(1)
            keyboard.press_and_release(",")
            time.sleep(0.9)
            keyboard.press_and_release(".")
            time.sleep(1)
            keyboard.press_and_release("z")
            print('fin de puerta')
            time.sleep(0.5)
            keyboard.press_and_release("ctrl+8")
            time.sleep(0.5)
            keyboard.press_and_release("ctrl+7")
            centro_ventana3 =False
            puerta=False
            lanzabuff=1
            puertita=0
            atacar=1
            meta=False
            bosdetectado=0
            time.sleep(0.5)
                # x, y = pyautogui.position()

                # # new_x = x -95
                # # new_y = y -50

                # # pyautogui.moveTo(new_x, new_y)
                # while True:
                #     imagen_a_buscar_cabal = "login/cabal.png"  # Reemplaza con la ruta de tu propia imagen
                #     cabal = buscar_imagen_en_pantalla(imagen_a_buscar_cabal)
                #     if cabal!=False :
                #         break
                #     posicion_actual = pyautogui.position()
                #     pyautogui.click(button='left')

                #     time.sleep(0.5)
                #     keyboard.press_and_release(".")
                #     time.sleep(1)
                #     keyboard.press_and_release(",")
                #     time.sleep(0.9)

                #     keyboard.press_and_release("z")
                #     time.sleep(1)
                #     vidamostruo = imagenmostruo()
                #     if vidamostruo!= False:
                #         print('fin de puerta')

                #         # time.sleep(0.5)
                #         # keyboard.press_and_release(".")
                #         # time.sleep(1)
                #         # keyboard.press_and_release(",")
                #         # time.sleep(0.9)

                #         time.sleep(0.5)
                #         keyboard.press_and_release("ctrl+8")
                #         time.sleep(0.5)
                #         keyboard.press_and_release("ctrl+7")
                #         time.sleep(0.5)
                #         keyboard.press_and_release("f12")
                #         time.sleep(0.5)
                #         keyboard.press_and_release("f12")
                #         centro_ventana3 =False
                #         puerta=False
                #         lanzabuff=1
                #         puertita=0
                #         atacar=1
                #         meta=False
                #         bosdetectado=0
                #         time.sleep(0.5)
                #         if atacar==1 and puertita==0:
                #             break
    print("funcionpuerta terminada")

# Inicializar la variable de parada
stop_flag = False
contardg=0
contardgok=0
contadormostruos1=0
dungeon=0
wavecuenta=0
bosscuenta=0
bosdetectado=0
conteocabal=0
puerta=0
central=0
puertita=0
muriendo=0
terminando=0
bos1_namedetectado=0
cuenta=0
pase=0
contarwave=0
esperandocuenta=0
contarboss=0
terminar=False
meta=False
vidamostruo=False
tronco=False
tronco2=False
bm3WI1=False
bm2WI1=False
lanzabuff=0
bosfinal=False
accion_realizada = False  # Variable para controlar si ya se ha realizado la acción

fail = False
atacar=0
nombre_proceso = "cabal"
grupo_actual="grupo1"
tiempo_inicio = time.time()
# buscar_y_actuar_en_ventana(nombre_proceso, grupos_imagenes)
# Lista de funciones a ejecutar
funciones = [
    funciologin,
    funcionSP,
    funcionvida,
    funcionmostruo,
    funcionmostruoeca,
    funcionBM,
    funcionBM2,
    funcionBM3,
    funcionfail,
    funcionmuerte,
    funcioiniciar,
    funcionterminar,
    funcionpuerta
    ]

def ejecutar_funcion(funcion):
    """Ejecuta una función continuamente hasta que se active stop_flag."""
    global stop_flag
    while not stop_flag:
        try:
            funcion()
        except Exception as e:
            print(f"Error en {funcion.__name__}: {e}")
        time.sleep(0.1)  # Pequeña pausa para evitar uso excesivo de CPU

def detener_todo():
    """Detener todas las funciones."""
    global stop_flag
    while not stop_flag:
        if keyboard.is_pressed('end'):
            stop_flag = True
            print("Parando todas las funciones...")
            break
        time.sleep(0.1)

def ejecutar_funciones():
    global stop_flag
    stop_flag = False

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(funciones)) as executor:
        # Iniciar todas las funciones
        futuros = [executor.submit(ejecutar_funcion, funcion) for funcion in funciones]

        # Esperar a que todas las funciones terminen o se active stop_flag
        concurrent.futures.wait(futuros, return_when=concurrent.futures.FIRST_COMPLETED)

if __name__ == "__main__":
    try:
        # Iniciar el hilo para detectar la tecla 'end'
        hilo_tecla_end = threading.Thread(target=detener_todo, daemon=True)
        hilo_tecla_end.start()

        # Ejecutar las funciones
        ejecutar_funciones()
    except KeyboardInterrupt:
        print("Programa interrumpido manualmente.")
    finally:
        stop_flag = True
        print("Ejecución terminada.")