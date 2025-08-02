import concurrent.futures
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
import threading
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os


import ctypes

import tkinter as tk
from tkinter import ttk
contardg=contadormostruos1= atacar= etapa=contardgok=wavecuenta=esperandocuenta=bosscuenta=0
piso=""

def crear_ventana_info():
    global contardg, atacar, etapa, contardgok, piso, contadormostruos1, wavecuenta, esperandocuenta, bosscuenta
    ventana = tk.Tk()
    ventana.title("Información en tiempo real")
    ventana.geometry("300x250")  # Aumentado el tamaño vertical para acomodar las nuevas etiquetas

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

    etiqueta_cuentawave = ttk.Label(ventana, text="Cuenta Wave: ")
    etiqueta_cuentawave.pack()

    etiqueta_esperandocuenta = ttk.Label(ventana, text="Esperando Cuenta: ")
    etiqueta_esperandocuenta.pack()

    etiqueta_cuentaboss = ttk.Label(ventana, text="Cuenta Boss: ")
    etiqueta_cuentaboss.pack()

    def actualizar_info():
        global contardg, atacar, etapa, contardgok, piso, contadormostruos1, wavecuenta, esperandocuenta, bosscuenta
        etiqueta_dg.config(text=f"DG : {contardg}")
        etiqueta_dgok.config(text=f"DG ok: {contardgok}")
        etiqueta_atacar.config(text=f"Atacar: {atacar}")
        etiqueta_mostruos.config(text=f"Mostruos: {contadormostruos1}")
        etiqueta_piso.config(text=f"Piso: {piso}")
        etiqueta_etapa.config(text=f"Etapa inicial: {etapa}")
        etiqueta_cuentawave.config(text=f"Cuenta Wave: {wavecuenta}")
        etiqueta_esperandocuenta.config(text=f"Esperando Cuenta: {esperandocuenta}")
        etiqueta_cuentaboss.config(text=f"Cuenta Boss: {bosscuenta}")
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

def forzar_deshabilitar_bloq_mayus():
    # Código de tecla de Caps Lock
    VK_CAPITAL = 0x14

    # Obtener el estado actual de Caps Lock
    caps_lock_state = ctypes.windll.user32.GetKeyState(VK_CAPITAL)
    
    # Si está activado, envía un evento para desactivarlo
    if caps_lock_state & 1:  # Estado activado
        ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, 0, 0)  # Pulsar
        ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, 2, 0)  # Soltar
        print("Bloq Mayús ha sido deshabilitado.")
    else:
        print("Bloq Mayús ya estaba deshabilitado.")


def obtener_centro_ventana(nombre_proceso):
    try:
        ventana = gw.getWindowsWithTitle(nombre_proceso)[0]
        centro_x = ventana.left + ventana.width / 2
        centro_y = ventana.top + ventana.height / 2
        return centro_x, centro_y
    except IndexError:
        return None

mouse = Controller()

def raton_posicion (x,y):
    mouse.position = (x, y)
    print('Now we have moved it to {0}'.format(
        mouse.position))
    # Press and release
    # mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)

def click_raton_posicion (x,y):
    mouse.position = (x, y)
    print('Now we have moved it to {0}'.format(
        mouse.position))
    # Press and release
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)
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



def capturar_pantalla(x, y, ancho, alto):
    screenshot = pyautogui.screenshot(region=(x, y, ancho, alto))
    screenshot.save('captura/captura_pantalla_SP.png')
    return 'captura/captura_pantalla_SP.png'

def imagenSP():
    search = Search("sp/7.jpg")
    pos = search.imagesearch()
    if pos[0] == -1:
        if path.exists('captura/captura_pantalla_SP.png'):
            remove("captura/captura_pantalla_SP.png")
        return False
    else:
        return pos

