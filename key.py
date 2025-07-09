import concurrent.futures
import pyautogui
import pygetwindow as gw
import time
import win32gui
import keyboard

from pynput.mouse import Button, Controller
import time
from screen_search import Search

from os import remove
from PIL import ImageGrab

import os.path as path
import threading


import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os

import ctypes

import math

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
    VK_CAPIWIL = 0x14

    # Obtener el estado actual de Caps Lock
    caps_lock_state = ctypes.windll.user32.GetKeyState(VK_CAPIWIL)

    # Si está activado, envía un evento para desactivarlo
    if caps_lock_state & 1:  # Estado activado
        ctypes.windll.user32.keybd_event(VK_CAPIWIL, 0, 0, 0)  # Pulsar
        ctypes.windll.user32.keybd_event(VK_CAPIWIL, 0, 2, 0)  # Soltar
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

def tomar_captura_ventana(nombre_proceso):
    try:

        ventana = gw.getWindowsWithTitle(nombre_proceso)[0]
        # Define el área de la ventana (izquierda, superior, derecha, inferior)
        ventana_area = (ventana.left, ventana.top, ventana.right, ventana.bottom)

        # Captura la pantalla de la ventana especificada
        captura = ImageGrab.grab(bbox=ventana_area)

        # Guarda la captura de pantalla con un nombre único (usando la hora actual)
        nombre_captura = f"kong/captura_{int(time.time())}.png"
        captura.save(nombre_captura)

        print(f"Captura guardada como {nombre_captura}")
    except Exception as e:
        print(f"Error al capturar la ventana: {e}")

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
        print("funcionSP en ejecución")
        global puerta
        global dungeon
        global atacar
        global contardg
        global contardgok
        global lanzabuff
        global contadormostruos1
        global bosdetectado
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
        print('DGOK: ',contardgok)
        print('dungeon: ',dungeon)
        print('atacar: ',atacar)
        print('contadormostruos1: ',contadormostruos1)
        print('bosdetectado: ',bosdetectado)
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
            if vida <= 40:
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
def funcionmostruokey():
    global stop_flag, bosdetectado, lanzabuff

    boss_images = [
        ("key/bos_name_key7.png", "key/bos_key7.png", "7"),
        ("key/bos_name_key6.png", "key/bos_key6.png", "6"),
        ("key/bos_name_key5.png", "key/bos_key5.png", "5"),
        ("key/bos_name_key4.png", "key/bos_key4.png", "4"),
        ("key/bos_name_key3.png", "key/bos_key3.png", "3"),
        ("key/bos_name_key2.png", "key/bos_key2.png", "2"),
        ("key/bos_name_key1.png", "key/bos_key1.png", "1")
    ]

    caja_images = [
        "otros/caja.png",
        "otros/caja1.png"
    ]

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionmostruokey en ejecución")
        time.sleep(0.5)

        if bosdetectado == 0 and lanzabuff == 1:
            for bos_name, bos_key, num in boss_images:
                bos = buscar_imagen_en_pantalla(bos_name)
                if bos:
                    raton_posicion(bos[0], bos[1]+10)
                    pyautogui.click(button='left')
                    print(f'detecte bos {num}')
                
                bos_key_img = buscar_imagen_en_pantalla(bos_key)
                if bos_key_img:
                    bosdetectado = 1
                    print(f'detecte bos {num}A')
                    break

        for caja_img in caja_images:
            caja = buscar_imagen_en_pantalla(caja_img)
            if caja:
                raton_posicion(caja[0], caja[1]+10)
                pyautogui.click(button='left')
                print(f'detecte {caja_img}')
                for _ in range(30):
                    keyboard.press_and_release("space")
                    time.sleep(0.1)

    print("funcionmostruokey terminada")

def funcionmostruo():
    global stop_flag, contadormostruos1, bosfinal, dungeon, puerta, terminar, bosdetectado
    global terminando, lanzabuff, puertita, vidamostruo, fail

    while not stop_flag and not keyboard.is_pressed('delete'):
        salix = buscar_imagen_en_pantalla("otros/salix.png")

        if  not (dungeon == 1 and salix):
            continue

        print("funcionmostruo en ejecución")

        # Realizar todas las búsquedas de imágenes de una vez
        vidamostruo = imagenmostruo()

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
        
        if contadormostruos1 >=80  and lanzabuff == 1:
            pyautogui.click(button='left')

        time.sleep(0.1)  # Pequeña pausa para evitar sobrecarga de CPU

    print("funcionmostruo terminada")


