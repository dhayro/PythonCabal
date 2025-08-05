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
contardg=contadormostruos1= atacar= etapa=contardgok=moustruovida=vida_actual=vida_anterior=vida=0
piso=mensaje=""
bos_detected = False

def crear_ventana_info():
    global  contardg, atacar, etapa,contardgok, piso,contadormostruos1,vida,bos_detected,mensaje,moustruovida,vida_actual,vida_anterior
    ventana = tk.Tk()
    ventana.title("Información en tiempo real")
    ventana.geometry("300x350")

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

    etiqueta_vida = ttk.Label(ventana, text="Vida: ")
    etiqueta_vida.pack()

    etiqueta_Vidamostruo = ttk.Label(ventana, text="Vidamostruo: ")
    etiqueta_Vidamostruo.pack()

    etiqueta_etapa = ttk.Label(ventana, text="Etapa inicial: ")
    etiqueta_etapa.pack()


    def actualizar_info():
        global  contardg, atacar, etapa,contardgok, piso,contadormostruos1,vida,bos_detected,mensaje,moustruovida,vida_actual,vida_anterior
        etiqueta_dg.config(text=f"DG : {contardg} bos_detected : {bos_detected}")
        etiqueta_dgok.config(text=f"DG ok: {contardgok} mensaje : {mensaje}" )
        etiqueta_atacar.config(text=f"Atacar: {atacar}")
        etiqueta_mostruos.config(text=f"Mostruos: {contadormostruos1}")
        etiqueta_piso.config(text=f"Piso: {piso}")
        etiqueta_vida.config(text=f"Vida: {vida} ")
        etiqueta_Vidamostruo.config(text=f"Vidamostruo: {moustruovida}")

        etiqueta_etapa.config(text=f"Etapa inicial: {etapa} \n vida_actual: {vida_actual} \n  vida_anterior: {vida_anterior}")
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
            print(f"funcionSP en ejecución\n")
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
    global stop_flag, tiempo_inicio,vida
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
            if vida <= 30:
                keyboard.press_and_release(13)
                print("Usado =")

            # Verificar y usar F6 si es necesario y está disponible
            if vida <= 15 and current_time - last_use_f6 >= cooldown_f6:
                last_use_f6 = use_skill("f6", 80)
                print(f"F6 usado. Próximo uso disponible en {cooldown_f6} segundos.")

            # Verificar y usar F5 si es necesario y está disponible
            elif vida <= 25 and current_time - last_use_f5 >= cooldown_f5:
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
        if image is None:
            print("[ERROR] No se pudo cargar la imagen del monstruo.")
            return False  # <-- Agrega este control

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
def funcioncaja():  
    global stop_flag, contadormostruos1, bosfinal, dungeon, puerta, terminar, bosdetectado,rangodetected
    global terminando, lanzabuff, puertita, vidamostruo, fail, atacar

    while not stop_flag and not keyboard.is_pressed('delete'):
        if dungeon != 1 or atacar == 0:
            time.sleep(0.5)
            continue
        print("funcioncaja en ejecución")

        imagen_a_buscar_bosfinal = "acheron/bosfinal.png"  # Reemplaza con la ruta de tu propia imagen
        bosfinal = buscar_imagen_en_pantalla(imagen_a_buscar_bosfinal)
        time.sleep(1)
        if bosfinal!=False:
            keyboard.press_and_release("alt+9")
            keyboard.press_and_release("F10")

        if buscar_imagen_en_pantalla("otros/cajaverde.png"):
            atacar = 0
            time.sleep(2)
            atacar = 1
        
        rango = buscar_imagen_en_pantalla("acheron/rango.png")
        if not rango:
            rango = buscar_imagen_en_pantalla("acheron/rango1.png")
        if rango:
            rangodetected = rango[1]+15

        caja_images = [
            # "otros/caja.png",
            # "otros/cofre.png",
            # "otros/cofre1.png",
            # "otros/cofre2.png",
            "otros/caja1.png",
            "acheron/rojo2.png",
            "acheron/rojo1.png",
            "acheron/master1.png",
            "acheron/bos1_name.png",
            "acheron/bos3_name.png",
        ]
        for caja_img in caja_images:
            caja = buscar_imagen_en_pantalla(caja_img)
            if caja:
                # Verificar si la posición Y está fuera del rango 165-170
                if caja[1] > rangodetected:
                    raton_posicion(caja[0], caja[1]+10)
                    pyautogui.click(button='left')
                    print(f'detecte {caja_img} en posición Y: {caja[1]} (fuera del rango 165-170)')
                    keyboard.press_and_release("space")
                    keyboard.press_and_release("space")
                else:
                    print(f'detecte {caja_img} en posición Y: {caja[1]} (dentro del rango 165-170, no se hace clic)')
    print("funcionmostruo terminada")
        
    

    