def funcionSP():
    
    global stop_flag
    while not stop_flag and not keyboard.is_pressed('delete'):
        global etapa
        global dungeon
        global contardg
        print("funcionSP en ejecución")
        time.sleep(1)
        imagen_a_buscar_bufsp = "otros/bufsp.png"  # Reemplaza con la ruta de tu propia imagen
        bufsp = buscar_imagen_en_pantalla(imagen_a_buscar_bufsp)
        if bufsp!=False :
            keyboard.press_and_release("F8")
            time.sleep(1)
        sp = imagenSP()
        if sp!= False:
            imagen_capturada = capturar_pantalla(sp[0], sp[1], 65, 10)

        if path.exists('captura/captura_pantalla_SP.png'):

            img = cv2.imread('captura/captura_pantalla_SP.png')
        else:
            img = cv2.imread('sp/1.jpg')
        grises = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bordes = cv2.Canny(grises, 100, 800)
            #Para OpenCV3
            #_, ctns, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            #Para OpenCV4
        ctns, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, ctns, -1, (0,0,255), 2)

        print('Número de sp: ', len(ctns))
        print('DG1: ',contardg)
        print('etapa inicial: ',etapa)
        print('dungeon inicial: ',dungeon)
        if len(ctns)==0:
            keyboard.press_and_release("-")

    print("funcionSP terminada")
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
def capturar_pantalla_mostruo(x, y, ancho, alto):
    screenshot = pyautogui.screenshot(region=(x, y, ancho, alto))
    # screenshot.show()
    screenshot.save('captura/captura_pantalla_mostruo.png')
    return 'captura/captura_pantalla_mostruo.png'

def capturar_pantalla_hp(x, y, ancho, alto):
    screenshot = pyautogui.screenshot(region=(x, y, ancho, alto))
    # screenshot.show()
    screenshot.save('captura/captura_pantalla_HP.png')
    return 'captura/captura_pantalla_HP.png'

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


def funcionmostruo():
    global stop_flag, bosfinal, dungeon, terminando, ultimo, etapa, terminar, vidamostruo, contadormostruos1, terminarok,atacar

    while not stop_flag and not keyboard.is_pressed('delete'):
        if dungeon == 0 or dungeon == 2 : #or final == 1
            time.sleep(0.5)
            continue

        print("funcionmostruo en ejecución")

        # Realizar todas las búsquedas de imágenes de una vez
        bos3 = buscar_imagen_en_pantalla("ahv/bos3.png")
        if bos3:
            etapa = 0
            terminarok = 1

        terminar = imagenterminar()
        if terminar and dungeon == 1:
            terminarok = 1

        vidamostruo = imagenmostruo()

        if vidamostruo:
            atacar=1
            contadormostruos1 = 0
            print('variable atacar')
            if vidamostruo <= 15:
                keyboard.press_and_release("z")
        else:
            keyboard.press_and_release("z")
            contadormostruos1 += 1
            vidamostruo = imagenmostruo()
            if contadormostruos1 >= 3 and dungeon == 1 and terminarok == 0:
                etapa = 3

        time.sleep(0.1)  # Pequeña pausa para evitar sobrecarga de CPU

    print("funcionmostruo terminada")


def funcionBM():
    global stop_flag, bm3WI1, bm2WI1, vidamostruo, dungeon, tiempo_transcurrido, tiempo_inicio,atacar

    imagen_presente = False
    
    while not stop_flag and not keyboard.is_pressed('delete'):
        if dungeon != 1 or atacar != 1: #
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

# def funcionBM2():
#     global stop_flag, bm3WI1, dungeon, nombre_proceso, vidamostruo, puerta, atacar, puertita, bosfinal

#     while not stop_flag and not keyboard.is_pressed('delete'):
#         print("funcionBM2 en ejecución")
#         time.sleep(0.3)  # Reduced sleep time

#         if not (vidamostruo and dungeon == 1 and atacar == 1 )  :
#             continue


#         if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
#             continue

#         if buscar_imagen_en_pantalla("login/cabal.png"):
#             continue