def funcionBM():
    global stop_flag
    while not stop_flag and not keyboard.is_pressed('delete'):
        global bm3WI1
        global tiempo_transcurrido
        global vidamostruo
        global puerta
        global bosdetectado
        global atacar
        global dungeon
        print("funcionBM en ejecución")
        time.sleep(1)
        tiempo_transcurrido = time.time() - tiempo_inicio
        if vidamostruo!= False and dungeon==1 and puerta == False and atacar==1 :
            imagen_a_buscar_bm2WI = "otros/bm2WI.png"  # Reemplaza con la ruta de tu propia imagen
            bm2WI = buscar_imagen_en_pantalla(imagen_a_buscar_bm2WI)

            imagen_a_buscar_bm2WI1 = "otros/bm2WI1.png"  # Reemplaza con la ruta de tu propia imagen
            bm2WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2WI1)

            imagen_a_buscar_bm2WI2 = "otros/bm2WI2.png"  # Reemplaza con la ruta de tu propia imagen
            bm2WI2 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2WI2)

            imagen_a_buscar_bm3WI = "otros/bm3WI.png"  # Reemplaza con la ruta de tu propia imagen
            bm3WI = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI)

            imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
            bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)

            imagen_a_buscar_bm3WI2 = "otros/bm3WI2.png"  # Reemplaza con la ruta de tu propia imagen
            bm3WI2 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI2)
            if tiempo_transcurrido>(4*60):
                if bm3WI!=False and (bm3WI1==False and bm2WI1==False ):

                    keyboard.press_and_release("f12")
                    time.sleep(0.5)
                    keyboard.press_and_release("f12")
                    time.sleep(0.5)
                    # if bm3WI2!=False:
                    #     time.sleep(2)
                arquero = buscar_imagen_en_pantalla("otros/arquero.png")
                blader = buscar_imagen_en_pantalla("otros/blader.png")
                if bm2WI!=False and ((not arquero  and not blader) or bosdetectado==1) and (bm3WI1==False and bm2WI1==False ):

                    keyboard.press_and_release("f10")
                    time.sleep(0.5)
                    keyboard.press_and_release("f10")
                    time.sleep(0.5)
                    # if bm2WI2!=False:
                    #     time.sleep(5)

    print("funcionBM terminada")

def funcionBM2():
    global stop_flag, bm3WI1, dungeon, nombre_proceso, vidamostruo, puerta, atacar, puertita, bosdetectado

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM2 en ejecución")
        time.sleep(0.3)  # Reduced sleep time

        salix = buscar_imagen_en_pantalla("otros/salix.png")
        
        if  not (dungeon == 1 and atacar == 1 and salix):
            continue

     
        if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
            continue

        if buscar_imagen_en_pantalla("login/cabal.png"):
            continue

        bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
        mago = buscar_imagen_en_pantalla("otros/mago.png")
        
        time.sleep(0.5)
        
        if bm2WI1 and not mago:
            for _ in range(6):  # Limit the number of attempts
                keyboard.press_and_release("6")
                keyboard.press_and_release("space")
                time.sleep(0.2)
                
                if not buscar_imagen_en_pantalla("otros/bm2WI1.png"):
                    continue
        else:
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
    global stop_flag, bm3WI1, dungeon, vidamostruo, atacar

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM3 en ejecución")
        time.sleep(0.5)  # Reducido de 1 a 0.5 segundos
        salix = buscar_imagen_en_pantalla("otros/salix.png")

        if not (vidamostruo and dungeon == 1 and atacar == 1 and salix):
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
                break

            # vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
            # if not vidamostruo:
            #     keyboard.press_and_release("space")
            #     time.sleep(0.3)  # Reducido de 0.5 a 0.3 segundos
            #     break

            ataque_count += 1

    print("funcionBM3 terminada")

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
            
            if not (vidamostruo and dungeon == 1 and atacar == 1 and salix and puerta == False):
                time.sleep(0.3)
                continue

            tiempo_transcurrido = tiempo_actual - tiempo_inicio

            if check_imagen("login/cabal.png", True):
                time.sleep(0.3)
                continue
        if not (vidamostruo and dungeon == 1 and atacar == 1  and puerta == False):
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
                
                if not bosdetectado:
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
    global stop_flag

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionfail en ejecución")
        global dungeon
        global nombre_proceso
        global tiempo_inicio
        global puerta
        global terminando
        global terminar
        global lanzabuff
        global puertita
        global atacar
        global muriendo
        global fail
        time.sleep(1)
        imagen_a_buscar_fail = "otros/fail.png"  # Reemplaza con la ruta de tu propia imagen
        fail = buscar_imagen_en_pantalla(imagen_a_buscar_fail)
        if fail!= False and dungeon==1: #and puertita==0 and terminar== False and muriendo==0
            print('fail')
            click_raton_posicion (fail[0], fail[1])
            dungeon=2
            bosdetectado=0
            terminando=0
            lanzabuff=0
            atacar=0
            terminar= False
            contardg=0
            puerta=0
            terminando=0
            puertita=0
            muriendo=0
            vidamostruo=False
            fin2=False
            meta=False
            bosfinal=False
            tiempo_inicio = time.time()
            time.sleep(0.5)
        if fail!= False and dungeon==2: #and puertita==0 and terminar== False and muriendo==0
            ok=imagenok()
            if ok!= False:
                print('salir2')
                click_raton_posicion (ok[0], ok[1])
                time.sleep(0.5)



    print("funcionfail terminada")