def funcionmostruo():
    global stop_flag, contadormostruos1, bosfinal, dungeon, puerta, terminar, bosdetectado
    global terminando, lanzabuff, puertita, vidamostruo, fail, atacar,etapa
    global mensaje

    bos_detected = False
    bos2_detected = False
    caja_detected = False

    while not stop_flag and not keyboard.is_pressed('delete'):
        if atacar == 0:
            bos_detected = False
            caja_detected = False
            bos2_detected = False
            mensaje = ""

        if dungeon != 1 or atacar == 0:
            time.sleep(0.5)
            continue

        if etapa==27 and (bos_detected or caja_detected):
            etapa=28
            
        if buscar_imagen_en_pantalla("acheron/bos1.png") or buscar_imagen_en_pantalla("acheron/bos1_name.png"):
            print("Bos1 detected, handling separately")
            # Add any specific logic for "bos2" here if needed
            etapa=23

        # Check specifically for "acheron/bos2.png"
        if buscar_imagen_en_pantalla("acheron/bos2.png") or buscar_imagen_en_pantalla("acheron/bos2_1.png"):
            print("Bos2 detected, handling separately")
            # Add any specific logic for "bos2" here if needed
            bos2_detected = True
            bos_detected = False
            caja_detected = False

        # Check for other specific images
        bos_images = ["acheron/bos1.png",  "acheron/bos3.png",  "acheron/bosfinal.png"]
        for image in bos_images:
            if buscar_imagen_en_pantalla(image):
                bos_detected = True
                caja_detected = False
                bos2_detected = False
                break
        print("funcionmostruo en ejecución")
        # If any of the specific images are detected, stop pressing "z"
        if bos_detected and not (bos2_detected or caja_detected)  :
            mensaje = "Bos detected, stopping 'z' press"
            print("Bos detected, stopping 'z' press")
            time.sleep(0.5)
            if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                time.sleep(2)
                while not caja_detected:
                    atacar=0
                    keyboard.press_and_release("z")
                    if buscar_imagen_en_pantalla("acheron/caja.png"):
                        contadormostruos1 = 0
                        atacar=1
                        caja_detected = True
                        bos_detected = False
                        bos2_detected = False
                    else:
                        contadormostruos1 += 1
        if caja_detected and not (bos_detected or bos2_detected):
            mensaje = "Caja detected, stopping 'z' press"
            time.sleep(0.5)
            if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                contadormostruos1 += 1
                
                if contadormostruos1 >= 2 and not buscar_imagen_en_pantalla("acheron/caja.png"):
                    caja_detected = False

                while not caja_detected:
                    
                    keyboard.press_and_release("z")
                    if buscar_imagen_en_pantalla("acheron/caja.png"):
                        contadormostruos1 = 0
                        atacar=1
                        caja_detected = True
                        bos_detected = False
                        bos2_detected = False
                    else:
                        contadormostruos1 += 1
                        if contadormostruos1 >= 4:
                            # atacar=0
                            contadormostruos1 = 4
                            break
                    
            # else:
            #     while not caja_detected:
            #         if  buscar_imagen_en_pantalla("otros/mostrous.jpg"):
            #             keyboard.press_and_release("z")
            #             if buscar_imagen_en_pantalla("acheron/caja.png"):
            #                 atacar=1
            #-                 caja_detected = True
            #         else:
            #             contadormostruos1 += 1
        if bos2_detected and not (bos_detected or caja_detected) :
            mensaje = "Bos2 detected, stopping 'z' press"
            time.sleep(0.5)
            if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                contadormostruos1 += 1
        else:
            if not (bos_detected or caja_detected or bos2_detected):
                mensaje = "normal"
                vidamostruo = imagenmostruo()

                if vidamostruo:
                    print('variable atacar')
                    contadormostruos1 = 0
                    if vidamostruo <= 9:
                        keyboard.press_and_release("z")
                else:
                    keyboard.press_and_release("z")
                    contadormostruos1 += 1

        # Reset detection if atacar changes to zero
        

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
    global stop_flag, bm3WI1, bm2WI1, vidamostruo, dungeon, tiempo_transcurrido, tiempo_inicio,atacar,contadormostruos1,bosfinal1,etapa

    imagen_presente = False

    while not stop_flag and not keyboard.is_pressed('delete'):
        if dungeon == 0 or dungeon == 2 or atacar == 0  : #or final == 1
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


        if bm3WI and buscar_imagen_en_pantalla("otros/mostrous.jpg")  and not (bm3WI1 or bm2WI1):
            keyboard.press_and_release("f12")
            time.sleep(0.5)
            keyboard.press_and_release("f12")

        
        if etapa >27 and bm2WI and buscar_imagen_en_pantalla("otros/mostrous.jpg")  and not (bm3WI1 or bm2WI1):
            keyboard.press_and_release("F10")
            time.sleep(0.5)
            keyboard.press_and_release("F10")

        # if bm2WI and vidamostruo  and not (bm3WI1 or bm2WI1):
        #     keyboard.press_and_release("f10")
        #     time.sleep(0.5)
        #     keyboard.press_and_release("f10")

    print("funcionBM terminada")