#         bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
#         mago = buscar_imagen_en_pantalla("otros/mago.png")

#         if bm2WI1 and not mago:
#             for _ in range(10):  # Limit the number of attempts
#                 keyboard.press_and_release("6")
#                 keyboard.press_and_release("space")
#                 time.sleep(0.2)
#                 if not buscar_imagen_en_pantalla("otros/bm2WI1.png"):
#                     break

#         print('ataque normal con monstruos')
#         if  (bm2WI1 and mago): #not bm2WI1 or
#             for tecla in ["2", "3", "4", "8"]:
#                 keyboard.press_and_release(tecla)
#                 keyboard.press_and_release("space")
#                 time.sleep(0.2)

#                 if buscar_imagen_en_pantalla("otros/bm3WI1.png") or not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
#                     keyboard.press_and_release("space")
#                     break

#     print("funcionBM2 terminada")


# def funcionBM3():
#     global stop_flag, bm3WI1, dungeon, vidamostruo, atacar

#     while not stop_flag and not keyboard.is_pressed('delete'):
#         print("funcionBM3 en ejecución")
#         time.sleep(0.5)  # Reducido de 1 a 0.5 segundos

#         if dungeon == 0 or dungeon == 2:
#             time.sleep(0.5)
#             continue

#         if not (vidamostruo and dungeon == 1) and not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
#             continue

#         bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
#         if not bm3WI1:
#             continue

#         ataque_count = 0
#         max_ataques = 15  # Límite de ataques antes de verificar condiciones nuevamente

#         while ataque_count < max_ataques and dungeon == 1:
#             if buscar_imagen_en_pantalla("login/cabal.png"):
#                 break

#             if dungeon == 0 or dungeon == 2:
#                 break

#             print('ataque BM3 con monstruos')
#             keyboard.press_and_release("6")
#             keyboard.press_and_release("space")
#             time.sleep(0.1)  # Reducido de 0.3 a 0.2 segundos

#             if not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
#                 break

#             vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
#             if not vidamostruo:
#                 break

#             ataque_count += 1

#     print("funcionBM3 terminada")

def funcionBM_optimizada():
    global stop_flag, bm3WI1, tiempo_transcurrido, vidamostruo, bosfinal, atacar, dungeon, nombre_proceso, lanzabuff, tiempo_inicio

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
            
            if not (vidamostruo and dungeon == 1 and atacar == 1 and salix ):
                time.sleep(0.3)
                continue

            tiempo_transcurrido = tiempo_actual - tiempo_inicio

            if check_imagen("login/cabal.png", True):
                time.sleep(0.3)
                continue
        if not (vidamostruo and dungeon == 1 and atacar == 1  ):
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
                    
                    if not check_imagen("otros/bm2WI1.png", True):
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
                    if check_imagen("otros/bm3WI1.png", True) or not check_imagen("otros/mostrous.jpg", True):
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
                
                if not bosfinal:
                    keyboard.press_and_release("6")
                    keyboard.press_and_release("space")
                    time.sleep(0.15)  # Reducido de 0.2 a 0.15
                    
                    if not check_imagen("otros/bm3WI1.png", True):
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
                            
                            if not check_imagen("otros/bm3WI1.png", True):
                                break
                
                if not check_imagen("otros/bm3WI1.png", True):
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
                if check_imagen("otros/bm3WI1.png", True) or not check_imagen("otros/mostrous.jpg", True):
                    keyboard.press_and_release("space")
                    time.sleep(0.15)  # Reducido de 0.2 a 0.15
                    break

    print("funcionBM optimizada terminada")

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
    