def funcionmuerte():
    global stop_flag

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionmuerte en ejecución")
        global dungeon
        global nombre_proceso
        global tiempo_inicio
        global puerta
        global grupos_imagenes
        global terminar
        global meta
        global lanzabuff
        global muriendo
        global atacar
        time.sleep(1)
        imagen_a_buscar_muerte = "otros/wrap-dead.bmp"  # Reemplaza con la ruta de tu propia imagen
        muerte = buscar_imagen_en_pantalla(imagen_a_buscar_muerte)

        if muerte!=False and dungeon==1 and terminar== False:
            print('muerte')
            muriendo=1
            click_raton_posicion (muerte[0], muerte[1])
            imagen_a_buscar_confirmar_muerte = "otros/confirmar_muerte.png"  # Reemplaza con la ruta de tu propia imagen
            confirmar_muerte = buscar_imagen_en_pantalla(imagen_a_buscar_confirmar_muerte)
            if confirmar_muerte!=False:
                print('confirmar_muerte')
                click_raton_posicion (confirmar_muerte[0], confirmar_muerte[1])
                time.sleep(3)
                lanzabuff=0
                atacar=0

                centro_ventana3 = obtener_centro_ventana(nombre_proceso)
                if centro_ventana3:
                    print(f"El centro de la ventana3 de {nombre_proceso} es ({centro_ventana3[0]}, {centro_ventana3[1]}).")
                    distancia = 450 / math.sqrt(2)  # Calculamos la distancia en X e Y
                    nueva_x = int(centro_ventana3[0] + distancia)
                    nueva_y = int(centro_ventana3[1] - distancia)  # Restamos para mover hacia arriba
                    
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
                    
                    imagenes_a_buscar = ["key/fin.png", "key/fin1.png", "key/fin1_1.png", "key/fin1_2.png", "key/fin1_3.png", "key/fin1_4.png", "key/fin1_5.png", "key/fin1_6.png"]
                    encontrada_imagen = False

                    while not encontrada_imagen:
                        for imagen in imagenes_a_buscar:
                            elemento = buscar_imagen_en_pantalla(imagen)
                            if elemento:
                                angulo = math.radians(158)

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

def imagentren():
    ruta_imagen = 'tren/despertado.png'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre tren')
        return False
    else:
        print('encontre tren')
        return pos

def imagennoentrar():
    imagen_a_buscar = "otros/no_entrada.png"  # Reemplaza con la ruta de tu propia imagen
    pos = buscar_imagen_en_pantalla(imagen_a_buscar)
    if pos== False:
        return False
    else:
        return pos

def imagenkey1():
    ruta_imagen = 'key/L1.jpg'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre key1')
        return False
    else:
        print('encontre key1')
        return pos

def imagenkey2():
    ruta_imagen = 'key/L2.jpg'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre key2')
        return False
    else:
        print('encontre key2')
        return pos

def imagenkey3():
    ruta_imagen = 'key/L3.jpg'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre key3')
        return False
    else:
        print('encontre key3')
        return pos
def imagenkey4():
    ruta_imagen = 'key/L4.jpg'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre key4')
        return False
    else:
        print('encontre key4')
        return pos

def imagenkey5():
    ruta_imagen = 'key/L5.jpg'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre key5')
        return False
    else:
        print('encontre key5')
        return pos

def imagenkey6():
    ruta_imagen = 'key/L6.jpg'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre key6')
        return False
    else:
        print('encontre key6')
        return pos

def imagenkey7():
    ruta_imagen = 'key/L7.jpg'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre key7')
        return False
    else:
        print('encontre key7')
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