def funcionBM_optimizada():
    global stop_flag, bm3WI1, tiempo_transcurrido, vidamostruo, puerta, bosdetectado, atacar, dungeon, nombre_proceso, puertita, lanzabuff, tiempo_inicio

    # Cache para reducir búsquedas de imágenes repetitivas
    cache_imagenes = {}
    ultimo_check = {}
    intervalo_check = {
        "otros/salix.png": 1.0,
        "login/cabal.png": 2.0,
        "otros/bufsp.png": 5.0,
        "otros/bm2WI.png": 0.5,
        "otros/bm2WI1.png": 0.3,
        "otros/bm3WI.png": 0.5,
        "otros/bm3WI1.png": 0.3,
        "otros/mago.png": 1.0,
        "eca/boss.png": 1.0,
        "otros/mostrous.jpg": 0.5
    }

    # Inicializar el caché
    for img in intervalo_check:
        ultimo_check[img] = 0
        cache_imagenes[img] = False

    def check_imagen(ruta, forzar=False):
        tiempo_actual = time.time()
        if forzar or (tiempo_actual - ultimo_check.get(ruta, 0) >= intervalo_check.get(ruta, 0.5)):
            resultado = buscar_imagen_en_pantalla(ruta)
            cache_imagenes[ruta] = resultado
            ultimo_check[ruta] = tiempo_actual
            return resultado
        return cache_imagenes.get(ruta, False)

    # Secuencia de teclas para ataques normales
    secuencia_ataques = ["2", "3", "4", "8"]
    indice_ataque = 0
    
    # Tiempo del último ataque normal
    ultimo_ataque_normal = 0
    intervalo_ataque_normal = 2  # Intervalo entre ataques normales

    while not stop_flag and not keyboard.is_pressed('delete'):
        tiempo_actual = time.time()
        
        # Verificaciones menos frecuentes
        if tiempo_actual - ultimo_check.get("otros/salix.png", 0) >= intervalo_check["otros/salix.png"]:
            salix = check_imagen("otros/salix.png", True)
            
            if not (dungeon == 1 and atacar == 1 and salix ):
                time.sleep(0.3)
                continue

            tiempo_transcurrido = tiempo_actual - tiempo_inicio

            if check_imagen("login/cabal.png", True):
                time.sleep(0.3)
                continue
        if not (dungeon == 1 and atacar == 1  ):
                time.sleep(0.3)
                continue

        # Verificar buff cada 5 segundos
        if tiempo_actual - ultimo_check.get("otros/bufsp.png", 0) >= intervalo_check["otros/bufsp.png"]:
            bufsp = check_imagen("otros/bufsp.png", True)
            if bufsp and lanzabuff == 1:
                keyboard.press_and_release("f8")
                time.sleep(1)

        # Verificar estado de combate
        bm2WI = check_imagen("otros/bm2WI.png")
        bm2WI1 = check_imagen("otros/bm2WI1.png")
        bm3WI = check_imagen("otros/bm3WI.png")
        bm3WI1 = check_imagen("otros/bm3WI1.png", True)  # Siempre verificar bm3WI1
        
        # Priorizar ataques según el estado
        if bm2WI1:
            mago = check_imagen("otros/mago.png")
            if not mago:
                for _ in range(3):  # Reducido de 6 a 3 para mayor velocidad
                    keyboard.press_and_release("6")
                    keyboard.press_and_release("space")
                    time.sleep(0.15)  # Reducido de 0.2 a 0.15
                    
                    if not check_imagen("otros/bm2WI1.png", True) or  atacar == 0:
                        break
            else:
                max_intentos = 45  # Limitar el número de intentos para evitar bucles infinitos
                intentos = 0
                
                while intentos < max_intentos:
                    intentos += 1
                    # Optimización para ataques normales: usar un ataque a la vez en rotación
                    # if tiempo_actual - ultimo_ataque_normal >= intervalo_ataque_normal:
                    print(f'Ataque normal con monstruos: {secuencia_ataques[indice_ataque]}')
                    keyboard.press_and_release(secuencia_ataques[indice_ataque])
                    keyboard.press_and_release("space")
                    
                    # Rotar al siguiente ataque
                    indice_ataque = (indice_ataque + 1) % len(secuencia_ataques)
                    ultimo_ataque_normal = tiempo_actual
                    
                    # Verificar si debemos detener los ataques
                    if check_imagen("otros/bm3WI1.png", True) or not check_imagen("otros/mostrous.jpg", True) or atacar == 0:
                        keyboard.press_and_release("space")
                        time.sleep(0.15)  # Reducido de 0.2 a 0.15
                        break
        elif bm3WI1:
            # Optimización para el manejo de habilidades
            habilidades = [
                {"tecla": "6", "cooldown": 0.5, "casting": 0.7, "ultimo_uso": 0},  # Reducido casting time
                {"tecla": "6", "cooldown": 0.5, "casting": 0.7, "ultimo_uso": 0},  # Reducido casting time
                {"tecla": "5", "cooldown": 0.5, "casting": 0.7, "ultimo_uso": 0},
                {"tecla": "6", "cooldown": 0.5, "casting": 0.7, "ultimo_uso": 0},
                {"tecla": "7", "cooldown": 0, "casting": 1.5, "ultimo_uso": 0},    # Reducido casting time
                {"tecla": "7", "cooldown": 0, "casting": 1.5, "ultimo_uso": 0},    # Reducido casting time
                {"tecla": "7", "cooldown": 0, "casting": 1.5, "ultimo_uso": 0},    # Reducido casting time
            ]

            max_intentos = 45  # Limitar el número de intentos para evitar bucles infinitos
            intentos = 0
            
            while intentos < max_intentos:
                intentos += 1
                
                if not bosdetectado:
                    keyboard.press_and_release("6")
                    keyboard.press_and_release("space")
                    time.sleep(0.15)  # Reducido de 0.2 a 0.15
                    
                    if not check_imagen("otros/bm3WI1.png", True) or atacar == 0:
                        break
                else:  
                    ahora = time.time()
                    for hab in habilidades:
                        if ahora - hab["ultimo_uso"] >= hab["cooldown"]:
                            keyboard.press_and_release(hab["tecla"])
                            print(f"Presionando {hab['tecla']} - Casting {hab['casting']}s")
                            hab["ultimo_uso"] = ahora
                            time.sleep(hab["casting"])
                            keyboard.press_and_release("space")
                            
                            if not check_imagen("otros/bm3WI1.png", True) or atacar == 0:
                                break
                
                if not check_imagen("otros/bm3WI1.png", True) or atacar == 0:
                    break
        else:
            max_intentos = 45  # Limitar el número de intentos para evitar bucles infinitos
            intentos = 0
            
            while intentos < max_intentos:
                intentos += 1
                # Optimización para ataques normales: usar un ataque a la vez en rotación
                # if tiempo_actual - ultimo_ataque_normal >= intervalo_ataque_normal:
                print(f'Ataque normal con monstruos: {secuencia_ataques[indice_ataque]}')
                keyboard.press_and_release(secuencia_ataques[indice_ataque])
                keyboard.press_and_release("space")
                
                # Rotar al siguiente ataque
                indice_ataque = (indice_ataque + 1) % len(secuencia_ataques)
                ultimo_ataque_normal = tiempo_actual
                
                # Verificar si debemos detener los ataques
                if check_imagen("otros/bm3WI1.png", True) or not check_imagen("otros/mostrous.jpg", True) or atacar == 0:
                    keyboard.press_and_release("space")
                    time.sleep(0.15)  # Reducido de 0.2 a 0.15
                    break

    print("funcionBM optimizada terminada")

def funcionBM2():
    global stop_flag, bm3WI1, dungeon, nombre_proceso, vidamostruo, puerta, atacar, puertita, bosdetectado

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM2 en ejecución")
        time.sleep(0.3)  # Reduced sleep time

        if not (vidamostruo and dungeon == 1 and atacar == 1):
            continue

        if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
            continue

        if buscar_imagen_en_pantalla("login/cabal.png"):
            continue

        bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
        mago = buscar_imagen_en_pantalla("otros/mago.png")


        if bm2WI1 and not mago :
            while vidamostruo:
                keyboard.press_and_release("6")
                keyboard.press_and_release("space")
                time.sleep(0.2)
                keyboard.press_and_release("space")
                time.sleep(0.2)
                keyboard.press_and_release("space")
                time.sleep(0.2)
                vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
                if not buscar_imagen_en_pantalla("otros/bm2WI1.png"):
                    break

        print('ataque normal con monstruos')
        if (bm2WI1 and mago) :
            while vidamostruo:
                for tecla in ["2", "3", "4", "8"]:
                    keyboard.press_and_release(tecla)
                    keyboard.press_and_release("space")
                    time.sleep(0.2)
                    keyboard.press_and_release("space")
                    time.sleep(0.2)
                    keyboard.press_and_release("space")
                    time.sleep(0.2)
                    vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
                    if not vidamostruo or buscar_imagen_en_pantalla("otros/bm3WI1.png") or not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                        break
                if not vidamostruo or buscar_imagen_en_pantalla("otros/bm3WI1.png") or not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                    break

    print("funcionBM2 terminada")


def funcionBM3():
    global stop_flag, bm3WI1, dungeon, vidamostruo, atacar

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM3 en ejecución")

        if dungeon != 1 or atacar != 1 or not vidamostruo:
            time.sleep(0.5)
            continue

        bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
        if not bm3WI1:
            time.sleep(0.3)
            continue


        print('Iniciando ataque BM3 con monstruos')
        ataque_count = 0
        last_check_time = time.time()

        while vidamostruo and dungeon == 1 and atacar == 1:
            keyboard.press_and_release("6")
            keyboard.press_and_release("space")
            keyboard.press_and_release("space")
            keyboard.press_and_release("space")

            ataque_count += 1

            if ataque_count % 5 == 0:  # Comprueba cada 5 ataques
                current_time = time.time()
                if current_time - last_check_time >= 1:  # Comprueba cada segundo
                    if buscar_imagen_en_pantalla("login/cabal.png") or not buscar_imagen_en_pantalla("otros/bm3WI1.png") or not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                        break
                    last_check_time = current_time

            time.sleep(0.1)  # Pequeña pausa entre ataques

        print("Terminando ataque BM3 con monstruos")

        time.sleep(0.3)

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
        ok = buscar_imagen_en_pantalla("otros/ok.png")
        if fail and ok:
            print('fail')
            click_raton_posicion(fail[0], fail[1])
            reset_variables()
            time.sleep(0.5)
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

