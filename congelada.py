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

import tkinter as tk
from tkinter import ttk
contardg=contadormostruos1= atacar= etapa=contardgok=0
piso=""

def crear_ventana_info():
    global  contardg, atacar, etapa,contardgok, piso,contadormostruos1 
    ventana = tk.Tk()
    ventana.title("Información en tiempo real")
    ventana.geometry("300x150")

    etiqueta_sp = ttk.Label(ventana, text="Número de sp: ")
    etiqueta_sp.pack()

    etiqueta_dg = ttk.Label(ventana, text="DG: ")
    etiqueta_dg.pack()

    etiqueta_dgok = ttk.Label(ventana, text="DG OK: ")
    etiqueta_dgok.pack()

    etiqueta_atacar = ttk.Label(ventana, text="Atacar: ")
    etiqueta_atacar.pack()

    etiqueta_mostruos = ttk.Label(ventana, text="Mostruos: ")
    etiqueta_mostruos.pack()

    etiqueta_piso = ttk.Label(ventana, text="Piso: ")
    etiqueta_piso.pack()

    etiqueta_etapa = ttk.Label(ventana, text="Etapa inicial: ")
    etiqueta_etapa.pack()


    def actualizar_info():
        global  contardg, atacar, etapa,contardgok, piso,contadormostruos1
        etiqueta_dg.config(text=f"DG : {contardg}")
        etiqueta_dgok.config(text=f"DG ok: {contardgok}")
        etiqueta_atacar.config(text=f"Atacar: {atacar}")
        etiqueta_mostruos.config(text=f"Mostruos: {contadormostruos1}")
        etiqueta_piso.config(text=f"Piso: {piso}")
        etiqueta_etapa.config(text=f"Etapa inicial: {etapa}")
        ventana.after(1000, actualizar_info)  # Actualizar cada segundo

    actualizar_info()
    return ventana
# Crear la ventana en un hilo separado
ventana_info = None
def iniciar_ventana_info():
    global ventana_info
    ventana_info = crear_ventana_info()
    ventana_info.mainloop()