def funcioiniciar():
    global stop_flag
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcioiniciar en ejecución ")
        global contardg
        global terminar
        global dungeon
        global meta
        global nombre_proceso
        global bosdetectado
        global tiempo_inicio
        global conteocabal
        global grupos_imagenes
        global terminando
        global confirmatronco
        global puertita
        global lanzabuff
        global atacar
        global fin2
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
            atacar=1
            lanzabuff=1
        imagen_a_buscar_confirmasalir = "otros/confirmasalir.png"  # Reemplaza con la ruta de tu propia imagen
        confirmasalir = buscar_imagen_en_pantalla(imagen_a_buscar_confirmasalir)
        time.sleep(0.5)
        if confirmasalir!=False:
            dungeon=0
            atacar=0
            lanzabuff=0

        imagen_a_buscar_cerrarmen = "otros/cerrarmen.png"  # Reemplaza con la ruta de tu propia imagen
        cerrarmen = buscar_imagen_en_pantalla(imagen_a_buscar_cerrarmen)
        time.sleep(1)
        if cerrarmen!=False and dungeon==0 and not buscar_imagen_en_pantalla("otros/okrecuperar.png") and not notice:
            keyboard.press_and_release("esc")
            while True :
                imagen_a_buscar_cerrarmen = "otros/cerrarmen.png"  # Reemplaza con la ruta de tu propia imagen
                cerrarmen = buscar_imagen_en_pantalla(imagen_a_buscar_cerrarmen)
                if cerrarmen==False:
                    break
                imagen_a_buscar_cabal = "login/cabal.png"  # Reemplaza con la ruta de tu propia imagen
                cabal = buscar_imagen_en_pantalla(imagen_a_buscar_cabal)
                if cabal!=False :
                    break
                time.sleep(1)
                imagen_a_buscar_salirdg = "otros/salirdg.png"
                salirdg = buscar_imagen_en_pantalla(imagen_a_buscar_salirdg)
                time.sleep(1.5)
                if salirdg != False:
                    print('salirdg1')
                    click_raton_posicion(salirdg[0], salirdg[1])
                raton_posicion (cerrarmen[0], cerrarmen[1])
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                pyautogui.click(button='left')
                
        imagen_a_buscar_puerta = "otros/puerta.png"  # Reemplaza con la ruta de tu propia imagen
        puerta = buscar_imagen_en_pantalla(imagen_a_buscar_puerta)
        imagen_a_buscar_comentarios1 = "otros/comentarios1.png"  # Reemplaza con la ruta de tu propia imagen
        comentarios1 = buscar_imagen_en_pantalla(imagen_a_buscar_comentarios1)
        
        if comentarios1!=False and puertita==0 and meta==False and puerta==False and not buscar_imagen_en_pantalla("otros/okrecuperar.png"):
            imagen_a_buscar_salirdg = "otros/salirdg.png"
            salirdg = buscar_imagen_en_pantalla(imagen_a_buscar_salirdg)
            time.sleep(1.5)
            if salirdg != False:
                print('salirdg1')
                click_raton_posicion(salirdg[0], salirdg[1])
            else:
                raton_posicion (comentarios1[0], comentarios1[1])
                posicion_actual = pyautogui.position()
                time.sleep(1)
                pyautogui.click(button='left')
                imagen_a_buscar_poder = "login/poder.png"  # Reemplaza con la ruta de tu propia imagen
                poder = buscar_imagen_en_pantalla(imagen_a_buscar_poder)
                if poder!=False:
                    raton_posicion (poder[0], poder[1])
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    keyboard.press_and_release("F1")
                    time.sleep(0.5)
        imagen_a_buscar_comentarios = "otros/comentarios.png"  # Reemplaza con la ruta de tu propia imagen
        comentarios = buscar_imagen_en_pantalla(imagen_a_buscar_comentarios)
        if comentarios!=False and puertita==0 and meta==False and puerta==False and not buscar_imagen_en_pantalla("otros/okrecuperar.png"):
            imagen_a_buscar_salirdg = "otros/salirdg.png"
            salirdg = buscar_imagen_en_pantalla(imagen_a_buscar_salirdg)
            time.sleep(1.5)
            if salirdg != False:
                print('salirdg1')
                click_raton_posicion(salirdg[0], salirdg[1])
            else:
                raton_posicion (comentarios[0], comentarios[1]-10)
                posicion_actual = pyautogui.position()
                time.sleep(1)
                pyautogui.click(button='left')
                imagen_a_buscar_poder = "login/poder.png"  # Reemplaza con la ruta de tu propia imagen
                poder = buscar_imagen_en_pantalla(imagen_a_buscar_poder)
                if poder!=False:
                    raton_posicion (poder[0], poder[1])
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    keyboard.press_and_release("F1")
                    time.sleep(0.5)
        imagen_a_buscar_party = "otros/party.png"  # Reemplaza con la ruta de tu propia imagen
        party = buscar_imagen_en_pantalla(imagen_a_buscar_party)
        imagen_a_buscar_party1 = "otros/party1.png"  # Reemplaza con la ruta de tu propia imagen
        party1 = buscar_imagen_en_pantalla(imagen_a_buscar_party1)
        if party!=False and party1!=False and dungeon==0:
            raton_posicion (party[0], party[1])
            posicion_actual = pyautogui.position()
            time.sleep(1)
            pyautogui.click(button='left')
        imagen_a_buscar_account_login = "login/account-login.bmp"  # Reemplaza con la ruta de tu propia imagen
        account_login = buscar_imagen_en_pantalla(imagen_a_buscar_account_login)
        imagen_a_buscar_character_list = "login/character-list.bmp"  # Reemplaza con la ruta de tu propia imagen
        character_list = buscar_imagen_en_pantalla(imagen_a_buscar_character_list)
        imagen_a_buscar_recuperardg = "otros/recuperardg.png"  # Reemplaza con la ruta de tu propia imagen
        recuperardg = buscar_imagen_en_pantalla(imagen_a_buscar_recuperardg)
        imagen_a_buscar_okrecuperar = "otros/okrecuperar.png"  # Reemplaza con la ruta de tu propia imagen
        okrecuperar = buscar_imagen_en_pantalla(imagen_a_buscar_okrecuperar)
        imagen_a_buscar_duallogin = "login/duallogin.png"  # Reemplaza con la ruta de tu propia imagen
        duallogin = buscar_imagen_en_pantalla(imagen_a_buscar_duallogin)

        if okrecuperar!=False and notice:
            raton_posicion (okrecuperar[0], okrecuperar[1])
            posicion_actual = pyautogui.position()
            time.sleep(1)
            pyautogui.click(button='left')
            time.sleep(4)
        imagen_a_buscar_confirmatronco = "key/confirmatronco.png"  # Reemplaza con la ruta de tu propia imagen
        confirmatronco = buscar_imagen_en_pantalla(imagen_a_buscar_confirmatronco)
        imagen_a_buscar_server_select = "login/server-select.bmp"  # Reemplaza con la ruta de tu propia imagen
        server_select = buscar_imagen_en_pantalla(imagen_a_buscar_server_select)
        if  confirmatronco==False and   conteocabal==1 and server_select==False:
            pyautogui.scroll(-10000)
        if dungeon==0  and terminar== False and (account_login==False and character_list==False and recuperardg==False and duallogin==False and okrecuperar==False):
            desplazamiento_x = -100  # Ajusta según sea necesario
            desplazamiento_y = 0    # No hay desplazamiento vertical
            centro_ventana = obtener_centro_ventana(nombre_proceso)
            if centro_ventana:
                dungeon=0
                bosdetectado=0
                atacar=0
                terminando=0
                terminar= False
                tiempo_inicio = time.time()
                bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
                bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")

                for bm in [bm3WI1, bm2WI1]:
                    if bm:
                        raton_posicion(bm[0], bm[1]+5)
                        pyautogui.mouseDown(button='right')
                        time.sleep(1.5)  # Mantener el botón presionado por 0.2 segundos
                        pyautogui.mouseUp(button='right')
                        time.sleep(0.5)
                        pyautogui.click(button='right')

                imagen_a_buscar_confirmatronco1 = "key/confirmatronco1.png"  # Reemplaza con la ruta de tu propia imagen
                confirmatronco1 = buscar_imagen_en_pantalla(imagen_a_buscar_confirmatronco1)
                imagen_a_buscar_confirmatronco = "key/confirmatronco.png"  # Reemplaza con la ruta de tu propia imagen
                confirmatronco = buscar_imagen_en_pantalla(imagen_a_buscar_confirmatronco)
                if confirmatronco!=False and confirmatronco1!=False:
                    raton_posicion (confirmatronco[0]-640, confirmatronco[1]+110)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                else:
                    imagen_a_buscar_confirmatronco2 = "key/confirmatronco2.png"  # Reemplaza con la ruta de tu propia imagen
                    confirmatronco2 = buscar_imagen_en_pantalla(imagen_a_buscar_confirmatronco2)
                    if confirmatronco2!=False and confirmatronco1!=False:
                        raton_posicion (confirmatronco2[0]-600, confirmatronco2[1]+235)
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(3)


                imagen_a_buscar_selectdg = "otros/selectdg.png"  # Reemplaza con la ruta de tu propia imagen
                selectdg = buscar_imagen_en_pantalla(imagen_a_buscar_selectdg)
                if selectdg!=False:
                    imagen_a_buscar_dgproceso = "otros/dgproceso.png"  # Reemplaza con la ruta de tu propia imagen
                    dgproceso = buscar_imagen_en_pantalla(imagen_a_buscar_dgproceso)
                    if dgproceso!=False:
                        dungeon=1
                        atacar=1
                        lanzabuff=1
                        time.sleep(0.5)
                    entrar = imagenentrar()
                    if entrar!= False :
                        click_raton_posicion (entrar[0], entrar[1])
                        print('clic entrar1')
                    key7 = imagenkey7()
                    if key7!= False :
                        click_raton_posicion (key7[0], key7[1])
                        print('clic Key7')
                        noentrar = imagennoentrar()
                        entrar = imagenentrar()
                        time.sleep(2)
                        if noentrar!= False :
                            print('clic no entrar7')
                            key6 = imagenkey6()
                            if key6!= False :
                                click_raton_posicion (key6[0], key6[1])
                                print('clic Key6')
                                noentrar = imagennoentrar()
                                entrar = imagenentrar()
                                time.sleep(2)
                                if noentrar!= False :
                                    print('clic no entrar6')
                                    key5 = imagenkey5()
                                    if key5!= False :
                                        click_raton_posicion (key5[0], key5[1])
                                        print('clic Key5')
                                        noentrar = imagennoentrar()
                                        entrar = imagenentrar()
                                        time.sleep(2)
                                        if noentrar!= False :
                                            print('clic no entrar5')
                                            key4 = imagenkey4()
                                            if key4!= False :
                                                click_raton_posicion (key4[0], key4[1])
                                                print('clic Key4')
                                                noentrar = imagennoentrar()
                                                entrar = imagenentrar()
                                                time.sleep(2)
                                                if noentrar!= False :
                                                    print('clic no entrar4')
                                                    key3 = imagenkey3()
                                                    if key3!= False :
                                                        click_raton_posicion (key3[0], key3[1])
                                                        print('clic Key3')
                                                        noentrar = imagennoentrar()
                                                        entrar = imagenentrar()
                                                        time.sleep(2)
                                                        if noentrar!= False :
                                                            print('clic no entrar3')
                                                            key2 = imagenkey2()
                                                            if key2!= False :
                                                                click_raton_posicion (key2[0], key2[1])
                                                                print('clic Key2')
                                                                noentrar = imagennoentrar()
                                                                entrar = imagenentrar()
                                                                time.sleep(2)
                                                                if noentrar!= False :
                                                                    print('clic no entrar2')
                                                                    key1 = imagenkey1()
                                                                    if key1!= False :
                                                                        click_raton_posicion (key1[0], key1[1])
                                                                        print('clic Key1')
                                                                        noentrar = imagennoentrar()
                                                                        entrar = imagenentrar()
                                                                        time.sleep(2)
                                                                        if noentrar!= False :
                                                                            print('clic no entrar1')
                                                                            stop_flag = True
                                                                            # os.system("shutdown /s /t 10")
                                                                            break
                                                                        else:
                                                                            if entrar!= False :
                                                                                click_raton_posicion (entrar[0], entrar[1])
                                                                                print('clic entrar1')
                                                                else:
                                                                    if entrar!= False :
                                                                        click_raton_posicion (entrar[0], entrar[1])
                                                                        print('clic entrar2')
                                                        else:
                                                            if entrar!= False :
                                                                click_raton_posicion (entrar[0], entrar[1])
                                                                print('clic entrar3')
                                                else:
                                                    if entrar!= False :
                                                        click_raton_posicion (entrar[0], entrar[1])
                                                        print('clic entrar4')
                                        else:
                                            if entrar!= False :
                                                click_raton_posicion (entrar[0], entrar[1])
                                                print('clic entrar5')
                                else:
                                    if entrar!= False :
                                        click_raton_posicion (entrar[0], entrar[1])
                                        print('clic entrar6')
                        else:
                            if entrar!= False :
                                click_raton_posicion (entrar[0], entrar[1])
                                print('clic entrar7')
                    time.sleep(1)
                iniciar = imageniniciar()
                imagen_a_buscar_meta = "key/meta1.png"  # Reemplaza con la ruta de tu propia imagen
                # meta = buscar_imagen_en_pantalla(imagen_a_buscar_meta)
                # if  meta!=False:
                #     raton_posicion (meta[0]+116, meta[1])
                #     print('meta1.png')
                
                imagen_a_buscar_cerrarmen = "otros/cerrarmen.png"  # Reemplaza con la ruta de tu propia imagen
                cerrarmen = buscar_imagen_en_pantalla(imagen_a_buscar_cerrarmen)
                time.sleep(0.5)
                imagen_a_buscar_comentarios1 = "otros/comentarios1.png"  # Reemplaza con la ruta de tu propia imagen
                comentarios1 = buscar_imagen_en_pantalla(imagen_a_buscar_comentarios1)
                time.sleep(0.5)
            
                if iniciar!= False   and not (comentarios1 and cerrarmen): #and meta
                    click_raton_posicion (iniciar[0], iniciar[1])
                    lanzabuff=0
                    atacar=0
                    dungeon=1
                    conteocabal=0
                    contardg=contardg+1
                    time.sleep(1)
                    # buscar_y_actuar_en_ventana(nombre_proceso, grupos_imagenes)
                    centro_ventana3 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana3:
                        print(f"El centro de la ventana3 de {nombre_proceso} es ({centro_ventana3[0]}, {centro_ventana3[1]}).")
                        distancia = 450 / math.sqrt(2)  # Calculamos la distancia en X e Y
                        nueva_x = int(centro_ventana3[0] + distancia)
                        nueva_y = int(centro_ventana3[1] - distancia)  # Restamos para mover hacia arriba
                        
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
                        
                        imagenes_a_buscar = ["key/fin.png", "key/fin1.png", "key/fin1_1.png", "key/fin1_2.png", "key/fin1_3.png", "key/fin1_4.png", "key/fin1_5.png", "key/fin1_6.png"]
                        encontrada_imagen = False

                        while not encontrada_imagen:
                            for imagen in imagenes_a_buscar:
                                elemento = buscar_imagen_en_pantalla(imagen)
                                if elemento:
                                    angulo = math.radians(158)

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

                        # imagenes_a_buscar = ["key/fin.png", "key/fin1.png", "key/fin1_1.png", "key/fin1_2.png", "key/fin1_3.png"]
                        # for imagen in imagenes_a_buscar:
                        #     elemento = buscar_imagen_en_pantalla(imagen)
                        #     if elemento:
                        #         raton_posicion(elemento[0]+70, elemento[1]-100)
                        
                else:
                    imagen_a_buscar_salirdg = "otros/salirdg.png"  # Reemplaza con la ruta de tu propia imagen
                    salirdg = buscar_imagen_en_pantalla(imagen_a_buscar_salirdg)
                    time.sleep(1.5)
                    if salirdg!= False:
                        print('salirdg1')
                        click_raton_posicion (salirdg[0], salirdg[1])
            else:
                print(f"El programa {nombre_proceso} no está abierto o no se pudo obtener la información de la ventana.")

    print("funcioiniciar terminada")

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
                    # raton_posicion(pos[0], pos[1] + 75)
                    # pyautogui.click(clicks=2, interval=0.1)
                    keyboard.press_and_release("enter")
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
    global stop_flag, terminar, dungeon, bosdetectado, vidamostruo, puerta, terminando, lanzabuff, nombre_proceso, tiempo_inicio, contardgok, atacar

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionterminar en ejecución")
        time.sleep(0.5)
        terminar = imagenterminar()

        if terminar:
            print('Terminando')
            terminando = 1

            for _ in range(30):
                keyboard.press_and_release("space")
                time.sleep(0.1)

            # Buscar y hacer clic en las imágenes hasta que desaparezcan
            imagenes_a_buscar = {
                "medium": "key/medium.png",
                "low": "key/low.png",
                "ultimete": "key/ultimete.png",
                "ultialtosupermete": "key/altosuper.png"
            }

            todas_desaparecidas = False
            max_intentos = 10  # Número máximo de intentos para evitar bucle infinito
            intentos = 0

            while not todas_desaparecidas and intentos < max_intentos:
                todas_desaparecidas = True
                for nombre, ruta in imagenes_a_buscar.items():
                    try:
                        imagen = buscar_imagen_en_pantalla(ruta)
                        if imagen:
                            todas_desaparecidas = False
                            click_raton_posicion(imagen[0]-30, imagen[1]+10)
                            print(f"Haciendo clic en {nombre}")
                            for _ in range(20):
                                keyboard.press_and_release("space")
                                time.sleep(0.1)
                    except Exception as e:
                        print(f"Error al procesar {nombre}: {e}")

                if todas_desaparecidas:
                    print("Todas las imágenes han desaparecido.")
                    break

                intentos += 1
                if intentos >= max_intentos:
                    print("Se alcanzó el número máximo de intentos.")
                
                time.sleep(1)  # Esperar un segundo antes de volver a buscar

            if not todas_desaparecidas:
                print("No se pudieron procesar todas las imágenes.")

            bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
            bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")

            for bm in [bm3WI1, bm2WI1]:
                if bm:
                    raton_posicion(bm[0], bm[1]+5)
                    pyautogui.mouseDown(button='right')
                    time.sleep(1.5)  # Mantener el botón presionado por 0.2 segundos
                    pyautogui.mouseUp(button='right')
                    time.sleep(0.5)
                    pyautogui.click(button='right')

            if not buscar_imagen_en_pantalla("otros/bm2WI1.png") and not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                click_raton_posicion(terminar[0], terminar[1])
                time.sleep(1.5)


            if not buscar_imagen_en_pantalla("otros/bm2WI1.png") and not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                click_raton_posicion(terminar[0], terminar[1])
                time.sleep(1.5)

        dungeo = buscar_imagen_en_pantalla("otros/dungeo.png")
        if dungeo and dungeon == 1:
            dungeon, bosdetectado, terminando, atacar, lanzabuff = 2, 0, 0, 0, 0
            contardgok += 1
            tiempo_inicio = time.time()
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
                        dungeon = 0
                        break
                
                # Verificar si dungeo sigue existiendo después de cada acción
                if not buscar_imagen_en_pantalla("otros/dungeo.png"):
                    print('Dungeo ya no está visible')
                    dungeon = 0
                    break

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
       
                # while True :
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
                #     keyboard.press_and_release(".")
                #     time.sleep(1)
                #     keyboard.press_and_release(",")
                #     time.sleep(0.9)
                #     keyboard.press_and_release(".")
                #     time.sleep(1)
                #     keyboard.press_and_release("z")
                #     vidamostruo = imagenmostruo()
                #     time.sleep(0.5)
                #     if vidamostruo!= False:
                #         print('fin de puerta')
                #         time.sleep(0.5)
                #         keyboard.press_and_release("ctrl+8")
                #         time.sleep(0.5)
                #         keyboard.press_and_release("ctrl+7")
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