def funcionfail():
    global stop_flag,muriendo,esperandocuenta,bosscuenta,wavecuenta, dungeon, nombre_proceso, tiempo_inicio, puerta, terminando, terminar, lanzabuff, puertita, atacar, muriendo, fail

    def reset_variables():
        global dungeon,esperandocuenta,wavecuenta,bosscuenta, bosdetectado, terminando, lanzabuff, atacar, terminar, contardg, puerta, puertita, muriendo, vidamostruo, fin2, meta, bosfinal, tiempo_inicio
        dungeon = 2
        bosdetectado = terminando = lanzabuff = atacar = bosscuenta = wavecuenta  = puerta = puertita = esperandocuenta = muriendo = muriendo = 0
        terminar = fin2 = meta = bosfinal = vidamostruo  = False
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

    global dungeon
    global nombre_proceso
    global tiempo_inicio
    global etapa
    global stop_flag
    global terminarok
    global muerte
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionmuerte en ejecución")
        time.sleep(1)
        imagen_a_buscar_muerte = "otros/wrap-dead.bmp"  # Reemplaza con la ruta de tu propia imagen
        muerte = buscar_imagen_en_pantalla(imagen_a_buscar_muerte)

        if muerte!=False and dungeon==1 :
            print('muerte')
            click_raton_posicion (muerte[0], muerte[1])
            imagen_a_buscar_confirmar_muerte = "otros/confirmar_muerte.png"  # Reemplaza con la ruta de tu propia imagen
            confirmar_muerte = buscar_imagen_en_pantalla(imagen_a_buscar_confirmar_muerte)
            if confirmar_muerte!=False:
                print('confirmar_muerte')
                click_raton_posicion (confirmar_muerte[0], confirmar_muerte[1])
                time.sleep(3)
                centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                if centro_ventana2:
                    keyboard.press_and_release("alt+3")
                    time.sleep(1)
                    keyboard.press_and_release("alt+4")
                    time.sleep(1)
                    keyboard.press_and_release("z")
                    etapa=3
                    vidamostruo=False 
                    dungeon=1 
                    terminarok=0 
                    bosfinal=False
                    terminar=False

    print("funcionmuerte terminada")

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

def imagenahv():
    ruta_imagen = 'ahv/despertado.png'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre ahv')
        return False
    else:
        print('encontre ahv')
        return pos

def imagennoentrar():
    imagen_a_buscar = "otros/no_entrada.png"  # Reemplaza con la ruta de tu propia imagen
    pos = buscar_imagen_en_pantalla(imagen_a_buscar)
    if pos== False:
        return False
    else:
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
    
def funcioiniciar():
    global stop_flag, contardg, terminar, wavecuenta, esperandocuenta, bosscuenta, dungeon, nombre_proceso, bosdetectado
    global tiempo_inicio,  conteocabal,  terminando,  atacar, lanzabuff, puerta,etapa

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
        if comentarios  and not buscar_imagen_en_pantalla("otros/selectdg.png"):
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
            time.sleep(1.2)
            keyboard.press_and_release("alt+3")
            time.sleep(1)
            keyboard.press_and_release("alt+4")
            time.sleep(1)
            time.sleep(15)
            keyboard.press_and_release("z")
            # etapa=3
            dungeon=1
            atacar=1
            lanzabuff=1
            contardg=contardg+1
            conteocabal=0
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
    confirmatronco = buscar_imagen_en_pantalla("ahv/confirmatronco.png")
    if confirmatronco:

        click_imagen(confirmatronco,offset_x=-190,offset_y=100)
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

        ahv = imagenahv()
        detected = buscar_imagen_en_pantalla("ahv/detected.png")
        if not detected and ahv:
            click_imagen(ahv)
            time.sleep(1)
            raton_posicion(ahv[0], ahv[1]+30)

        if ahv and detected:
            print('clic ahv')
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



def mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y, duracion_clic=0.7):
    try:
        # Obtener la posición actual del ratón
        posicion_actual = pyautogui.position()

        # Realizar clic derecho y mantenerlo presionado
        pyautogui.mouseDown(button='left')

        time.sleep(1)

        # Función para mover el ratón
        def mover_raton():
            pyautogui.moveRel(desplazamiento_x, desplazamiento_y, duration=duracion_clic)

        # Función para presionar la tecla
        def presionar_tecla():
            keyboard.press_and_release(",")
            time.sleep(0.8)
            keyboard.press_and_release(".")
            time.sleep(0.6)

        # Crear hilos para ejecutar ambas funciones simultáneamente
        hilo_raton = threading.Thread(target=mover_raton)
        hilo_tecla = threading.Thread(target=presionar_tecla)

        # Iniciar los hilos
        hilo_raton.start()
        hilo_tecla.start()

        # Esperar a que ambos hilos terminen
        hilo_raton.join()
        hilo_tecla.join()

        pyautogui.click(button='left')
        print('soy derecha pero me voy a la izquierda')
        # Soltar el clic derecho
        pyautogui.mouseUp(button='left')

    except Exception as e:
        print(f"Error: {e}")

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
    global terminar
    global dungeon
    global vidamostruo
    global etapa
    global terminando
    global ultimo
    global bosfinal
    global nombre_proceso
    global tiempo_inicio
    global terminarok
    global contardgok
    global stop_flag
    global contadormostruos1
    global bm3WI1

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionterminar en ejecución")
        time.sleep(1)
        terminar = imagenterminar()
        time.sleep(1)
        if terminar!= False :
                print('Terminando')
                terminando=1
                etapa=0
                keyboard.press_and_release("space")
                time.sleep(1)
                keyboard.press_and_release("space")
                time.sleep(1)
                keyboard.press_and_release("space")
                time.sleep(1)
                keyboard.press_and_release("space")
                click_raton_posicion (terminar[0], terminar[1])
                time.sleep(1)
        imagen_a_buscar_dungeo = "otros/dungeo.png"  # Reemplaza con la ruta de tu propia imagen
        dungeo = buscar_imagen_en_pantalla(imagen_a_buscar_dungeo)
        time.sleep(0.5)
        if dungeo!=False and dungeon==1:
            stop_flag = False
            contadormostruos1=0
            terminarok=0
            dungeon=2
            etapa=0
            terminando=0
            terminar=False
            vidamostruo=False
            bm3WI1=False
            bosfinal=False
            ultimo=0
            contardgok += 1
            
            tiempo_inicio = time.time()

        if dungeon==2 and dungeo!=False:
            imagen_a_buscar_recibir = "otros/recibir.png"  # Reemplaza con la ruta de tu propia imagen
            recibir = buscar_imagen_en_pantalla(imagen_a_buscar_recibir)
            time.sleep(1)
            if recibir!= False:
                click_raton_posicion (recibir[0], recibir[1])
            imagen_a_buscar_obtenerpuntos = "otros/obtenerpuntos.png"  # Reemplaza con la ruta de tu propia imagen
            obtenerpuntos = buscar_imagen_en_pantalla(imagen_a_buscar_obtenerpuntos)
            time.sleep(1)
            if obtenerpuntos!= False:
                click_raton_posicion (obtenerpuntos[0], obtenerpuntos[1])
            imagen_a_buscar_dado = "otros/dado.png"  # Reemplaza con la ruta de tu propia imagen
            dado = buscar_imagen_en_pantalla(imagen_a_buscar_dado)
            time.sleep(1)
            if dado!= False:
                click_raton_posicion (dado[0], dado[1])
                print('salir1')
                time.sleep(0.5)
                dungeon=0
                    

def funciologin():
    global stop_flag, contardg, dungeon, terminar, nombre_proceso, tiempo_inicio, bosfinal, conteocabal, terminando, atacar,etapa
    
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
                    conteocabal, dungeon, atacar,etapa = 1, 0, 0, 0
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

def detener_todo():
    global stop_flag
    while not stop_flag:
    # Verificar si se presionó la tecla 'End'
        if keyboard.is_pressed('end'):
            stop_flag = True
            print("Parando todas las funciones...")
            break  