thread_ventana = threading.Thread(target=iniciar_ventana_info)
thread_ventana.start()

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
    global stop_flag, conteocabal, puerta, contardg,etapa, contardgok, cuenta, lanzabuff, wavecuenta, esperandocuenta, dungeon, atacar, contadormostruos1, bosscuenta, tiempo_transcurrido

    last_print_time = time.time()
    last_buff_time = time.time()
    print_interval = 5  # Print every 5 seconds
    buff_interval = 10  # Check buff every 10 seconds

    while not stop_flag and not keyboard.is_pressed('delete'):
        current_time = time.time()
        ctns = []  # Inicializar ctns como una lista vacía

        if atacar == 1:
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
                if len(ctns)==0 :
                    keyboard.press_and_release("-")

        # Imprimir información de estado cada 5 segundos
        if current_time - last_print_time >= print_interval:
            print(f"funcionSP en ejecución\n"
                  f"Número de sp: {len(ctns)}, conteocabal: {conteocabal}, DG1: {contardg}, DGOK: {contardgok}, etapa: {etapa}\n"
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
    global stop_flag, contadormostruos1, bosfinal, dungeon, puerta, terminar, bosdetectado
    global terminando, lanzabuff, puertita, vidamostruo, fail

    while not stop_flag and not keyboard.is_pressed('delete'):
        if dungeon != 1 or atacar == 0:
            time.sleep(0.5)
            continue

        print("funcionmostruo en ejecución")

        # Realizar todas las búsquedas de imágenes de una vez
        vidamostruo = imagenmostruo()

        if vidamostruo:
            contadormostruos1 = 0
            print('variable atacar')
            if vidamostruo <= 15 and not bosdetectado:
                keyboard.press_and_release("z")
        else:
            keyboard.press_and_release("z")
            contadormostruos1 += 1
            # Verificar vida y puerta solo si no se detectó vida antes
            vidamostruo = imagenmostruo()

        time.sleep(0.1)  # Pequeña pausa para evitar sobrecarga de CPU

    print("funcionmostruo terminada")


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
    global stop_flag, bm3WI1, bm2WI1, vidamostruo, dungeon, tiempo_transcurrido, tiempo_inicio,atacar

    imagen_presente = False

    while not stop_flag and not keyboard.is_pressed('delete'):
        if dungeon == 0 or dungeon == 2 : #or final == 1
            time.sleep(0.5)
            continue
        print("funcionBM en ejecución")

        tiempo_transcurrido = time.time() - tiempo_inicio

        bm2WI = buscar_imagen_en_pantalla("otros/bm2WI.png")
        bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
        bm2WI2 = buscar_imagen_en_pantalla("otros/bm2WI2.png")
        bm3WI = buscar_imagen_en_pantalla("otros/bm3WI.png")
        bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
        bm3WI2 = buscar_imagen_en_pantalla("otros/bm3WI2.png")


        if bm3WI and vidamostruo  and not (bm3WI1 or bm2WI1):
            keyboard.press_and_release("f12")
            time.sleep(0.5)
            keyboard.press_and_release("f12")

        if bm2WI and vidamostruo  and not (bm3WI1 or bm2WI1):
            keyboard.press_and_release("f10")
            time.sleep(0.5)
            keyboard.press_and_release("f10")

    print("funcionBM terminada")

def funcionBM2():
    global stop_flag, bm3WI1, dungeon, nombre_proceso, vidamostruo, puerta, atacar, puertita, bosdetectado

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM2 en ejecución")
        time.sleep(0.3)  # Reduced sleep time

        if not (vidamostruo and dungeon == 1 and atacar == 1 )  :
            continue


        if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
            continue

        if buscar_imagen_en_pantalla("login/cabal.png"):
            continue

        bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
        mago = buscar_imagen_en_pantalla("otros/mago.png")

        if bm2WI1 and not mago:
            for _ in range(10):  # Limit the number of attempts
                keyboard.press_and_release("6")
                keyboard.press_and_release("space")
                time.sleep(0.2)
                if not buscar_imagen_en_pantalla("otros/bm2WI1.png"):
                    break

        print('ataque normal con monstruos')
        if  (bm2WI1 and mago): #not bm2WI1 or
            for tecla in ["2", "3", "4", "8"]:
                keyboard.press_and_release(tecla)
                keyboard.press_and_release("space")
                time.sleep(0.2)

                if buscar_imagen_en_pantalla("otros/bm3WI1.png") or not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                    keyboard.press_and_release("space")
                    break

    print("funcionBM2 terminada")


def funcionBM3():
    global stop_flag, bm3WI1, dungeon, vidamostruo, atacar

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM3 en ejecución")
        time.sleep(0.5)  # Reducido de 1 a 0.5 segundos

        if dungeon == 0 or dungeon == 2:
            time.sleep(0.5)
            continue

        if not (vidamostruo and dungeon == 1) and not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
            continue

        bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
        if not bm3WI1:
            continue

        ataque_count = 0
        max_ataques = 15  # Límite de ataques antes de verificar condiciones nuevamente

        while ataque_count < max_ataques and dungeon == 1:
            if buscar_imagen_en_pantalla("login/cabal.png"):
                break

            if dungeon == 0 or dungeon == 2:
                break

            print('ataque BM3 con monstruos')
            keyboard.press_and_release("6")
            keyboard.press_and_release("space")
            time.sleep(0.1)  # Reducido de 0.3 a 0.2 segundos

            if not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                break

            vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
            if not vidamostruo:
                break

            ataque_count += 1

    print("funcionBM3 terminada")
def funcionmercenario():
    global stop_flag,  dungeon

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionmercenario en ejecución")
        time.sleep(0.5)  # Reducido de 1 a 0.5 segundos

        if dungeon == 0 or dungeon == 2:
            time.sleep(0.5)
            continue

        M1 = buscar_imagen_en_pantalla("otros/M1.png")
        if M1:
            print("M1 detectado")
        else:
            M1_K = buscar_imagen_en_pantalla("otros/M1_K.png")
            if M1_K:
                print("M1_K detectado")
                keyboard.press('ctrl')
                time.sleep(0.5)
                keyboard.press('8')
                time.sleep(0.5)  
                keyboard.release('8')
                keyboard.release('ctrl')
            else:
                print("Ni M1 ni M1_K fueron detectados")

    print("funcionmercenario terminada")

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
    global stop_flag,muriendo,esperandocuenta,muro2,bosscuenta,wavecuenta, dungeon, nombre_proceso, tiempo_inicio, puerta, terminando, terminar, lanzabuff, puertita, atacar, muriendo, fail

    def reset_variables():
        global dungeon,esperandocuenta,wavecuenta,bosscuenta, bosdetectado, terminando, lanzabuff, atacar, terminar, contardg, puerta, puertita, muriendo, vidamostruo, fin2, meta, bosfinal, tiempo_inicio
        dungeon = 2
        bosdetectado = terminando = lanzabuff = atacar = bosscuenta = wavecuenta  = puerta = puertita = esperandocuenta = muriendo = muriendo = 0
        terminar = fin2 = meta = bosfinal = vidamostruo = muro2 = False
        tiempo_inicio = time.time()

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionfail en ejecución")
        time.sleep(1)
        fail = buscar_imagen_en_pantalla("otros/fail.png")
        if fail:
            if dungeon == 1:
                print('fail')
                click_raton_posicion(fail[0], fail[1])
                reset_variables()
            if dungeon == 2:
                ok = imagenok()
                if ok:
                    print('salir2')
                    click_raton_posicion(ok[0], ok[1])
                    time.sleep(0.5)

    print("funcionfail terminada")

def funcionmuerte():
    global stop_flag, dungeon, nombre_proceso, tiempo_inicio, etapa, muriendo, lanzabuff, terminar, meta, puertita, fail, atacar, contadormostruos1

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
                atacar=0
                etapa = 1


    print("funcionmuerte terminada")

def imagennoentrar():
    ruta_imagen = 'otros/no_entrada.png'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre no_entrada')
        return False
    else:
        print('encontre no_entrada')
        return pos

def imagencongelada():
    ruta_imagen = 'congelada/congelada.png'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre congelada')
        return False
    else:
        print('encontre congelada')
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

def buscar_y_procesar_imagen(imagenes, offset_x=101, offset_y=0):
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
    global stop_flag, contardg, terminar, wavecuenta, esperandocuenta, bosscuenta, dungeon, nombre_proceso, bosdetectado
    global tiempo_inicio, puertita, conteocabal, tronco, tronco2, meta, terminando, pase, atacar, lanzabuff, puerta,etapa

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcioiniciar en ejecución")
        time.sleep(1)
        notice = buscar_imagen_en_pantalla("otros/notice.png")


        imagen_a_buscar_salix = "otros/salix.png"  # Reemplaza con la ruta de tu propia imagen
        salix = buscar_imagen_en_pantalla(imagen_a_buscar_salix)
        time.sleep(0.5)
        imagen_a_buscar_iniciar = "otros/iniciar.png"  # Reemplaza con la ruta de tu propia imagen
        iniciar = buscar_imagen_en_pantalla(imagen_a_buscar_iniciar)
        time.sleep(0.5)
        if not iniciar and  salix and dungeon!=2:
            dungeon=1
        imagen_a_buscar_confirmasalir = "otros/confirmasalir.png"  # Reemplaza con la ruta de tu propia imagen
        confirmasalir = buscar_imagen_en_pantalla(imagen_a_buscar_confirmasalir)
        time.sleep(0.5)
        if confirmasalir!=False:
            dungeon=0

        # Handle cerrarmen
        cerrarmen = buscar_imagen_en_pantalla("otros/cerrarmen.png")
        if cerrarmen and dungeon == 0 and not buscar_imagen_en_pantalla("otros/selectdg.png") and not notice:
            keyboard.press_and_release("esc")
            while True:
                if buscar_imagen_en_pantalla("login/cabal.png"):
                    break
                cerrarmen = buscar_imagen_en_pantalla("otros/cerrarmen.png")
                if not cerrarmen:
                    break
                imagen_a_buscar_salirdg = "otros/salirdg.png"
                salirdg = buscar_imagen_en_pantalla(imagen_a_buscar_salirdg)
                time.sleep(1.5)
                if salirdg != False:
                    print('salirdg1')
                    click_raton_posicion(salirdg[0], salirdg[1])
                click_imagen(cerrarmen)

        # Handle comentarios
        comentarios = buscar_imagen_en_pantalla("otros/comentarios.png")
        puerta = buscar_imagen_en_pantalla("otros/puerta.png")
        if comentarios and puertita == 0 and not buscar_imagen_en_pantalla("otros/selectdg.png"):
            click_imagen(comentarios, offset_y=-10)
            poder = buscar_imagen_en_pantalla("login/poder.png")
            if poder:
                click_imagen(poder)
                keyboard.press_and_release("F1")

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
        

        if okrecuperar and notice :
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

        iniciar = imageniniciar()
        if iniciar != False and not buscar_imagen_en_pantalla("otros/comentarios.png"):
            click_raton_posicion(iniciar[0], iniciar[1])
            lanzabuff = 1
            pase = 0
            dungeon = 1
            etapa=1
            conteocabal = 0
            contardg += 1
            time.sleep(1)
        else:
            imagen_a_buscar_salirdg = "otros/salirdg.png"
            salirdg = buscar_imagen_en_pantalla(imagen_a_buscar_salirdg)
            time.sleep(1.5)
            if salirdg != False:
                print('salirdg1')
                click_raton_posicion(salirdg[0], salirdg[1])


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
    confirmatronco = buscar_imagen_en_pantalla("congelada/confirmatronco.png")
    if confirmatronco:
        
        click_imagen(confirmatronco)
        time.sleep(1)
    else:
        pyautogui.scroll(-10000)

def handle_dungeon_selection():
    global stop_flag
    selectdg = buscar_imagen_en_pantalla("otros/selectdg.png")
    if selectdg:
        dgproceso = buscar_imagen_en_pantalla("otros/dgproceso.png")
        if dgproceso:
            global dungeon, atacar, lanzabuff
            dungeon = atacar = lanzabuff = 1
            time.sleep(0.5)

        congelada = imagencongelada()
        detected = buscar_imagen_en_pantalla("congelada/detected.png")
        if not detected and congelada:
            click_imagen(congelada)
            time.sleep(1)
            raton_posicion(congelada[0], congelada[1]+30)

        if congelada and detected:
            print('clic congelada')
            noentrar = imagennoentrar()
            entrar = imagenentrar()
            time.sleep(2)
            if noentrar:
                print('clic no entrar1')
                stop_flag = True
                # os.system("shutdown /s /t 10")
                return
            elif entrar:
                click_imagen(entrar)
                print('clic entrar')
        else:
            noentrar = imagennoentrar()
            time.sleep(0.3)
            if noentrar:
                print('clic no entrar1')
                stop_flag = True
                # os.system("shutdown /s /t 10")
                return


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
    global stop_flag, terminar,muro2,muriendo, dungeon, bosdetectado, vidamostruo, puerta, terminando, lanzabuff, nombre_proceso, tiempo_inicio, contardgok, atacar

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionterminar en ejecución")
        time.sleep(0.5)
        terminar = imagenterminar()

        if terminar:
            print('Terminando')
            terminando = 1
            bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
            bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")

            for bm in [bm3WI1, bm2WI1]:
                    if bm:
                        raton_posicion(bm[0], bm[1]+5)
                        pyautogui.mouseDown(button='right')
                        time.sleep(1)  # Mantener el botón presionado por 0.2 segundos
                        pyautogui.mouseUp(button='right')
                        time.sleep(0.5)
                        pyautogui.click(button='right')

            for _ in range(6):
                keyboard.press_and_release("space")
                time.sleep(0.3)

            if not buscar_imagen_en_pantalla("otros/bm2WI1.png") and not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                click_raton_posicion(terminar[0], terminar[1])
                time.sleep(1.5)

        dungeo = buscar_imagen_en_pantalla("otros/dungeo.png")
        if dungeo and dungeon == 1:
            dungeon, bosdetectado, terminando, atacar, lanzabuff,muro2,muriendo = 2, 0, 0, 0, 0,False,0
            time.sleep(1.5)

        if dungeon == 2 and dungeo:
            imagenes_a_buscar = ["otros/recibir.png", "otros/obtenerpuntos.png", "otros/dado.png"]
            for imagen in imagenes_a_buscar:
                elemento = buscar_imagen_en_pantalla(imagen)
                if elemento:
                    click_raton_posicion(elemento[0], elemento[1])
                    time.sleep(0.3)
                    if imagen == "otros/dado.png":
                        print('salir1')
                        contardgok += 1
                        tiempo_inicio = time.time()
                        dungeon = 0
                        break

                # Verificar si dungeo sigue existiendo después de cada acción
                if not buscar_imagen_en_pantalla("otros/dungeo.png"):
                    print('Dungeo ya no está visible')
                    dungeon = 0
                    break

    print("funcionterminar terminada")

def funcionetapa():
    global stop_flag
    while not stop_flag and not keyboard.is_pressed('delete'):
        global contardg
        global bosfinal
        global dungeon
        global atacar
        global muriendo
        global muroactivado
        global terminar
        global murodetectado
        global muro2
        global contadormostruos1
        global vidamostruo
        global etapa
        global nombre_proceso
        global tiempo_inicio
        print("funcionetapa en ejecución")
        time.sleep(1)
        if etapa>0 and dungeon==1 :
            if etapa==1:
                muroactivado=0
                murodetectado=False
                print('etapa 1')
                piso1 = buscar_imagen_en_pantalla("congelada/piso1.png")
                time.sleep(0.3)
                if piso1!=False:
                    raton_posicion (piso1[0]+30, piso1[1]-50)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    pyautogui.click(button='left')
                    time.sleep(2)
                piso2 = buscar_imagen_en_pantalla("congelada/piso2.png")
                if piso2:
                    atacar=1
                    etapa=2
            if etapa==2 and not vidamostruo:
                print('etapa 2')
                piso2 = buscar_imagen_en_pantalla("congelada/piso2.png")
                if piso2 == False and contadormostruos1>15 and contadormostruos1<30:
                   keyboard.press_and_release("q") 
                if piso2 == False and contadormostruos1>30:
                   keyboard.press_and_release("w") 
                if piso2 == False and contadormostruos1>60:
                   keyboard.press_and_release("s") 
                #     piso2 = buscar_imagen_en_pantalla("congelada/piso2_1.png")
                #     if piso2 == False:
                #         piso2 = buscar_imagen_en_pantalla("congelada/piso2_2.png")
                bos0 = buscar_imagen_en_pantalla("congelada/bos0.png")
                time.sleep(0.3)
                if piso2!=False and bos0==False:
                    raton_posicion (piso2[0], piso2[1])
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    pyautogui.click(button='left')
                    npc = buscar_imagen_en_pantalla("congelada/npc.png")
                    time.sleep(0.3)
                    if npc!=False:
                        for _ in range(6):
                            keyboard.press_and_release("space")
                            time.sleep(0.3)
                        etapa=3
                    else:
                        if contadormostruos1>10 and piso2!=False:
                            etapa=3
            if etapa==3:
                print('etapa 3')
                piso3 = buscar_imagen_en_pantalla("congelada/piso3.png")
                if piso3 == False:
                    piso3 = buscar_imagen_en_pantalla("congelada/piso3_3.png")
                    if piso3 == False and contadormostruos1>10:
                        keyboard.press_and_release("w")
                        time.sleep(0.3)
                        keyboard.press_and_release("s")
                        time.sleep(0.3)
                        keyboard.press_and_release("q")
                    #     piso3 = buscar_imagen_en_pantalla("congelada/piso3_2.png")
                time.sleep(0.3)
                if piso3!=False:
                    raton_posicion (piso3[0]+30, piso3[1]+80)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    pyautogui.click(clicks=2, interval=0.1,button='left')
                    time.sleep(2)
                    etapa=4
                    atacar=0
            if etapa==4:
                print('etapa 3')
                piso3 = buscar_imagen_en_pantalla("congelada/piso3.png")
                if piso3 == False:
                    piso3 = buscar_imagen_en_pantalla("congelada/piso3_3.png")
                    # if piso3 == False:
                    #     piso3 = buscar_imagen_en_pantalla("congelada/piso3_2.png")
                time.sleep(0.3)
                if piso3!=False:
                    raton_posicion (piso3[0]+30, piso3[1]+80)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    pyautogui.click(clicks=2, interval=0.1,button='left')
                    time.sleep(2)
                    etapa=4
                    atacar=0
                print('etapa 4')
                piso4 = buscar_imagen_en_pantalla("congelada/piso4.png")
                if piso4 == False:
                    piso4 = buscar_imagen_en_pantalla("congelada/piso4_1.png")

                time.sleep(0.3)
                if piso4!=False:
                    raton_posicion (piso4[0]-180, piso4[1]+325)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    for _ in range(1):
                        keyboard.press_and_release(",")
                        time.sleep(1)
                        keyboard.press_and_release(".")
                        time.sleep(0.9)
                    time.sleep(0.5)
                    etapa=5
                    atacar=0
            if etapa==5:
                print('etapa 5')
                piso5 = buscar_imagen_en_pantalla("congelada/piso5.png")
                if piso5 == False:
                    piso5 = buscar_imagen_en_pantalla("congelada/piso5_1.png")
                time.sleep(0.3)
                if piso5!=False:
                    raton_posicion (piso5[0]-300, piso5[1]-140)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    for _ in range(1):
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                    time.sleep(0.5)
                    etapa=6
                    atacar=0
            if etapa==6:
                print('etapa 6')
                piso6 = buscar_imagen_en_pantalla("congelada/piso6.png")
                if piso6 == False:
                    piso6 = buscar_imagen_en_pantalla("congelada/piso6_1.png")
                time.sleep(0.3)
                if piso6!=False:
                    raton_posicion (piso6[0], piso6[1])
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    for _ in range(1):
                        keyboard.press_and_release(".")
                        time.sleep(1)
                    time.sleep(0.5)
                    etapa=7
                    atacar=0
            if etapa==7:
                print('etapa 7')

                if muro2==False:
                    muro2 = buscar_imagen_en_pantalla("congelada/muro1.png")

                if muriendo==0:
                    muro1 = buscar_imagen_en_pantalla("congelada/muro1.png")
                    time.sleep(0.3)
                    if muro1!=False and muroactivado==0:
                        raton_posicion (muro1[0], muro1[1]+250)
                        posicion_actual = pyautogui.position()
                        time.sleep(0.3)
                        pyautogui.click(clicks=1, interval=0.1,button='left')
                        bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
                        bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
                        if bm2WI1:
                            keyboard.press_and_release("2")
                            time.sleep(3)
                        if bm3WI1:
                            keyboard.press_and_release("6")
                            time.sleep(0.3)
                            keyboard.press_and_release("6")
                            time.sleep(0.3)
                            keyboard.press_and_release("6")
                            time.sleep(0.3)
                            keyboard.press_and_release("6")
                            time.sleep(0.3)
                        etapa=8
                        atacar=0
                else:
                    raton_posicion (muro2[0], muro2[1]+250)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    etapa=8
                    atacar=0

            if etapa==8:
                print('etapa 8')
                muro1 = buscar_imagen_en_pantalla("congelada/muro1.png")
                if not muro1:
                    for _ in range(4):
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                    time.sleep(0.5)
                    etapa=9
                    keyboard.press_and_release("f11")
                    time.sleep(4)
                    atacar=1
            if etapa==9 and not vidamostruo:
                print('etapa 9')
                piso7 = buscar_imagen_en_pantalla("congelada/piso7.png")
                if piso7 == False:
                    piso7 = buscar_imagen_en_pantalla("congelada/piso7_1.png")
                    if piso7 == False:
                        piso7 = buscar_imagen_en_pantalla("congelada/piso7_2.png")
                time.sleep(0.3)
                if piso7!=False :
                    raton_posicion (piso7[0], piso7[1])
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    pyautogui.click(button='left')
                    npc = buscar_imagen_en_pantalla("congelada/npc.png")
                    time.sleep(0.3)
                    if npc!=False:
                        for _ in range(6):
                            keyboard.press_and_release("space")
                            time.sleep(0.3)
                        etapa=10
                        atacar=0
                    else:
                        if contadormostruos1>30 and piso7!=False:
                            etapa=10
                            atacar=0
                else:
                    if contadormostruos1>30 :
                        keyboard.press_and_release("w")
                        keyboard.press_and_release(".")
            if etapa==10:
                print('etapa 10')
                piso7 = buscar_imagen_en_pantalla("congelada/piso7.png")
                if piso7 == False:
                    piso7 = buscar_imagen_en_pantalla("congelada/piso7_1.png")
                    if piso7 == False:
                        piso7 = buscar_imagen_en_pantalla("congelada/piso7_2.png")
                time.sleep(0.3)
                bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
                bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")

                for bm in [bm3WI1, bm2WI1]:
                    if bm:
                        raton_posicion(bm[0], bm[1]+5)
                        pyautogui.mouseDown(button='right')
                        time.sleep(1)  # Mantener el botón presionado por 0.2 segundos
                        pyautogui.mouseUp(button='right')
                        time.sleep(0.5)
                        pyautogui.click(button='right')
                  
                for _ in range(6):
                    keyboard.press_and_release("space")
                    time.sleep(0.3)
                if piso7!=False and (not buscar_imagen_en_pantalla("otros/bm2WI1.png") and not buscar_imagen_en_pantalla("otros/bm3WI1.png")): # 
                    raton_posicion (piso7[0]-600, piso7[1]+180)
                    for _ in range(3):
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                    keyboard.press_and_release(".")
                    time.sleep(0.5)
                    etapa=11
                else:
                    if contadormostruos1>20 :
                        keyboard.press_and_release("w")
            if etapa==11:
                print('etapa 11')
                decontar=0
                piso8 = buscar_imagen_en_pantalla("congelada/piso8.png")
                print('piso8')
                decontar=(-15)
                if piso8 == False:
                    piso8 = buscar_imagen_en_pantalla("congelada/piso8_1.png")
                    decontar=(-15)
                    print('piso8_1')
                    if piso8 == False:
                        piso8 = buscar_imagen_en_pantalla("congelada/piso8_4.png")
                        print('piso8_4')
                        time.sleep(0.5)
                        # raton_posicion (piso8[0], piso8[1])
                        # pyautogui.click() 
                        decontar=(40)
                    #     # time.sleep(3)
                        # if piso8 == False:.
                        #     piso8 = buscar_imagen_en_pantalla("congelada/piso8_3.png")
                        #     print('piso8_3')
                        #     time.sleep(0.5)
                        #     raton_posicion (piso8[0], piso8[1])
                        #     pyautogui.click()
                        #     decontar=(145)
                        #     time.sleep(3)
                time.sleep(0.3)
                if piso8!=False :
                    raton_posicion (piso8[0]-500, piso8[1]+100-decontar)
                    for _ in range(2):
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                    keyboard.press_and_release(".")
                    # time.sleep(1)
                    time.sleep(0.5)
                    etapa=12
                    atacar=1
                else:
                    if contadormostruos1>50 :
                        keyboard.press_and_release(".")
            if etapa==12 and not vidamostruo:
                print('etapa 12')
                piso9 = buscar_imagen_en_pantalla("congelada/piso9.png")
                if piso9 == False:
                    piso9 = buscar_imagen_en_pantalla("congelada/piso9_1.png")
                    if piso9 == False:
                        piso9 = buscar_imagen_en_pantalla("congelada/piso9_2.png")
                        if piso9 == False:
                            piso9 = buscar_imagen_en_pantalla("congelada/piso9_3.png")
                            if piso9 == False:
                                piso9 = buscar_imagen_en_pantalla("congelada/piso9_4.png")
                                if piso9 == False:
                                    piso9 = buscar_imagen_en_pantalla("congelada/piso9_5.png")
                                    if piso9 == False:
                                        piso9 = buscar_imagen_en_pantalla("congelada/piso9_6.png")
                                        if piso9 == False:
                                            piso9 = buscar_imagen_en_pantalla("congelada/piso9_7.png")
                time.sleep(0.3)
                if piso9==False :
                    if contadormostruos1>30 :
                        keyboard.press_and_release(".")
                if piso9!=False and not vidamostruo and contadormostruos1>10:
                    raton_posicion (piso9[0], piso9[1])
                    posicion_actual = pyautogui.position()
                    time.sleep(0.3)
                    pyautogui.click(button='left')
                    npc = buscar_imagen_en_pantalla("congelada/npc.png")
                    time.sleep(0.3)
                    if npc!=False:
                        for _ in range(6):
                            keyboard.press_and_release("space")

                            time.sleep(0.3)
                        etapa=13
                        atacar=0
                    # else:
                    #     if contadormostruos1>10 and piso9!=False:
                    #         etapa=13


    print("funcionetapa terminada")





# Inicializar la variable de parada
stop_flag = False
contardg=0
contardgok=0
muroactivado=0
etapa=0
dungeon=0
contadormostruos1=0
wavecuenta=0
bosscuenta=0
bosdetectado=0
conteocabal=0
puerta=0
central=0
murodetectado=False
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
muro2=False
bm3WI1=False
bm2WI1=False
lanzabuff=0
bosfinal=False
fail = False
atacar=0
nombre_proceso = "cabal"
grupo_actual="grupo1"
tiempo_inicio = time.time()

# Lista de funciones a ejecutar
funciones = [
    funciologin,
    funcionSP,
    funcionvida,
    funcionmostruo,
    funcionBM,
    funcionBM2,
    funcionBM3,
    funcionfail,
    funcionmuerte,
    funcioiniciar,
    funcionterminar,
    # funcionmercenario,
    funcionetapa
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

def monitorear_funciones(futuros, executor):
    """Monitorea las funciones y las reinicia si han terminado o si ocurre un error."""
    global stop_flag
    while not stop_flag:
        reiniciar_todas = False
        for i, futuro in enumerate(futuros):
            try:
                if futuro.done():
                    if futuro.exception():
                        print(f"Error en la función {funciones[i].__name__}: {futuro.exception()}")
                        reiniciar_todas = True
                        break
                    else:
                        print(f"Función {funciones[i].__name__} terminó normalmente. Reiniciando...")
                        futuros[i] = executor.submit(ejecutar_funcion, funciones[i])
            except Exception as e:
                print(f"Error inesperado al monitorear {funciones[i].__name__}: {e}")
                reiniciar_todas = True
                break

        if reiniciar_todas:
            print("Reiniciando todas las funciones debido a un error...")
            futuros = [executor.submit(ejecutar_funcion, funcion) for funcion in funciones]

        time.sleep(1)  # Revisar cada segundo

def ejecutar_funciones():
    global stop_flag, executor
    stop_flag = False

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(funciones)) as executor:
        # Iniciar todas las funciones
        futuros = [executor.submit(ejecutar_funcion, funcion) for funcion in funciones]

        # Crear el hilo de monitoreo
        hilo_monitoreo = threading.Thread(target=monitorear_funciones, args=(futuros, executor), daemon=True)

        # Iniciar el hilo de monitoreo
        hilo_monitoreo.start()

        # Esperar a que se active stop_flag
        while not stop_flag:
            time.sleep(0.1)

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