# Configurar la función de detección del evento de Escape
# Define los grupos de imágenes y sus acciones correspondientes , "key/meta2.png",, "key/meta4.png", "key/meta3.png", "key/meta1.png"
grupos_imagenes = {
    "grupo1": {
        "imagenes": ["key/meta1.png"],
        "accion": lambda posicion: (
            raton_posicion(posicion[0] + 116, posicion[1]),
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
    "grupo2": {
        "imagenes": ["key/fin.png", "key/fin1.png", "key/fin1_1.png", "key/fin1_2.png", "key/fin1_3.png"],
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
        "imagenes": ["key/fin2.png", "key/fin3.png", "key/fin4.png"],
        "accion": lambda posicion: (
            raton_posicion(posicion[0]+30, posicion[1] - 120)
        )
    },
}

def ajustar_area_ventana(area):
    margen_superior = 30  # Ajusta según el tamaño de la barra de título
    margen_lateral = 5    # Ajusta según el tamaño de los bordes laterales
    x1, y1, x2, y2 = area
    return (x1 + margen_lateral, y1 + margen_superior, x2 - margen_lateral, y2 - margen_lateral)

def obtener_area_ventana(nombre_proceso):
    ventana = win32gui.FindWindow(None, nombre_proceso)
    if ventana == 0:
        print("Ventana no encontrada.")
        return None
    rect = win32gui.GetWindowRect(ventana)
    return ajustar_area_ventana(rect)

def buscar_imagen_en_pantalla2(imagen_path, area=None, confianza=0.9):
    imagen = cv2.imread(imagen_path)
    if imagen is None:
        print(f"No se pudo cargar la imagen {imagen_path}")
        return False, None
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    try:
        if area:
            captura_pantalla = pyautogui.screenshot(region=area)
        else:
            captura_pantalla = pyautogui.screenshot()
        captura_pantalla_np = np.array(captura_pantalla)
        captura_pantalla_cv = cv2.cvtColor(captura_pantalla_np, cv2.COLOR_RGB2BGR)
        captura_pantalla_gris = cv2.cvtColor(captura_pantalla_cv, cv2.COLOR_BGR2GRAY)

        coincidencias = cv2.matchTemplate(captura_pantalla_gris, imagen_gris, cv2.TM_CCOEFF_NORMED)
        loc = np.where(coincidencias >= confianza)

        if len(loc[0]) > 0:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(coincidencias)
            imagen_h, imagen_w = imagen_gris.shape
            pos_x = max_loc[0] + (imagen_w // 2)  # Coordenada x del centro de la imagen encontrada
            pos_y = max_loc[1] + (imagen_h // 2)  # Coordenada y del centro de la imagen encontrada
            return True, (pos_x + area[0], pos_y + area[1]) if area else (pos_x, pos_y)
        else:
            return False, None

    except Exception as e:
        print(f"Error al buscar la imagen: {e}")
        return False, None



def buscar_y_actuar_en_ventana(nombre_proceso, grupos_imagenes, intervalo=0.05):
    global grupo_actual

    print("Buscando imágenes en tiempo real en la ventana especificada. Presiona Ctrl+C para detener.")

    grupo_actual = "grupo1"
    coordenadas_guardadas = None
    clic_continuo = False
    ultima_ejecucion_grupo1 = time.time()

    while True :
        imagen_a_buscar_cabal = "login/cabal.png"  # Reemplaza con la ruta de tu propia imagen
        cabal = buscar_imagen_en_pantalla(imagen_a_buscar_cabal)
        if cabal!=False :
            break
        global lanzabuff
        global fail
        global puertita
        global meta
        area_ventana = obtener_area_ventana(nombre_proceso)
        # tomar_captura_ventana(nombre_proceso)
        if not area_ventana:
            continue

        # Función para buscar imágenes de un grupo en paralelo
        def buscar_en_grupo(grupo):
            encontrado = False
            posicion_detectada = None
            for imagen_path in grupos_imagenes[grupo]["imagenes"]:
                encontrado, posicion = buscar_imagen_en_pantalla2(imagen_path, area=area_ventana)
                if encontrado:
                    posicion_detectada = posicion
                    break
            return encontrado, posicion_detectada

        # Hilos para buscar en los grupos simultáneamente
        hilos = []
        resultados = {}

        def buscar_grupo(grupo):
            encontrado, posicion = buscar_en_grupo(grupo)
            resultados[grupo] = (encontrado, posicion)

        for grupo in ["grupo1", "grupo2", "grupo3"]:
            hilo = threading.Thread(target=buscar_grupo, args=(grupo,))
            hilos.append(hilo)
            hilo.start()

        # Espera a que todos los hilos terminen
        for hilo in hilos:
            hilo.join()

        # Procesar los resultados
        if resultados["grupo1"][0]:
            print(f"Imagen del grupo 1 detectada en la ventana {nombre_proceso}.")
            grupos_imagenes["grupo1"]["accion"](resultados["grupo1"][1])
            coordenadas_guardadas = resultados["grupo1"][1]
            clic_continuo = False
            ultima_ejecucion_grupo1 = time.time()
        elif resultados["grupo2"][0]:
            print(f"Imagen del grupo 2 detectada en la ventana {nombre_proceso}.")
            grupos_imagenes["grupo2"]["accion"](resultados["grupo2"][1])
            grupo_actual = "grupo2"
            clic_continuo = False
            meta=False
            break
        elif resultados["grupo3"][0]:
            print(f"Imagen del grupo 3 detectada en la ventana {nombre_proceso}.")
            grupos_imagenes["grupo3"]["accion"](resultados["grupo3"][1])
            grupo_actual = "grupo3"
            clic_continuo = False

        # Continúa el clic en las coordenadas guardadas si se ha detectado previamente
        if clic_continuo:
            tiempo_espera = time.time() - ultima_ejecucion_grupo1
            if tiempo_espera > 40:  # Tiempo máximo de espera sin detección
                clic_continuo = False
            else:
                print(f"Continuando clic en las coordenadas guardadas: {coordenadas_guardadas}")
                raton_posicion(coordenadas_guardadas[0] + 116, coordenadas_guardadas[1])
                pyautogui.mouseDown(button='left')
                time.sleep(0.5)
                pyautogui.mouseUp(button='left')
        # vidamostruo = imagenmostruo()

        # if lanzabuff == 1 or puertita==1 or fail!= False or vidamostruo!= False:
        #     break

        time.sleep(intervalo)

# Inicializar la variable de parada
stop_flag = False
contardg=0
contardgok=0
contadormostruos1=0
dungeon=0
atacar=0
bosdetectado=0
puerta=0
terminar=False
terminando=0
puertita=0
muriendo=0
conteocabal=0
vidamostruo=False
fin2=False
meta=False
bm3WI1=False
tronco=False
lanzabuff=0
bosfinal=False
confirmatronco=False
fail=False
reiniciar_flag = False
reiniciando_en_progreso = False
lock = threading.Lock()  # Lock para proteger acceso a futuros
futuros = {}
nombre_proceso = "cabal"
grupo_actual="grupo1"
tiempo_inicio = time.time()
forzar_deshabilitar_bloq_mayus()
# Lista de funciones a ejecutar
funciones = [
    funcionSP,
    funciologin,
    funcionmostruokey,
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