def funcionetapa():
    global stop_flag
    
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionetapa en ejecución")
        time.sleep(1)
        global contardg
        global bosfinal
        global dungeon
        global terminar
        global contadormostruos1
        global vidamostruo
        global muerte
        global terminarok
        global etapa
        global nombre_proceso
        global tiempo_inicio
        imagen_a_buscar_dungeo = "otros/dungeo.png"  # Reemplaza con la ruta de tu propia imagen
        dungeo = buscar_imagen_en_pantalla(imagen_a_buscar_dungeo)
        if etapa==0 and vidamostruo!=False  and dungeon==1  and terminar== False and dungeo==False:
            centro_ventana = obtener_centro_ventana(nombre_proceso)
            if centro_ventana:
                print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                raton_posicion (centro_ventana[0], centro_ventana[1])
                posicion_actual = pyautogui.position()

        if etapa>0 and vidamostruo==False  and dungeon==1  and terminar== False:
            if etapa==3:
                print('etapa 3')
                conteo=0
                while True:
                    imagen_a_buscar_cabal = "login/cabal.png"  # Reemplaza con la ruta de tu propia imagen
                    cabal = buscar_imagen_en_pantalla(imagen_a_buscar_cabal)
                    if cabal!=False :
                        break
                    imagen_a_buscar_dungeo = "otros/dungeo.png"  # Reemplaza con la ruta de tu propia imagen
                    dungeo = buscar_imagen_en_pantalla(imagen_a_buscar_dungeo)
                    if etapa>0 and vidamostruo!=False and dungeo==False:
                        centro_ventana = obtener_centro_ventana(nombre_proceso)
                        if centro_ventana:
                            print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                            raton_posicion (centro_ventana[0], centro_ventana[1])
                            posicion_actual = pyautogui.position()

                    if etapa>0 and vidamostruo==False and contadormostruos1>2  and dungeon==1  and terminar== False and dungeo==False:
                        conteo=conteo+1
                        centro_ventana3 = obtener_centro_ventana(nombre_proceso)
                        if contadormostruos1>50:
                            keys = ['w', 'w','w', 'w','w', 'w']
                            hold_time = 1.5  # Tiempo que se mantiene presionada cada tecla (en segundos)
                            delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                            for key in keys:
                                keyboard.press(key)
                                time.sleep(hold_time)
                                keyboard.release(key)
                                time.sleep(delay_between_keys)
                            keyboard.press_and_release("z")
                        if contadormostruos1>65:
                            keys = ['q', 'q','q', 'q','q', 'q']
                            hold_time = 1.5  # Tiempo que se mantiene presionada cada tecla (en segundos)
                            delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                            for key in keys:
                                keyboard.press(key)
                                time.sleep(hold_time)
                                keyboard.release(key)
                                time.sleep(delay_between_keys)
                            contadormostruos1=2
                            keyboard.press_and_release("z")    
                        else:
                            if conteo > 30:
                                valore=-50
                                valoresdesplazamiento_x=350
                                conteo=0
                            
                            if conteo > 15:
                                valore=220
                                valoresdesplazamiento_x=400
                            else:
                                
                                valoresdesplazamiento_x=420
                                valore=180
                        if centro_ventana3:
                            print(f"El centro de la ventana3 de {nombre_proceso} es ({centro_ventana3[0]}, {centro_ventana3[1]}).")
                            raton_posicion (centro_ventana3[0]-400, centro_ventana3[1]-valore)
                            desplazamiento_x =valoresdesplazamiento_x   # Ajusta según sea necesario
                            desplazamiento_y = 0
                            piso1=buscar_imagen_en_pantalla('ahv/piso1.png')
                            if piso1:
                                raton_posicion (piso1[0]-100, piso1[1])
                                posicion_actual = pyautogui.position()
                                time.sleep(0.3)
                                pyautogui.click(button='left')
                                time.sleep(3)

                            
                            mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y)
                            keyboard.press_and_release("z")
                            imagen_a_buscar_bosfinal = "ahv/bos3.png"  # Reemplaza con la ruta de tu propia imagen
                            bosfinal = buscar_imagen_en_pantalla(imagen_a_buscar_bosfinal)
                            time.sleep(1)
                            if bosfinal!=False:
                                keyboard.press_and_release("alt+9")
                                etapa=0
                                terminarok=1
                                centro_ventana = obtener_centro_ventana(nombre_proceso)
                                if centro_ventana and contadormostruos1>8:
                                    print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                                    raton_posicion (centro_ventana[0], centro_ventana[1])
                                    key = 'q'
                                    hold_time = 0.3  # Tiempo que se mantiene presionada cada tecla (en segundos)
                                    delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                                    keyboard.press(key)
                                    time.sleep(hold_time)
                                    keyboard.release(key)
                                    time.sleep(delay_between_keys)
                                    posicion_actual = pyautogui.position()                                                
                                break
                         
                            if vidamostruo!=False:
                                break
                            imagen_a_buscar_fail = "otros/fail.png"  # Reemplaza con la ruta de tu propia imagen
                            fail = buscar_imagen_en_pantalla(imagen_a_buscar_fail)
                            if fail!= False:
                                etapa=0
                                break
                            if muerte!=False:
                                break
                    else:
                        if dungeon==1 :
                            centro_ventana = obtener_centro_ventana(nombre_proceso)
                            if centro_ventana and contadormostruos1>8:
                                print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                                raton_posicion (centro_ventana[0], centro_ventana[1])
                                posicion_actual = pyautogui.position()
                                key = 'q'
                                hold_time = 0.3  # Tiempo que se mantiene presionada cada tecla (en segundos)
                                delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                                keyboard.press(key)
                                time.sleep(hold_time)
                                keyboard.release(key)
                                time.sleep(delay_between_keys)
                                
        else:
            if dungeon==1  and vidamostruo==False:
                centro_ventana = obtener_centro_ventana(nombre_proceso)
                if centro_ventana and contadormostruos1>8:
                    print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                    raton_posicion (centro_ventana[0], centro_ventana[1])
                    posicion_actual = pyautogui.position()
                    key = 'q'
                    hold_time = 0.3  # Tiempo que se mantiene presionada cada tecla (en segundos)
                    delay_between_keys = 0.5  # Tiempo de espera entre soltar una tecla y presionar la siguiente
                    keyboard.press(key)
                    time.sleep(hold_time)
                    keyboard.release(key)
                    time.sleep(delay_between_keys)

# Configurar la función de detección del evento de Escape

def detener_todo():
    """Detener todas las funciones."""
    global stop_flag
    while not stop_flag:
        if keyboard.is_pressed('end'):
            stop_flag = True
            print("Parando todas las funciones...")
            break
        
        

# Inicializar la variable de parada

stop_flag = False
contardg=0
contardgok=0
contadormostruos1=0
dungeon=0
etapa=0
atacar=0
terminando=0
conteocabal=0
terminarok=0
terminar=False
vidamostruo=False
bm3WI1=False
bosfinal=False
reiniciar_flag = False
lanzabuff=0
ultimo=0
reiniciando_en_progreso = False
lock = threading.Lock()  # Lock para proteger acceso a futuros
futuros = {}
nombre_proceso = "cabal"
tiempo_inicio = time.time()
forzar_deshabilitar_bloq_mayus()

# Lista de funciones a ejecutar
funciones = [
    funcionSP,
    funciologin,
    funcionvida,
    funcionmostruo,
    funcionBM,
    # funcionBM3,
    # funcionBM2,
    funcionBM_optimizada,
    funcionfail,
    funcionmuerte,
    funcioiniciar,
    funcionterminar,
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