def imagenacheron():
    ruta_imagen = 'acheron/acheron.png'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre acheron')
        return False
    else:
        print('encontre acheron')
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
            keyboard.press_and_release("F12")
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
    confirmatronco = buscar_imagen_en_pantalla("acheron/confirmatronco.png")
    if confirmatronco:
        click_imagen(confirmatronco, offset_x=-680, offset_y=165)
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

        acheron = imagenacheron()
        detected = buscar_imagen_en_pantalla("acheron/detected.png")
        if not detected and acheron:
            click_imagen(acheron)
            time.sleep(1)
            raton_posicion(acheron[0], acheron[1]+30)

        if acheron and detected:
            print('clic acheron')
            noentrar = imagennoentrar()
            entrar = imagenentrar()
            time.sleep(2)
            if noentrar:
                print('clic no entrar1')
                stop_flag = True
                os.system("shutdown /s /t 10")
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
                os.system("shutdown /s /t 10")
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
bosfinal1 = 0
def funcionterminar():
    global stop_flag, terminar,muro2,muriendo, dungeon, bosdetectado, vidamostruo, puerta, terminando, lanzabuff, nombre_proceso, tiempo_inicio, contardgok, atacar,etapa,contadormostruos1,bosfinal1

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionterminar en ejecución")
        time.sleep(0.5)
        terminar = imagenterminar()

        if terminar:
            print('Terminando')
            terminando = 1
            etapa=0  
            contadormostruos1=0
            bosfinal1=0
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
                        etapa=0  
                        bosfinal1=0  
                        contadormostruos1=0
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
        global fire2_detectado
        global encontrada_imagen
        global contadormostruos1
        global vidamostruo
        global etapa
        global bscar
        global entre
        global nombre_proceso
        global piso
        global vida_actual
        global vida_anterior
        global tiempo_inicio
        print("funcionetapa en ejecución")
        time.sleep(1)
        centro_ventana = obtener_centro_ventana(nombre_proceso)
        if etapa>0 and dungeon==1 :
            if etapa==1:
                atacar=1
                piso1 = buscar_imagen_en_pantalla("acheron/piso1.png")
                if not piso1:
                    print('Piso 1 no encontrado')
                    piso = "piso1"
                    atacar = 0
                    etapa=2
                else:
                    raton_posicion(piso1[0], piso1[1])
                    last_known_position1 = piso1
                    
            if etapa==2 and  not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                raton_posicion(last_known_position1[0]-650, last_known_position1[1])
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                raton_posicion(last_known_position1[0], last_known_position1[1])
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                etapa=3
            if etapa==3:
                piso2 = buscar_imagen_en_pantalla("acheron/piso2.png")
                piso = "piso2"
                if piso2:
                    raton_posicion(piso2[0], piso2[1]+5)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    etapa=4
            if etapa==4:
                piso3 = buscar_imagen_en_pantalla("acheron/piso3.png")
                if not piso3:
                    piso3 = buscar_imagen_en_pantalla("acheron/piso3_1.png")
                if piso3:
                    raton_posicion(piso3[0], piso3[1])
                    pyautogui.click(clicks=1, interval=0.1,button='left')
                    last_known_position3 = piso3
                    etapa=5
            if etapa==5:
                npc = buscar_imagen_en_pantalla("acheron/npc.png")
                time.sleep(0.3)
                if npc:
                    for _ in range(3):
                        keyboard.press_and_release("space")
                        time.sleep(0.3)
                else:
                    raton_posicion(last_known_position3[0], last_known_position3[1]+300)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    contadormostruos1=0
                    keys = ['e']
                    hold_time = 0.5  # Tiempo que se mantiene presionada cada tecla (en segundos)
                    delay_between_keys = 1  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                    for key in keys:
                        keyboard.press(key)
                        time.sleep(hold_time)
                        keyboard.release(key)
                        time.sleep(delay_between_keys)
                    atacar = 1
                    etapa=6
            if etapa==6 and contadormostruos1>3:
                raton_posicion(last_known_position1[0]-650, last_known_position1[1])
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release("z")
                if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                    etapa=7
            if etapa==7:
                atacar = 0
                raton_posicion(last_known_position1[0], last_known_position1[1])
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keys = ['e','e']
                hold_time = 1  # Tiempo que se mantiene presionada cada tecla (en segundos)
                delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                for key in keys:
                    keyboard.press(key)
                    time.sleep(hold_time)
                    keyboard.release(key)
                    time.sleep(delay_between_keys)
                raton_posicion(last_known_position1[0]-650, last_known_position1[1])
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                etapa=8
            if etapa==8:
                piso4 = buscar_imagen_en_pantalla("acheron/piso4.png")
                piso = "piso4"
                if piso4:
                    raton_posicion(piso4[0], piso4[1]+5)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    etapa=9
            if etapa==9:
                piso5 = buscar_imagen_en_pantalla("acheron/piso5.png")
                if not piso5:
                    piso5 = buscar_imagen_en_pantalla("acheron/piso5_1.png")
                if piso5:
                    raton_posicion(piso5[0], piso5[1])
                    pyautogui.click(clicks=1, interval=0.1,button='left')
                    last_known_position5 = piso5
                    etapa=10
            if etapa==10:
                
                npc = buscar_imagen_en_pantalla("acheron/npc.png")
                time.sleep(0.3)
                if npc:
                    for _ in range(3):
                        keyboard.press_and_release("space")
                        time.sleep(0.3)
                else:
                    if entre==0:
                        raton_posicion(last_known_position5[0]+15, last_known_position5[1]+300)
                        keyboard.press_and_release(".")
                        time.sleep(0.9)
                        contadormostruos1=0
                        keys = ['e','e']
                        hold_time = 0.5  # Tiempo que se mantiene presionada cada tecla (en segundos)
                        delay_between_keys = 1  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                        for key in keys:
                            keyboard.press(key)
                            time.sleep(hold_time)
                            keyboard.release(key)
                            time.sleep(delay_between_keys)
                        atacar = 1
                        keyboard.press_and_release("z")
                        entre=1
                    # Solo ejecutar la búsqueda si no hay monstruos visibles
                    if not buscar_imagen_en_pantalla("otros/mostrous.jpg") and contadormostruos1>2 and entre==1:
                        # Variable para rastrear la dirección actual de búsqueda
                        # 0: hacia atrás, 1: hacia adelante, 2: regreso a posición original
                        direccion_busqueda = 0
                        pasos_completados = 0
                        
                        # Ciclo principal de búsqueda
                        while direccion_busqueda < 3 and not buscar_imagen_en_pantalla("otros/mostrous.jpg") and contadormostruos1>2:
                            print("Iniciando ciclo kong")
                            if direccion_busqueda == 0:  # Búsqueda hacia atrás
                                print("Iniciando ciclo kongv1")
                                if pasos_completados < 2:
                                    raton_posicion(centro_ventana[0]-330, centro_ventana[1]+100)
                                    keyboard.press_and_release(",")
                                    time.sleep(1)
                                    keyboard.press_and_release("z")
                                    time.sleep(0.5)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado hacia atrás, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong1")  
                                            # Verificar si la vida del monstruo está bajando
                                            # if 'moustruovida' in globals():
                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad
                                        direccion_busqueda = 1
                                        pasos_completados = 0
                                            
                                else:
                                    # Completó los 2 pasos hacia atrás, cambiar dirección
                                    direccion_busqueda = 1
                                    pasos_completados = 0
                            
                            elif direccion_busqueda == 1:  # Búsqueda hacia adelante
                                print("Iniciando ciclo kongv2")
                                if pasos_completados < 2:
                                    raton_posicion(centro_ventana[0]+330, centro_ventana[1]-100)
                                    keyboard.press_and_release(",")
                                    time.sleep(1)
                                    keyboard.press_and_release("z")
                                    time.sleep(0.5)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado hacia adelante, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong2")
                                            # Verificar si la vida del monstruo está bajando
                                            # if 'moustruovida' in globals():
                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad
                                        direccion_busqueda = 2
                                        pasos_completados = 0
                                else:
                                    # Completó los 4 pasos hacia adelante, cambiar dirección
                                    direccion_busqueda = 2
                                    pasos_completados = 0
                            
                            elif direccion_busqueda == 2:  # Regreso a posición original
                                print("Iniciando ciclo kongv3")
                                if pasos_completados < 1:
                                    raton_posicion(centro_ventana[0]-330, centro_ventana[1]+100)
                                    keyboard.press_and_release(",")
                                    time.sleep(1)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado al regresar, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong3")

                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            etapa=11
                                                            entre=0
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad

                                        contadormostruos1 = 4
                                        etapa=11
                                        entre=0
                                        direccion_busqueda = 3
                                            # Si el combate dura demasiado, continuar
                                            # if time.time() - tiempo_inicio_combate > 15:
                                            #     print("Combate demasiado largo, continuando camino")
                                            #     atacar = 0
                                            #     break
                                                
                                            # time.sleep(1)  # Esperar mientras hay monstruos
                                    else:
                                        # Completó los 2 pasos de regreso, terminar ciclo.
                                        contadormostruos1 = 4
                                        etapa=11
                                        entre=0
                                        direccion_busqueda = 3
                    
            if etapa==11 and contadormostruos1>3:
                atacar = 0
                bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
                bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")

                for bm in [bm3WI1, bm2WI1]:
                    if bm:
                        raton_posicion(bm[0], bm[1]+5)
                        pyautogui.mouseDown(button='right')
                        time.sleep(1)  # Mantener el botón presionado por 0.2 segundos
                        pyautogui.mouseUp(button='right')
                        time.sleep(0.7)
                        pyautogui.click(button='right') 
                if not buscar_imagen_en_pantalla("otros/bm2WI1.png") and not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                    raton_posicion(centro_ventana[0]+330, centro_ventana[1]-120)
                    time.sleep(1)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keys = ['e','e']
                    hold_time = 1  # Tiempo que se mantiene presionada cada tecla (en segundos)
                    delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                    for key in keys:
                        keyboard.press(key)
                        time.sleep(hold_time)
                        keyboard.release(key)
                        time.sleep(delay_between_keys)
                    raton_posicion(centro_ventana[0]-200, centro_ventana[1]+150)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(1)
                    keyboard.press_and_release(".")
                    time.sleep(1.5)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    etapa=12
          
            if etapa==12:
                piso6 = buscar_imagen_en_pantalla("acheron/piso6.png")
                if not  piso6:
                    keys = ['s','s','s','s','q','w','w','q','s','s','s','s','q','w','w','q','s','s','s','s']
                    hold_time = 0.5  # Tiempo que se mantiene presionada cada tecla (en segundos)
                    delay_between_keys = 1  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                    for key in keys:
                        keyboard.press(key)
                        time.sleep(hold_time)
                        keyboard.release(key)
                        time.sleep(delay_between_keys)
                        piso6 = buscar_imagen_en_pantalla("acheron/piso6.png")
                        if piso6:
                            break
           
                if piso6:
                    raton_posicion(piso6[0], piso6[1])
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    etapa=13
            if etapa==13:
                piso7 = buscar_imagen_en_pantalla("acheron/piso7.png")
                if not piso7:
                    piso7 = buscar_imagen_en_pantalla("acheron/piso7_1.png")
                if piso7:
                    raton_posicion(piso7[0], piso7[1])
                    pyautogui.click(clicks=1, interval=0.1,button='left')
                    last_known_position7 = piso7
                    etapa=14
            if etapa==14:
                npc = buscar_imagen_en_pantalla("acheron/npc.png")
                time.sleep(0.3)
                if npc:
                    for _ in range(3):
                        keyboard.press_and_release("space")
                        time.sleep(0.3)
                else:
                    if entre==0:
                        # raton_posicion(centro_ventana[0]+200, centro_ventana[1]+55)
                        raton_posicion(centro_ventana[0]+180, centro_ventana[1]+125)
                        keyboard.press_and_release(".")
                        time.sleep(0.9)
                        contadormostruos1=0
                        keys = ['e','e']
                        hold_time = 0.5  # Tiempo que se mantiene presionada cada tecla (en segundos)
                        delay_between_keys = 1  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                        for key in keys:
                            keyboard.press(key)
                            time.sleep(hold_time)
                            keyboard.release(key)
                            time.sleep(delay_between_keys)
                        atacar = 1
                        keyboard.press_and_release("z")
                        entre=1
                    # Solo ejecutar la búsqueda si no hay monstruos visibles
                    if not buscar_imagen_en_pantalla("otros/mostrous.jpg") and contadormostruos1>2 and entre==1:
                        # Variable para rastrear la dirección actual de búsqueda
                        # 0: hacia atrás, 1: hacia adelante, 2: regreso a posición original
                        direccion_busqueda = 0
                        pasos_completados = 0
                        
                        # Ciclo principal de búsqueda
                        while direccion_busqueda < 5 and not buscar_imagen_en_pantalla("otros/mostrous.jpg") and contadormostruos1>2:
                            print("Iniciando ciclo kong")
                            if direccion_busqueda == 0:  # Búsqueda hacia atrás
                                print("Iniciando ciclo kongv1")
                                if pasos_completados < 3:
                                    raton_posicion(centro_ventana[0]-100, centro_ventana[1]+150)
                                    keyboard.press_and_release(",")
                                    time.sleep(1)
                                    keyboard.press_and_release("z")
                                    time.sleep(0.5)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado hacia atrás, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong1")  
                                            # Verificar si la vida del monstruo está bajando
                                            # if 'moustruovida' in globals():
                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad
                                        direccion_busqueda = 1
                                        pasos_completados = 0
                                            
                                else:
                                    # Completó los 2 pasos hacia atrás, cambiar dirección
                                    direccion_busqueda = 1
                                    pasos_completados = 0
                            elif direccion_busqueda == 1:  # Búsqueda hacia adelante
                                print("Iniciando ciclo kongv2")
                                if pasos_completados < 1:
                                    raton_posicion(centro_ventana[0]-350, centro_ventana[1]+60)
                                    keyboard.press_and_release(".")
                                    time.sleep(1)
                                    keyboard.press_and_release("z")
                                    time.sleep(0.5)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado hacia adelante, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong2")
                                            # Verificar si la vida del monstruo está bajando
                                            # if 'moustruovida' in globals():
                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad
                                        direccion_busqueda = 2
                                        pasos_completados = 0
                                else:
                                    # Completó los 4 pasos hacia adelante, cambiar dirección
                                    direccion_busqueda = 2
                                    pasos_completados = 0

                            elif direccion_busqueda == 2:  # Búsqueda hacia adelante
                                print("Iniciando ciclo kongv2")
                                if pasos_completados < 1:
                                    raton_posicion(centro_ventana[0]+380, centro_ventana[1]+120)
                                    keyboard.press_and_release(".")
                                    time.sleep(1)
                                    keyboard.press_and_release("z")
                                    time.sleep(0.5)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado hacia adelante, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong2")
                                            # Verificar si la vida del monstruo está bajando
                                            # if 'moustruovida' in globals():
                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad
                                        direccion_busqueda = 3
                                        pasos_completados = 0
                                else:
                                    # Completó los 4 pasos hacia adelante, cambiar dirección
                                    direccion_busqueda = 3
                                    pasos_completados = 0
                            
                            elif direccion_busqueda == 3:  # Búsqueda hacia adelante
                                print("Iniciando ciclo kongv2")
                                if pasos_completados < 4:
                                    raton_posicion(centro_ventana[0]+300, centro_ventana[1]-250)
                                    keyboard.press_and_release(",")
                                    time.sleep(1)
                                    keyboard.press_and_release("z")
                                    time.sleep(0.5)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado hacia adelante, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong2")
                                            # Verificar si la vida del monstruo está bajando
                                            # if 'moustruovida' in globals():
                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad
                                        direccion_busqueda = 4
                                        pasos_completados = 0
                                else:
                                    # Completó los 4 pasos hacia adelante, cambiar dirección
                                    direccion_busqueda = 4
                                    pasos_completados = 0
                            
                            elif direccion_busqueda == 4:  # Regreso a posición original
                                print("Iniciando ciclo kongv3")
                                if pasos_completados < 2:
                                    raton_posicion(centro_ventana[0]-300, centro_ventana[1]+150)
                                    keyboard.press_and_release(",")
                                    time.sleep(1)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado al regresar, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong3")

                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            etapa=15
                                                            entre=0
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad

                                        contadormostruos1 = 4
                                        etapa=15
                                        entre=0
                                        direccion_busqueda = 5
                                            # Si el combate dura demasiado, continuar
                                            # if time.time() - tiempo_inicio_combate > 15:
                                            #     print("Combate demasiado largo, continuando camino")
                                            #     atacar = 0
                                            #     break
                                                
                                            # time.sleep(1)  # Esperar mientras hay monstruos
                                    else:
                                        # Completó los 2 pasos de regreso, terminar ciclo.
                                        contadormostruos1 = 4
                                        etapa=15
                                        entre=0
                                        direccion_busqueda = 5


            if etapa==15 and contadormostruos1>3:
                atacar = 0
                
                raton_posicion(centro_ventana[0]+100, centro_ventana[1]-150)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keys = ['e','e','e']
                hold_time = 1  # Tiempo que se mantiene presionada cada tecla (en segundos)
                delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                for key in keys:
                    keyboard.press(key)
                    time.sleep(hold_time)
                    keyboard.release(key)
                    time.sleep(delay_between_keys)
                raton_posicion(centro_ventana[0]-200, centro_ventana[1]+150)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                etapa=16
            if etapa==16:
                piso8 = buscar_imagen_en_pantalla("acheron/piso8_4.png")
                
                if not  piso8:
                    raton_posicion(centro_ventana[0]+100, centro_ventana[1]-150)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keys = ['e','e']
                    hold_time = 2  # Tiempo que se mantiene presionada cada tecla (en segundos)
                    delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                    for key in keys:
                        keyboard.press(key)
                        time.sleep(hold_time)
                        keyboard.release(key)
                        time.sleep(delay_between_keys)
                    keys = ['s']
                    hold_time = 0.5  # Tiempo que se mantiene presionada cada tecla (en segundos)
                    delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                    for key in keys:
                        keyboard.press(key)
                        time.sleep(hold_time)
                        keyboard.release(key)
                        time.sleep(delay_between_keys)
                    raton_posicion(centro_ventana[0]-300, centro_ventana[1]+20)
                    keyboard.press_and_release(".")
                    time.sleep(1.2)
                    raton_posicion(centro_ventana[0]-40, centro_ventana[1]-300)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    raton_posicion(centro_ventana[0]-40, centro_ventana[1]+300)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    piso8 = buscar_imagen_en_pantalla("acheron/piso8_4.png")
                    if not piso8:
                        piso8 = buscar_imagen_en_pantalla("acheron/piso8_5.png")
                if piso8:
                    raton_posicion(piso8[0], piso8[1]+50)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    etapa=17
            if etapa==17:
                piso9 = buscar_imagen_en_pantalla("acheron/piso9.png")
                if piso9:
                    raton_posicion(piso9[0], piso9[1])
                    pyautogui.click(clicks=1, interval=0.1,button='left')
                    last_known_position9 = piso9
                    etapa=18
            if etapa==18:
                npc = buscar_imagen_en_pantalla("acheron/npc.png")
                time.sleep(0.3)
                if npc:
                    for _ in range(3):
                        keyboard.press_and_release("space")
                        time.sleep(0.3)
                else:
                    if entre==0:
                        raton_posicion(centro_ventana[0]+300, centro_ventana[1]-15)
                        keyboard.press_and_release(".")
                        time.sleep(0.9)
                        contadormostruos1=0
                        keys = ['w']
                        hold_time = 0.5  # Tiempo que se mantiene presionada cada tecla (en segundos)
                        delay_between_keys = 1  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                        for key in keys:
                            keyboard.press(key)
                            time.sleep(hold_time)
                            keyboard.release(key)
                            time.sleep(delay_between_keys)
                        atacar = 1
                        keyboard.press_and_release("z")
                        entre=1
                    # Solo ejecutar la búsqueda si no hay monstruos visibles
                    if not buscar_imagen_en_pantalla("otros/mostrous.jpg") and contadormostruos1>2 and entre==1:
                        # Variable para rastrear la dirección actual de búsqueda
                        # 0: hacia atrás, 1: hacia adelante, 2: regreso a posición original
                        direccion_busqueda = 0
                        pasos_completados = 0
                        
                        # Ciclo principal de búsqueda
                        while direccion_busqueda < 3 and not buscar_imagen_en_pantalla("otros/mostrous.jpg") and contadormostruos1>2:
                            print("Iniciando ciclo kong")
                            if direccion_busqueda == 0:  # Búsqueda hacia atrás
                                print("Iniciando ciclo kongv1")
                                if pasos_completados < 3:
                                    raton_posicion(centro_ventana[0]+5, centro_ventana[1]+250)
                                    keyboard.press_and_release(",")
                                    time.sleep(1)
                                    keyboard.press_and_release("z")
                                    time.sleep(0.5)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado hacia atrás, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong1")  
                                            # Verificar si la vida del monstruo está bajando
                                            # if 'moustruovida' in globals():
                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad
                                        direccion_busqueda = 1
                                        pasos_completados = 0
                                            
                                else:
                                    # Completó los 2 pasos hacia atrás, cambiar dirección
                                    direccion_busqueda = 1
                                    pasos_completados = 0
                            
                            elif direccion_busqueda == 1:  # Búsqueda hacia adelante
                                print("Iniciando ciclo kongv2")
                                if pasos_completados < 4:
                                    raton_posicion(centro_ventana[0]-5, centro_ventana[1]-250)
                                    keyboard.press_and_release(",")
                                    time.sleep(1)
                                    keyboard.press_and_release("z")
                                    time.sleep(0.5)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado hacia adelante, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong2")
                                            # Verificar si la vida del monstruo está bajando
                                            # if 'moustruovida' in globals():
                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad
                                        direccion_busqueda = 2
                                        pasos_completados = 0
                                else:
                                    # Completó los 4 pasos hacia adelante, cambiar dirección
                                    direccion_busqueda = 2
                                    pasos_completados = 0
                            
                            elif direccion_busqueda == 2:  # Regreso a posición original
                                print("Iniciando ciclo kongv3")
                                if pasos_completados < 1:
                                    raton_posicion(centro_ventana[0]+5, centro_ventana[1]+250)
                                    keyboard.press_and_release(",")
                                    time.sleep(1)
                                    pasos_completados += 1
                                    
                                    # Si encuentra monstruos, esperar a que los mate
                                    if buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                        print("Monstruo encontrado al regresar, esperando a que sea eliminado")
                                        tiempo_inicio_combate = time.time()
                                        vida_anterior = None
                                        ciclos_sin_bajar = 0
                                        
                                        while buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                                                print("Iniciando ciclo kong3")

                                                vida_actual = imagenmostruo()
                                                print(f"[DEBUG] vida_actual detectada: {vida_actual}")

                                                if vida_anterior is None:
                                                    vida_anterior = vida_actual
                                                    ciclos_sin_bajar = 0
                                                    print(f"[DEBUG] Inicializando vida_anterior: {vida_anterior}")
                                                    contadormostruos1  = 3
                                                else:
                                                    if vida_actual < vida_anterior - 1:
                                                        print(f"[DEBUG] La vida bajó de {vida_anterior} a {vida_actual}, reiniciando ciclos_sin_bajar.")
                                                        vida_anterior = vida_actual
                                                        ciclos_sin_bajar = 0
                                                        keyboard.press_and_release("esc")
                                                        keyboard.press_and_release("esc")
                                                        contadormostruos1  = 3
                                                    else:
                                                        ciclos_sin_bajar += 1
                                                        print(f"[DEBUG] La vida no bajó, ciclos_sin_bajar: {ciclos_sin_bajar}")
                                                        if ciclos_sin_bajar >= 8:
                                                            print("[DEBUG] La vida no bajó en 3 ciclos, saliendo del bucle.")
                                                            pasos_completados=5
                                                            keyboard.press_and_release("esc")
                                                            keyboard.press_and_release("esc")
                                                            atacar = 0
                                                            time.sleep(1)
                                                            keyboard.press_and_release("esc")
                                                            contadormostruos1  = 3
                                                            etapa=19
                                                            entre=0
                                                            break

                                                time.sleep(0.5)  # Ajusta el tiempo según tu necesidad

                                        contadormostruos1 = 4
                                        etapa=19
                                        entre=0
                                        direccion_busqueda = 3
                                    else:
                                        # Completó los 2 pasos de regreso, terminar ciclo.
                                        contadormostruos1 = 4
                                        etapa=19
                                        entre=0
                                        direccion_busqueda = 3


            if etapa==19 and contadormostruos1>3:
                atacar = 0
                raton_posicion(centro_ventana[0]-5, centro_ventana[1]-250)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keys = ['e','e','e']
                hold_time = 1  # Tiempo que se mantiene presionada cada tecla (en segundos)
                delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                for key in keys:
                    keyboard.press(key)
                    time.sleep(hold_time)
                    keyboard.release(key)
                    time.sleep(delay_between_keys)
                bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
                bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")

                for bm in [bm3WI1, bm2WI1]:
                    if bm:
                        raton_posicion(bm[0], bm[1]+5)
                        pyautogui.mouseDown(button='right')
                        time.sleep(1)  # Mantener el botón presionado por 0.2 segundos
                        pyautogui.mouseUp(button='right')
                        time.sleep(0.7)
                        pyautogui.click(button='right') 
                if not buscar_imagen_en_pantalla("otros/bm2WI1.png") and not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                    raton_posicion(centro_ventana[0]-50, centro_ventana[1]+200)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    etapa=20
     
            if etapa==20:
                piso10 = buscar_imagen_en_pantalla("acheron/piso10.png")
                if not piso10:
                    piso10 = buscar_imagen_en_pantalla("acheron/piso10_1.png")
                if not  piso10:
                    raton_posicion(centro_ventana[0]-5, centro_ventana[1]-250)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    keys = ['e','e']
                    hold_time = 0.8  # Tiempo que se mantiene presionada cada tecla (en segundos)
                    delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                    for key in keys:
                        keyboard.press(key)
                        time.sleep(hold_time)
                        keyboard.release(key)
                        time.sleep(delay_between_keys)
                    bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
                    bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")

                    for bm in [bm3WI1, bm2WI1]:
                        if bm:
                            raton_posicion(bm[0], bm[1]+5)
                            pyautogui.mouseDown(button='right')
                            time.sleep(1)  # Mantener el botón presionado por 0.2 segundos
                            pyautogui.mouseUp(button='right')
                            time.sleep(0.7)
                            pyautogui.click(button='right') 
                    if not buscar_imagen_en_pantalla("otros/bm2WI1.png") and not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                        raton_posicion(centro_ventana[0]-50, centro_ventana[1]+200)
                        keyboard.press_and_release(".")
                        time.sleep(0.9)
                        keyboard.press_and_release(",")
                        time.sleep(0.7)
                        keyboard.press_and_release(".")
                        time.sleep(0.9)
                        piso10 = buscar_imagen_en_pantalla("acheron/piso10.png")
                        if not piso10:
                            piso10 = buscar_imagen_en_pantalla("acheron/piso10_1.png")
                        time.sleep(1)
                if piso10:
                    raton_posicion(piso10[0], piso10[1])
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    keyboard.press_and_release(",")
                    time.sleep(0.7)
                    etapa=21
            if etapa==21:
                piso11 = buscar_imagen_en_pantalla("acheron/piso11.png")
                
                if piso11:
                    raton_posicion(piso11[0], piso11[1]+20)
                    pyautogui.click(clicks=1, interval=0.1,button='left')
                    last_known_position7 = piso11
                    etapa=22
            if etapa==22:
                npc = buscar_imagen_en_pantalla("acheron/npc.png")
                time.sleep(0.3)
                if npc:
                    for _ in range(3):
                        keyboard.press_and_release("space")
                        time.sleep(0.3)
                else:
                    raton_posicion (centro_ventana[0]+17, centro_ventana[1]-230)
                    keyboard.press_and_release(".")
                    time.sleep(0.9)
                    contadormostruos1=0
                    while True:
                        keyboard.press_and_release("z")
                        time.sleep(0.1)
                        rango1 = buscar_imagen_en_pantalla("acheron/Rango1.png")
                        rangobos = buscar_imagen_en_pantalla("acheron/rangobos.png")
                        
                        # Si encuentra alguna de las imágenes de rango, salir del bucle
                        if rango1 or rangobos:
                            atacar = 1
                            etapa = 23
                            print("Rango detectado, atacar=1 y etapa=23")
                            break
                        
                        
            if etapa==23 and contadormostruos1>3:
                atacar = 0
                keys = ['q']
                hold_time = 2  # Tiempo que se mantiene presionada cada tecla (en segundos)
                delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                for key in keys:
                    keyboard.press(key)
                    time.sleep(hold_time)
                    keyboard.release(key)
                    time.sleep(delay_between_keys)
                raton_posicion (centro_ventana[0]+200, centro_ventana[1]-50)    
                keyboard.press_and_release(",")
                time.sleep(0.7)
                etapa=24
            if etapa==24:
                raton_posicion (centro_ventana[0]-200, centro_ventana[1]-300)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                raton_posicion (centro_ventana[0]-350, centro_ventana[1]+20)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                contadormostruos1=0
                atacar = 1
                etapa=25
            if etapa==25 and contadormostruos1>3:
                atacar = 0
                keys = ['w','w']
                hold_time = 2  # Tiempo que se mantiene presionada cada tecla (en segundos)
                delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                for key in keys:
                    keyboard.press(key)
                    time.sleep(hold_time)
                    keyboard.release(key)
                    time.sleep(delay_between_keys)
                raton_posicion (centro_ventana[0], centro_ventana[1]+200)    
                keyboard.press_and_release(".")
                time.sleep(0.9)
                raton_posicion (centro_ventana[0]-350, centro_ventana[1]+110)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                raton_posicion (centro_ventana[0]-350, centro_ventana[1]+300)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                raton_posicion (centro_ventana[0]+200, centro_ventana[1]+150)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                raton_posicion (centro_ventana[0]-150, centro_ventana[1]+250)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                contadormostruos1=0
                atacar = 1
                etapa=26
            if etapa==26 and contadormostruos1>3:
                atacar = 0
                keys = ['q','q']
                hold_time = 2  # Tiempo que se mantiene presionada cada tecla (en segundos)
                delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                for key in keys:
                    keyboard.press(key)
                    time.sleep(hold_time)
                    keyboard.release(key)
                    time.sleep(delay_between_keys)
                raton_posicion (centro_ventana[0]+200, centro_ventana[1]+20)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                raton_posicion (centro_ventana[0]-50, centro_ventana[1]+300)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                raton_posicion (centro_ventana[0]+250, centro_ventana[1]+203)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                contadormostruos1=0
                atacar = 1
                etapa=27
            if etapa==27 and contadormostruos1>3:
                atacar = 0
                raton_posicion (centro_ventana[0]+320, centro_ventana[1]-10)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                contadormostruos1=0
                atacar = 1
                etapa=28
            if etapa==28 and contadormostruos1>3:
                atacar = 0
                bos_detected = False
                caja_detected = False
                bos2_detected = False
                raton_posicion (centro_ventana[0]+300, centro_ventana[1]-40)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keys = ['e','e','e']
                hold_time = 2  # Tiempo que se mantiene presionada cada tecla (en segundos)
                delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                for key in keys:
                    keyboard.press(key)
                    time.sleep(hold_time)
                    keyboard.release(key)
                    time.sleep(delay_between_keys)
                raton_posicion (centro_ventana[0]-350, centro_ventana[1]+80)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                raton_posicion (centro_ventana[0]-25, centro_ventana[1]-300)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                keyboard.press_and_release(",")
                time.sleep(0.7)
                keyboard.press_and_release(".")
                time.sleep(0.9)
                contadormostruos1=0
                atacar = 1
                etapa=29
            if etapa==29 and contadormostruos1>10:
                if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                    keys = ['s']
                    hold_time = 0.5  # Tiempo que se mantiene presionada cada tecla (en segundos)
                    delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                    for key in keys:
                        keyboard.press(key)
                        time.sleep(hold_time)
                        keyboard.release(key)
                        time.sleep(delay_between_keys)
                    keyboard.press_and_release("z")


            
    print("funcionetapa terminada")

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

        # M2 = buscar_imagen_en_pantalla("otros/M2.png")
        # if M2:
        #     print("M2 detectado")
        # else:
        #     M2_K = buscar_imagen_en_pantalla("otros/M2_K.png")
        #     if M2_K:
        #         print("M2_K detectado")
        #         keyboard.press('ctrl')
        #         time.sleep(0.5)
        #         keyboard.press('6')
        #         time.sleep(0.5)
        #         keyboard.release('6')
        #         keyboard.release('ctrl')
        #     else:
        #         print("Ni M2 ni M2_K fueron detectados")

    print("funcionmercenario terminada")





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
fire2_detectado=False
bscar=False
muro2=False
bm3WI1=False
bm2WI1=False
encontrada_imagen=False
lanzabuff=0
bosfinal=False
fail = False
entre=0
rangodetected=0
bosfinal1=0
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
    funcionBM_optimizada,
    # funcionBM2,
    # funcionBM3,
    funcionfail,
    funcionmuerte,
    funcioncaja,
    funcioiniciar,
    funcionterminar,
    funcionmercenario,
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
