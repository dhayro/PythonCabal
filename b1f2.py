import concurrent.futures
import pyautogui
import pygetwindow as gw
import time

import keyboard

from pynput.mouse import Button, Controller
import time
from screen_search import Search

import threading

from os import remove

import os.path as path

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os

import ctypes

import tkinter as tk
from tkinter import ttk

def crear_ventana_info():
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

    etiqueta_contadormostruos1 = ttk.Label(ventana, text="contadormostruos1: ")
    etiqueta_contadormostruos1.pack()

    etiqueta_etapa = ttk.Label(ventana, text="Etapa inicial: ")
    etiqueta_etapa.pack()

    def actualizar_info():
        global  contardg, atacar, etapa,contarsp,contardgok,contadormostruos1
        etiqueta_sp.config(text=f"Número de sp: {contarsp}")
        etiqueta_dg.config(text=f"DG : {contardg}")
        etiqueta_dgok.config(text=f"DG ok: {contardgok}")
        etiqueta_contadormostruos1.config(text=f"contadormostruos1: {contadormostruos1}")
        etiqueta_atacar.config(text=f"Atacar: {atacar}")
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

import threading
thread_ventana = threading.Thread(target=iniciar_ventana_info)
thread_ventana.start()


# Constantes
VK_CAPIWIL = 0x14
mouse = Controller()
stop_flag = False

def forzar_deshabilitar_bloq_mayus():
    caps_lock_state = ctypes.windll.user32.GetKeyState(VK_CAPIWIL)
    if caps_lock_state & 1:
        ctypes.windll.user32.keybd_event(VK_CAPIWIL, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_CAPIWIL, 0, 2, 0)
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

            if imagen_path.startswith("b1f/"):
                print(f"Imagen encontrada en ({centro_x_global}, {centro_y_global}) - {imagen_path}")
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
    global etapa
    global contardg
    global lanzabuff
    global stop_flag
    global contardgok
    global contarsp

    global atacar
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionSP en ejecución")
        time.sleep(1)
        imagen_a_buscar_bufsp = "otros/bufsp.png"  # Reemplaza con la ruta de tu propia imagen
        bufsp = buscar_imagen_en_pantalla(imagen_a_buscar_bufsp)
        if bufsp!=False and lanzabuff==1 :
            keyboard.press_and_release("f8")
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
        contarsp = len(ctns)
        # print('Número de sp: ', len(ctns))
        # print('DG1: ',contardg)
        # print('atacar: ',atacar)
        # print('DGOK: ',contardgok)

        # print('etapa inicial: ',etapa)
        # if len(ctns)==0:
        #     keyboard.press_and_release("-")

    print("funcionSP terminada")
def imagenhp():
    search = buscar_imagen_en_pantalla("otros/vida.png")
    if search == False:
        return False

    # Capturar directamente la región de interés
    # x, y = int(search[0])-37, int(search[1])-14
    x, y = int(search[0])-7, int(search[1])-14
    screenshot = pyautogui.screenshot(region=(x, y, 145, 15))
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


    print(f"Porcentaje de HP: {total_percentage:.2f}% (Rojo: {red_percentage:.2f}%, Verde: {green_percentage:.2f}%)")
    return total_percentage

def funcionvida():
    global stop_flag, tiempo_inicio, lanzabuff
    last_print_time = time.time()
    print_interval = 2  # Imprimir cada 2 segundos

    # Configuración de cooldowns (en segundos)
    cooldown_f5 = 60
    cooldown_f6 = 180
    cooldown_ctrl9 = 6  # Cooldown específico para ctrl+9

    # Tiempo del último uso de cada habilidad
    last_use_f5 = 0
    last_use_f6 = 0
    last_use_ctrl9 = 0  # Inicializar el último uso de ctrl+9

    def use_skill(skill_number, ctrl_number):
        print(f"Usando habilidad {skill_number} con ctrl+{ctrl_number}")
        time.sleep(0.2)
        keyboard.press_and_release(skill_number)
        time.sleep(0.5)
        keyboard.press_and_release(f"ctrl+{ctrl_number}")
        print(f"Habilidad {skill_number} usada")
        return time.time()

    while not stop_flag and not keyboard.is_pressed('delete'):
        current_time = time.time()
        if current_time - last_print_time >= print_interval:
            tiempo_transcurrido = current_time - tiempo_inicio
            print(f"funcionvida en ejecución. Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos")
            last_print_time = current_time

        vida = imagenhp()
        if vida != False :  # and lanzabuff == 1
            print(f"Nivel de vida actual: {vida}")

            # Usar ctrl+9 cada 6 segundos si la vida es menor o igual a 50
            if vida <= 35 :#and current_time - last_use_ctrl9 >= cooldown_ctrl9
                keyboard.press_and_release("ctrl+9")
                print("Usado ctrl+9")
                last_use_ctrl9 = current_time


            if vida <= 10 and current_time - last_use_f6 >= cooldown_f6:
                last_use_f6 = use_skill("f6", 2)
            elif vida <= 25 and current_time - last_use_f5 >= cooldown_f5:
                last_use_f5 = use_skill("f5", 1)
                time.sleep(0.5)
                vida = imagenhp()
                print(f"Nivel de vida después de usar habilidad 5: {vida}")

        time.sleep(0.5)  # Reducido el tiempo de espera

    print("funcionvida terminada")
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


def funcionmostruo():
    global stop_flag, contadormostruos1, bosfinal, dungeon, terminar,atacar
    global terminando, lanzabuff, vidamostruo

    while not stop_flag and not keyboard.is_pressed('delete'):
        imagen_a_buscar_bosfinal = "b1f/bosfinal.png"  # Reemplaza con la ruta de tu propia imagen
        bosfinal = buscar_imagen_en_pantalla(imagen_a_buscar_bosfinal)
        time.sleep(0.5)
        if bosfinal!=False:
            etapa=11
        imagen_a_buscar_caja = "b1f/caja.png"  # Reemplaza con la ruta de tu propia imagen
        caja = buscar_imagen_en_pantalla(imagen_a_buscar_caja)
        time.sleep(0.5)
        if caja!=False:
            etapa=11
        imagen_a_buscar_bosfinal_name = "b1f/bosfinal_name.png"  # Reemplaza con la ruta de tu propia imagen
        bosfinal_name = buscar_imagen_en_pantalla(imagen_a_buscar_bosfinal_name)
        time.sleep(0.5)
        if bosfinal_name!=False:
            etapa=11
        vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
        if not vidamostruo:
           contadormostruos1 += 1
        else:
            atacar=1
        if dungeon != 1 or atacar == 0:
            time.sleep(0.5)
            continue

        print("funcionmostruo en ejecución")

        # Realizar todas las búsquedas de imágenes de una vez

        if vidamostruo:
            lanzabuff=1
            contadormostruos1 = 0
            print('variable atacar')
            while vidamostruo and not stop_flag and not keyboard.is_pressed('delete'):
                if not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                    break
        else:
            keyboard.press_and_release("z")
            if contadormostruos1>=2:
                atacar=0
                lanzabuff=0

        time.sleep(0.1)  # Pequeña pausa para evitar sobrecarga de CPU

    print("funcionmostruo terminada")
# def funcionmostruo():

#     global contadormostruos1
#     global stop_flag
#     global bosfinal
#     global dungeon
#     global etapa
#     global terminar
#     global vidamostruo
#     global terminando
#     global final
#     global atacar
#     global lanzabuff
#     while not stop_flag and not keyboard.is_pressed('delete'):
#         if dungeon==1 and atacar==1 and terminando==0:
#             print("funcionmostruo en ejecución")
#             time.sleep(0.5)
#             imagen_a_buscar_vidamostruo = "otros/mostrous.jpg"  # Reemplaza con la ruta de tu propia imagen
#             vidamostruo = buscar_imagen_en_pantalla(imagen_a_buscar_vidamostruo)
#             if vidamostruo!= False:
#                 contadormostruos1=0
#                 atacar=1
#                 lanzabuff=1
#                 imagen_a_buscar_bosfinal = "b1f/bosfinal.png"  # Reemplaza con la ruta de tu propia imagen
#                 bosfinal = buscar_imagen_en_pantalla(imagen_a_buscar_bosfinal)
#                 time.sleep(0.5)
#                 if bosfinal!=False:
#                     etapa=11
#                 imagen_a_buscar_caja = "b1f/caja.png"  # Reemplaza con la ruta de tu propia imagen
#                 caja = buscar_imagen_en_pantalla(imagen_a_buscar_caja)
#                 time.sleep(0.5)
#                 if caja!=False:
#                     etapa=11
#                 imagen_a_buscar_bosfinal_name = "b1f/bosfinal_name.png"  # Reemplaza con la ruta de tu propia imagen
#                 bosfinal_name = buscar_imagen_en_pantalla(imagen_a_buscar_bosfinal_name)
#                 time.sleep(0.5)
#                 if bosfinal_name!=False:
#                     etapa=11
#                 # etapa=0
#                 print('variable atacar')

#             else:
#                 keyboard.press_and_release("z")
#                 contadormostruos1=contadormostruos1+1
#                 if contadormostruos1>=5 and dungeon==1:
#                     atacar=0
#                     lanzabuff=0

#         if dungeon==1 and atacar==0 and terminando==0:
#             print("funcionmostruo en ejecución")
#             time.sleep(0.5)
#             imagen_a_buscar_vidamostruo = "otros/mostrous.jpg"  # Reemplaza con la ruta de tu propia imagen
#             vidamostruo = buscar_imagen_en_pantalla(imagen_a_buscar_vidamostruo)
#             if vidamostruo!= False:
#                 atacar=1
#                 lanzabuff=1


#     print("funcionmostruo terminada")


def funcionBM():
    global bm3WI1
    global etapa
    global dungeon
    global atacar
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionBM en ejecución")
        time.sleep(1)
        if vidamostruo!= False and atacar==1 and dungeon==1 and etapa>0 :
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
            if bm3WI!=False and etapa>0 and (bm3WI1==False and bm2WI1==False ):
                # raton_posicion (bm3WI[0], bm3WI[1])
                # posicion_actual = pyautogui.position()
                # pyautogui.click(button='right')
                # pyautogui.click(button='right')
                keyboard.press_and_release("f12")
                time.sleep(0.5)
                keyboard.press_and_release("f12")
                time.sleep(0.5)
                if bm3WI2!=False:
                    time.sleep(2)
            # if bm2WI!=False and (bm3WI1==False and bm2WI1==False ):
            #     # raton_posicion (bm2WI[0], bm2WI[1])
            #     # posicion_actual = pyautogui.position()
            #     # pyautogui.click(button='right')
            #     # pyautogui.click(button='right')
            #     keyboard.press_and_release("1")
            #     time.sleep(0.5)
            #     keyboard.press_and_release("f10")
            #     time.sleep(0.5)
            #     if bm2WI2!=False:
            #         time.sleep(5)

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
                
                time.sleep(0.2)
                if not buscar_imagen_en_pantalla("otros/bm2WI1.png"):
                    break

        print('ataque normal con monstruos')
        if  (bm2WI1 and mago) or not bm2WI1: #not bm2WI1 or
            for tecla in ["2", "3", "4", "8"]:
                keyboard.press_and_release(tecla)
                
                time.sleep(0.2)

                if buscar_imagen_en_pantalla("otros/bm3WI1.png") or not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                    
                    break

    print("funcionBM2 terminada")

# def funcionBM2():
#     global bm3WI1
#     global dungeon
#     global contadormostruos1
#     global nombre_proceso
#     global vidamostruo
#     global stop_flag
#     global etapa
#     while not stop_flag and not keyboard.is_pressed('delete'):
#         print("funcionBM2 en ejecución")
#         time.sleep(1)
#         if vidamostruo!= False and dungeon==1 and etapa>0 and atacar==1:

#             while True:
#                 # centro_ventananormal = obtener_centro_ventana(nombre_proceso)
#                 # print(f"El centro de la ventananormal de {nombre_proceso} es ({centro_ventananormal[0]}, {centro_ventananormal[1]}).")
#                 # raton_posicion (centro_ventananormal[0], centro_ventananormal[1])

#                 print('ataque normal con mostruos')

#                 keyboard.press_and_release("2")
#                 # keyboard.press_and_release("z")
#                 time.sleep(0.5)

#                 imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
#                 bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
#                 if bm3WI1!=False:
#                     break
#                 # if vidamostruo==False and contadormostruos1>=1:
#                 #     keyboard.press_and_release("z")
#                 #     time.sleep(0.5)
#                 #     break

#                 keyboard.press_and_release("3")
#                 # keyboard.press_and_release("z")
#                 time.sleep(0.5)

#                 imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
#                 bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
#                 if bm3WI1!=False:
#                     break
#                 # if vidamostruo==False and contadormostruos1>=1:
#                 #     keyboard.press_and_release("z")
#                 #     time.sleep(0.5)
#                 #     break

#                 keyboard.press_and_release("4")
#                 # keyboard.press_and_release("z")
#                 time.sleep(0.5)

#                 imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
#                 bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
#                 if bm3WI1!=False:
#                     break
#                 # if vidamostruo==False and contadormostruos1>=1:
#                 #     keyboard.press_and_release("z")
#                 #     time.sleep(0.5)
#                 #     break

#                 keyboard.press_and_release("8")
#                 # keyboard.press_and_release("z")
#                 time.sleep(0.5)

#                 imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
#                 bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
#                 if bm3WI1!=False:
#                     break
#                 # if vidamostruo==False and contadormostruos1>=1:
#                 #     keyboard.press_and_release("z")
#                 #     time.sleep(0.5)
#                 #     break

#     print("funcionBM2 terminada")

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

        while ataque_count < max_ataques and dungeon == 1 and bm3WI1 and vidamostruo:
            if buscar_imagen_en_pantalla("login/cabal.png"):
                break

            if dungeon == 0 or dungeon == 2:
                break

            print('ataque BM3 con monstruos')
            keyboard.press_and_release("6")
            
            time.sleep(0.1)  # Reducido de 0.3 a 0.2 segundos

            if not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                break

            vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
            if not vidamostruo:
                break

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

def funcionfail():

    global dungeon
    global nombre_proceso
    global tiempo_inicio
    global etapa
    global stop_flag
    global terminar
    global terminando
    global vidamostruo
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionfail en ejecución")
        time.sleep(1)
        imagen_a_buscar_fail = "otros/fail.png"  # Reemplaza con la ruta de tu propia imagen
        fail = buscar_imagen_en_pantalla(imagen_a_buscar_fail)
        if fail!= False and dungeon==1 and terminar== False:
            print('fail')
            click_raton_posicion (fail[0], fail[1])
            ok=imagenok()
            if ok!= False:
                print('salir2')
                click_raton_posicion (ok[0], ok[1])
                dungeon=0
                etapa=0
                bosfinal=False
                final=0
                terminar= False
                terminando=0
                vidamostruo=False
                tiempo_inicio = time.time()
                time.sleep(3)

    print("funcionfail terminada")

def funcionmuerte():

    global dungeon
    global nombre_proceso
    global tiempo_inicio
    global etapa
    global final
    global terminar
    global stop_flag
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionmuerte en ejecución")
        time.sleep(1)
        imagen_a_buscar_muerte = "otros/wrap-dead.bmp"  # Reemplaza con la ruta de tu propia imagen
        muerte = buscar_imagen_en_pantalla(imagen_a_buscar_muerte)

        if muerte!=False and dungeon==1 and terminar== False:
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
                    etapa=0

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

def imagenb1f():
    ruta_imagen = 'b1f/entrada.png'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre b1f')
        return False
    else:
        print('encontre b1f')
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

    global stop_flag

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcioiniciar en ejecución")
        global contardg
        global dungeon
        global terminar
        global nombre_proceso
        global tiempo_inicio
        global bosfinal
        global conteocabal
        global final
        global terminando
        global atacar
        global etapa
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
            # atacar=1
            # lanzabuff=1
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
            while True :
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
                imagen_a_buscar_cerrarmen = "otros/cerrarmen.png"  # Reemplaza con la ruta de tu propia imagen
                cerrarmen = buscar_imagen_en_pantalla(imagen_a_buscar_cerrarmen)
                if cerrarmen==False:
                    break
        imagen_a_buscar_puerta = "otros/puerta.png"  # Reemplaza con la ruta de tu propia imagen
        puerta = buscar_imagen_en_pantalla(imagen_a_buscar_puerta)
        # imagen_a_buscar_comentarios1 = "otros/comentarios1.png"  # Reemplaza con la ruta de tu propia imagen
        # comentarios1 = buscar_imagen_en_pantalla(imagen_a_buscar_comentarios1)

        # if comentarios1!=False  and puerta==False and not buscar_imagen_en_pantalla("otros/okrecuperar.png"):
        #     imagen_a_buscar_salirdg = "otros/salirdg.png"
        #     salirdg = buscar_imagen_en_pantalla(imagen_a_buscar_salirdg)
        #     time.sleep(1.5)
        #     if salirdg != False:
        #         print('salirdg1')
        #         click_raton_posicion(salirdg[0], salirdg[1])
        #     else:
        #         raton_posicion (comentarios1[0], comentarios1[1])
        #         posicion_actual = pyautogui.position()
        #         time.sleep(1)
        #         pyautogui.click(button='left')
        #         imagen_a_buscar_poder = "login/poder.png"  # Reemplaza con la ruta de tu propia imagen
        #         poder = buscar_imagen_en_pantalla(imagen_a_buscar_poder)
        #         if poder!=False:
        #             raton_posicion (poder[0], poder[1])
        #             posicion_actual = pyautogui.position()
        #             time.sleep(1)
        #             pyautogui.click(button='left')
        #             time.sleep(0.5)
        #             keyboard.press_and_release("f1")
        #             time.sleep(0.5)
        imagen_a_buscar_comentarios = "otros/comentarios.png"  # Reemplaza con la ruta de tu propia imagen
        comentarios = buscar_imagen_en_pantalla(imagen_a_buscar_comentarios)
        if comentarios!=False and puerta==False and not buscar_imagen_en_pantalla("otros/okrecuperar.png"):
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
                    keyboard.press_and_release("f1")
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
        # imagen_a_buscar_confirmatronco = "key/confirmatronco.png"  # Reemplaza con la ruta de tu propia imagen
        # confirmatronco = buscar_imagen_en_pantalla(imagen_a_buscar_confirmatronco)
        imagen_a_buscar_server_select = "login/server-select.bmp"  # Reemplaza con la ruta de tu propia imagen
        server_select = buscar_imagen_en_pantalla(imagen_a_buscar_server_select)

        if conteocabal==1 and (account_login==False and character_list==False and recuperardg==False and duallogin==False and okrecuperar==False and server_select==False):
            keyboard.press("ctrl")
            time.sleep(1)
            keyboard.press_and_release("a")
            time.sleep(1)
            keyboard.press_and_release("a")
            time.sleep(1)
            keyboard.press_and_release("a")
            time.sleep(1)
            keyboard.press_and_release("a")
            time.sleep(1)
            keyboard.release("ctrl")
        print("kong27")
        if dungeon==0 and terminar== False and (account_login==False and character_list==False and recuperardg==False and duallogin==False and okrecuperar==False):
            centro_ventana = obtener_centro_ventana(nombre_proceso)
            if centro_ventana:
                dungeon=0
                etapa=0
                terminar= False
                bosfinal=False
                terminando=0
                final=0
                tiempo_inicio = time.time()
                imagen_a_buscar_bm2WI1 = "otros/bm2WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm2WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2WI1)

                imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                time.sleep(1)
                if bm3WI1!=False:
                    raton_posicion (bm3WI1[0], bm3WI1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
                    pyautogui.click(button='right')
                time.sleep(1)
                if bm2WI1!=False:
                    raton_posicion (bm2WI1[0], bm2WI1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
                    pyautogui.click(button='right')
                keyboard.press_and_release("f8")
                time.sleep(1)
                print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                raton_posicion (centro_ventana[0], centro_ventana[1]-120)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(0.5)
                # keyboard.release("alt")
                # time.sleep(0.5)
                raton_posicion (centro_ventana[0], centro_ventana[1]-20)
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(1)
                # pyautogui.click(button='left')
                # raton_posicion (centro_ventana[0], centro_ventana[1]+20)
                imagen_a_buscar_selectdg = "otros/selectdg.png"  # Reemplaza con la ruta de tu propia imagen
                selectdg = buscar_imagen_en_pantalla(imagen_a_buscar_selectdg)
                time.sleep(1)
                if selectdg!=False:
                    B1f = imagenb1f()
                    if B1f!= False :
                        # click_raton_posicion (B1f[0], B1f[1])
                        print('clic b1f')
                        noentrar = imagennoentrar()
                        entrar = imagenentrar()
                        time.sleep(2)
                        if noentrar!= False :
                            print('clic no entrar b1f')
                            stop_flag = True
                            os.system("shutdown /s /t 10")
                            break
                        else:
                            if entrar!= False :
                                click_raton_posicion (entrar[0], entrar[1])
                                print('clic entrar b1f')
                    time.sleep(1)
                iniciar = imageniniciar()
                if iniciar!= False :
                    click_raton_posicion (iniciar[0], iniciar[1])
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                        # time.sleep(0.5)
                        # keyboard.press_and_release("alt+3")
                        # time.sleep(1)
                        # keyboard.press_and_release("alt+4")
                        time.sleep(0.5)
                        keyboard.press("+")
                        time.sleep(1.5)
                        keyboard.release("+")
                        time.sleep(0.5)
                        # keyboard.press("alt")
                        # time.sleep(0.5)
                        # keyboard.press_and_release("2")
                        # time.sleep(0.9)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                        # keyboard.release("alt")
                        # time.sleep(0.5)
                        keyboard.press_and_release("z")
                        time.sleep(0.3)
                        keyboard.press_and_release("f12")
                        time.sleep(0.5)
                        keyboard.press_and_release("f12")
                        time.sleep(0.5)
                        etapa=1
                        dungeon=1
                        atacar=1
                        conteocabal=0
                        contardg=contardg+1
                        time.sleep(1)

            else:
                print(f"El programa {nombre_proceso} no está abierto o no se pudo obtener la información de la ventana.")

    print("funcioiniciar terminada")

def mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y, duracion_clic=1):
    try:
        # Obtener la posición actual del ratón
        posicion_actual = pyautogui.position()

        # Realizar clic derecho y mantenerlo presionado
        pyautogui.mouseDown(button='left')

        # Mover el ratón con desplazamiento
        pyautogui.moveRel(desplazamiento_x, desplazamiento_y, duration=duracion_clic)

        pyautogui.click(button='left')
        print('soy derecha pero me voy a la izquierda')
        # Soltar el clic derecho
        pyautogui.mouseUp(button='left')

        pyautogui.click(button='left')
        pyautogui.click(button='left')
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
    global terminar
    global dungeon
    global vidamostruo
    global etapa
    global final
    global nombre_proceso
    global terminando
    global contardgok
    global tiempo_inicio
    global stop_flag
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionterminar en ejecución")
        time.sleep(1)
        terminar = imagenterminar()
        time.sleep(1)
        if terminar!= False and dungeon==1:
                print('Terminando')
                final=1
                etapa=11
                terminando=1
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
                time.sleep(1)
                keyboard.press_and_release("space")
                time.sleep(1)
                keyboard.press_and_release("space")
                time.sleep(1)
                keyboard.press_and_release("space")
                time.sleep(1)
                keyboard.press_and_release("space")
                click_raton_posicion (terminar[0], terminar[1])
                time.sleep(1)
        imagen_a_buscar_recibir = "otros/recibir.png"  # Reemplaza con la ruta de tu propia imagen
        recibir = buscar_imagen_en_pantalla(imagen_a_buscar_recibir)
        time.sleep(1)
        if recibir!= False and dungeon==1:
            click_raton_posicion (recibir[0], recibir[1])
            etapa=0
        imagen_a_buscar_dado = "otros/dado.png"  # Reemplaza con la ruta de tu propia imagen
        dado = buscar_imagen_en_pantalla(imagen_a_buscar_dado)
        time.sleep(1)
        if dado!= False and dungeon==1:
            click_raton_posicion (dado[0], dado[1])
            print('salir1')
            dungeon=0
            etapa=0
            terminar= False
            bosfinal=False
            final=0
            contardgok += 1
            terminando=0
            tiempo_inicio = time.time()
            time.sleep(5)
        # imagen_a_buscar_salir = "otros/salir.png"  # Reemplaza con la ruta de tu propia imagen
        # salir = buscar_imagen_en_pantalla(imagen_a_buscar_salir)
        # time.sleep(1)
        # if salir!= False and dungeon==1:
        #     print('salir1')
        #     click_raton_posicion (salir[0], salir[1])
        #     dungeon=0
        #     etapa=0
        #     terminar= False
        #     bosfinal=False
        #     final=0
        #     terminando=0
        #     tiempo_inicio = time.time()
        #     time.sleep(5)

def funcionetapa():
    global contardg
    global bosfinal
    global dungeon
    global terminar
    global contadormostruos1
    global vidamostruo
    global etapa
    global pase
    global final
    global nombre_proceso
    global tiempo_inicio
    global stop_flag
    global atacar
    global conteo
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionetapa en ejecución")
        time.sleep(1)
        if etapa>0 and dungeon==1 and final==0 and bosfinal==False and terminar== False: #and vidamostruo==False
            print('entre kong')
            centro_ventana2 = obtener_centro_ventana(nombre_proceso)
            if contadormostruos1>5:
                keyboard.press_and_release("space")
                time.sleep(0.2)

            if atacar==0:
                conteo=conteo+1
            else:
                conteo=0
            if conteo>10 and conteo<20 :
                keyboard.press_and_release("z")
                time.sleep(1.5)
                print('delante')
                keyboard.press_and_release("s")
                time.sleep(1.5)
            if conteo>20:
                keyboard.press_and_release("z")
                vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
                if vidamostruo:
                    atacar=1
                time.sleep(1.5)
                keyboard.press_and_release("w")
                print('atras')
                time.sleep(1.5)
            if etapa==1 and atacar==0:
                if pase==0:
                    # keyboard.press_and_release("f12")
                    # time.sleep(0.5)
                    # keyboard.press_and_release("f12")
                    # time.sleep(0.5)
                    imagen_a_buscar_piso0 = "b1f/piso0.png"  # Reemplaza con la ruta de tu propia imagen
                    piso0 = buscar_imagen_en_pantalla(imagen_a_buscar_piso0)
                    if piso0!=False :
                        raton_posicion (piso0[0]+70, piso0[1]+100)
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                    # time.sleep(0.5)
                    imagen_a_buscar_piso02 = "b1f/piso02.png"  # Reemplaza con la ruta de tu propia imagen
                    piso02 = buscar_imagen_en_pantalla(imagen_a_buscar_piso02)
                    if piso02!=False :
                        raton_posicion (piso02[0]+70, piso02[1]+100)
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                    # imagen_a_buscar_piso0_1 = "b1f/piso0_1.png"  # Reemplaza con la ruta de tu propia imagen
                    # piso0_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso0_1)
                    # if piso0_1!=False :
                    #     raton_posicion (piso0_1[0]-70, piso0_1[1]+100)
                    #     posicion_actual = pyautogui.position()
                    #     pyautogui.click(button='left')
                    #     time.sleep(2)
                    # imagen_a_buscar_piso0_4 = "b1f/piso0_4.png"  # Reemplaza con la ruta de tu propia imagen
                    # piso0_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso0_4)
                    # if piso0_4!=False :
                    #     raton_posicion (piso0_4[0]-50, piso0_4[1]+100)
                    #     posicion_actual = pyautogui.position()
                    #     pyautogui.click(button='left')
                    #     time.sleep(2)
                    imagen_a_buscar_piso0_2 = "b1f/piso0_2.png"  # Reemplaza con la ruta de tu propia imagen
                    piso0_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso0_2)
                    if piso0_2!=False :
                        raton_posicion (piso0_2[0], piso0_2[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        keyboard.press_and_release("z")
                        vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
                        if vidamostruo:
                            atacar=1
                        pase=1

                    # imagen_a_buscar_piso0_3 = "b1f/piso0_3.png"  # Reemplaza con la ruta de tu propia imagen
                    # piso0_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso0_3)
                    # if piso0_3!=False :
                    #     raton_posicion (piso0_3[0], piso0_3[1])
                    #     posicion_actual = pyautogui.position()
                    #     pyautogui.click(button='left')
                    #     pase=1
                    #     time.sleep(2)
                if pase==1 and not buscar_imagen_en_pantalla("otros/mostrous.jpg"):
                    atacar=0
                    print(f"El centro de la ventana2 de etapa 1 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    atacar=0
                    # keyboard.press("alt")
                    # time.sleep(0.5)
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
                    atacar=0
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(1.4)
                    keyboard.press_and_release(",")
                    time.sleep(1.4)
                    keyboard.press_and_release(",")
                    time.sleep(1)
                    atacar=0
                    raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release("z")
                    time.sleep(0.5)
                    atacar=0
                    bm2WI1 = buscar_imagen_en_pantalla("otros/bm2WI1.png")
                    bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
                    if bm2WI1 or not bm3WI1:
                        keyboard.press_and_release("2")
                        time.sleep(3)
                        print(f"El centro de la ventana2 de etapa 2 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                        posicion_actual = pyautogui.position()
                        time.sleep(0.5)
                        # keyboard.press("alt")
                        # time.sleep(0.5)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        # keyboard.release("alt")
                        # time.sleep(0.5)
                        keyboard.press_and_release("z")
                        etapa=3
                        atacar=1
                    if bm3WI1:
                        keyboard.press_and_release("6")
                        time.sleep(0.3)
                        keyboard.press_and_release("6")
                        time.sleep(0.3)
                        keyboard.press_and_release("6")
                        time.sleep(0.3)
                        keyboard.press_and_release("6")
                        time.sleep(0.3)
                        print(f"El centro de la ventana2 de etapa 2 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                        posicion_actual = pyautogui.position()
                        time.sleep(0.5)
                        # keyboard.press("alt")
                        # time.sleep(0.5)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.9)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        # keyboard.release("alt")
                        # time.sleep(0.5)
                        keyboard.press_and_release("z")
                        etapa=3
                        atacar=1
                    
            # if etapa==2 and atacar==0:
                
            if etapa==3 and atacar==0:
                imagen_a_buscar_bm2WI1 = "otros/bm2WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm2WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2WI1)

                imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                time.sleep(1)
                if bm3WI1!=False:
                    raton_posicion (bm3WI1[0], bm3WI1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
                    pyautogui.click(button='right')
                time.sleep(1)
                if bm2WI1!=False:
                    raton_posicion (bm2WI1[0], bm2WI1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
                    pyautogui.click(button='right')
                imagen_a_buscar_piso3_10 = "b1f/piso3_10.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_10 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_10)
                if piso3_10!=False :
                    raton_posicion (piso3_10[0]-(15)-100, piso3_10[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                pase=0
                if pase==0:
                    imagen_a_buscar_piso1_2 = "b1f/piso1_2.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_2)
                    if piso1_2!=False :
                        raton_posicion (piso1_2[0], piso1_2[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                    imagen_a_buscar_piso1_3 = "b1f/piso1_3.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_3)
                    if piso1_3!=False :
                        raton_posicion (piso1_3[0], piso1_3[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                    imagen_a_buscar_piso1 = "b1f/piso1.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1)
                    if piso1!=False :
                        raton_posicion (piso1[0], piso1[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        print(f"El centro de la ventana2 de etapa 3 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                        posicion_actual = pyautogui.position()
                        time.sleep(0.5)
                        # keyboard.press("alt")
                        # time.sleep(0.5)
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
                        # keyboard.release("alt")
                        # time.sleep(0.5)
                        pase=1
                    imagen_a_buscar_piso1_1 = "b1f/piso1_1.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_1)
                    if piso1_1!=False :
                        raton_posicion (piso1_1[0], piso1_1[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        print(f"El centro de la ventana2 de etapa 3 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                        posicion_actual = pyautogui.position()
                        time.sleep(0.5)
                        # keyboard.press("alt")
                        # time.sleep(0.5)
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
                        # keyboard.release("alt")
                        # time.sleep(0.5)
                        pase=1
                    imagen_a_buscar_piso1_4 = "b1f/piso1_4.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_4)
                    if piso1_4!=False :
                        raton_posicion (piso1_4[0], piso1_4[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        print(f"El centro de la ventana2 de etapa 3 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                        posicion_actual = pyautogui.position()
                        time.sleep(0.5)
                        # keyboard.press("alt")
                        # time.sleep(0.5)
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
                        # keyboard.release("alt")
                        # time.sleep(0.5)
                        pase=1
                    imagen_a_buscar_piso1_5 = "b1f/piso1_5.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_5)
                    if piso1_5!=False :
                        raton_posicion (piso1_5[0]-(15)-100, piso1_5[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        time.sleep(0.5)
                        pase=1
                    imagen_a_buscar_piso1_6 = "b1f/piso1_6.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_6 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_6)
                    if piso1_6!=False :
                        raton_posicion (piso1_6[0]-(15)-100, piso1_6[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        time.sleep(0.5)
                        pase=1
                    imagen_a_buscar_piso2 = "b1f/piso2.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2)
                    if piso2!=False :
                        raton_posicion (piso2[0], piso2[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0

                    imagen_a_buscar_piso2_1 = "b1f/piso2_1.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2_1)
                    if piso2_1!=False :
                        raton_posicion (piso2_1[0], piso2_1[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0

                    imagen_a_buscar_piso2_2 = "b1f/piso2_2.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2_2)
                    if piso2_2!=False :
                        raton_posicion (piso2_2[0], piso2_2[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0

                    imagen_a_buscar_piso2_4 = "b1f/piso2_4.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2_4)
                    if piso2_4!=False :
                        raton_posicion (piso2_4[0], piso2_4[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0
                    imagen_a_buscar_piso2_3 = "b1f/piso2_3.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2_3)
                    if piso2_3!=False :
                        raton_posicion (piso2_3[0], piso2_3[1]+150)
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0
                if pase==1:
                    imagen_a_buscar_piso1_2 = "b1f/piso1_2.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_2)
                    if piso1_2!=False :
                        raton_posicion (piso1_2[0], piso1_2[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                    imagen_a_buscar_piso1_3 = "b1f/piso1_3.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_3)
                    if piso1_3!=False :
                        raton_posicion (piso1_3[0], piso1_3[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                    imagen_a_buscar_piso1 = "b1f/piso1.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1)
                    if piso1!=False :
                        raton_posicion (piso1[0], piso1[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        print(f"El centro de la ventana2 de etapa 3 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                        posicion_actual = pyautogui.position()
                        time.sleep(0.5)
                        # keyboard.press("alt")
                        # time.sleep(0.5)
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
                        # keyboard.release("alt")
                        # time.sleep(0.5)
                        # pase=1
                    imagen_a_buscar_piso1_1 = "b1f/piso1_1.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_1)
                    if piso1_1!=False :
                        raton_posicion (piso1_1[0], piso1_1[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        print(f"El centro de la ventana2 de etapa 3 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                        posicion_actual = pyautogui.position()
                        time.sleep(0.5)
                        # keyboard.press("alt")
                        # time.sleep(0.5)
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
                        # keyboard.release("alt")
                        # time.sleep(0.5)
                        # pase=1
                    imagen_a_buscar_piso1_4 = "b1f/piso1_4.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_4)
                    if piso1_4!=False :
                        raton_posicion (piso1_4[0], piso1_4[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        print(f"El centro de la ventana2 de etapa 3 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                        posicion_actual = pyautogui.position()
                        time.sleep(0.5)
                        # keyboard.press("alt")
                        # time.sleep(0.5)
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
                        # keyboard.release("alt")
                        # time.sleep(0.5)
                        # pase=1
                    imagen_a_buscar_piso1_5 = "b1f/piso1_5.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_5)
                    if piso1_5!=False :
                        raton_posicion (piso1_5[0]-(15)-100, piso1_5[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        time.sleep(0.5)
                    imagen_a_buscar_piso1_6 = "b1f/piso1_6.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_6 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_6)
                    if piso1_6!=False :
                        raton_posicion (piso1_6[0]-(15)-100, piso1_6[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        time.sleep(0.5)
                    imagen_a_buscar_piso2 = "b1f/piso2.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2)
                    if piso2!=False :
                        raton_posicion (piso2[0], piso2[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0

                    imagen_a_buscar_piso2_1 = "b1f/piso2_1.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2_1)
                    if piso2_1!=False :
                        raton_posicion (piso2_1[0], piso2_1[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0

                    imagen_a_buscar_piso2_2 = "b1f/piso2_2.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2_2)
                    if piso2_2!=False :
                        raton_posicion (piso2_2[0], piso2_2[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0

                    imagen_a_buscar_piso2_4 = "b1f/piso2_4.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2_4)
                    if piso2_4!=False :
                        raton_posicion (piso2_4[0], piso2_4[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0
                    imagen_a_buscar_piso2_3 = "b1f/piso2_3.png"  # Reemplaza con la ruta de tu propia imagen
                    piso2_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso2_3)
                    if piso2_3!=False :
                        raton_posicion (piso2_3[0], piso2_3[1]+150)
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(1.5)
                        # keyboard.press_and_release("f11")
                        # time.sleep(2)
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        etapa=4
                        pase=0

            if etapa==4 and atacar==0:
                time.sleep(1.5)
                keyboard.press_and_release("ctrl+a")
                time.sleep(1)
                keyboard.press_and_release("ctrl+a")
                time.sleep(1)
                keyboard.press_and_release("ctrl+a")
                time.sleep(1)
                keyboard.press_and_release("ctrl+a")
                time.sleep(1)
                keyboard.press_and_release("ctrl+a")
                time.sleep(1)
                keyboard.press_and_release("ctrl+a")
                time.sleep(1)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=5
            if etapa==5 and atacar==0:
                imagen_a_buscar_piso7_8 = "b1f/piso7_8.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_8 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_8)
                if piso7_8!=False :
                    raton_posicion (piso7_8[0]+120, piso7_8[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                imagen_a_buscar_piso3 = "b1f/piso3.png"  # Reemplaza con la ruta de tu propia imagen
                piso3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3)
                if piso3!=False :
                    raton_posicion (piso3[0]+15, piso3[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    etapa=6
                    atacar=0
                    lanzabuff=0
                imagen_a_buscar_piso3_1 = "b1f/piso3_1.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_1)
                if piso3_1!=False :
                    raton_posicion (piso3_1[0]+5, piso3_1[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0
                    lanzabuff=0
                imagen_a_buscar_piso3_2 = "b1f/piso3_2.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_2)
                if piso3_2!=False :
                    raton_posicion (piso3_2[0]+5, piso3_2[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0
                    lanzabuff=0
                imagen_a_buscar_piso3_3 = "b1f/piso3_3.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_3)
                if piso3_3!=False :
                    raton_posicion (piso3_3[0]+5, piso3_3[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0
                    lanzabuff=0
                imagen_a_buscar_piso3_4 = "b1f/piso3_4.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_4)
                if piso3_4!=False :
                    raton_posicion (piso3_4[0]+5, piso3_4[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0
                    lanzabuff=0
                imagen_a_buscar_piso3_7 = "b1f/piso3_7.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_7 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_7)
                if piso3_7!=False :
                    raton_posicion (piso3_7[0]+5, piso3_7[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0
                    lanzabuff=0
                imagen_a_buscar_piso3_8 = "b1f/piso3_8.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_8 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_8)
                if piso3_8!=False :
                    raton_posicion (piso3_8[0]+5, piso3_8[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0
                    lanzabuff=0
                imagen_a_buscar_piso3_5 = "b1f/piso3_5.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_5)
                if piso3_5!=False :
                    raton_posicion (piso3_5[0]+5, piso3_5[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0
                    lanzabuff=0
                imagen_a_buscar_piso3_6 = "b1f/piso3_6.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_6 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_6)
                if piso3_6!=False :
                    raton_posicion (piso3_6[0]+5, piso3_6[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0
                    lanzabuff=0
            if etapa==6 and atacar==0 and contadormostruos1>0:
                if pase==0:
                    time.sleep(1.5)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25)-15, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
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
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    imagen_a_buscar_piso5 = "b1f/piso5.png"  # Reemplaza con la ruta de tu propia imagen
                    piso5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso5)
                    if piso5!=False :
                        raton_posicion (piso5[0], piso5[1])
                        posicion_actual = pyautogui.position()
                        etapa=7
                        pase=0
                        atacar=1
                        pase=1
                        contadormostruos1=0
                        keyboard.press_and_release("z")
                    else:
                        etapa=7
                        pase=0
                        atacar=1
                        pase=1
                        contadormostruos1=0
                        keyboard.press_and_release("z")
                if pase==1:
                    imagen_a_buscar_piso4 = "b1f/piso4.png"  # Reemplaza con la ruta de tu propia imagen
                    piso4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso4)
                    if piso4!=False :
                        raton_posicion (piso4[0], piso4[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(3)
                        time.sleep(0.5)
                        print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                        posicion_actual = pyautogui.position()
                        # keyboard.press("alt")
                        # time.sleep(0.5)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.5)
                        etapa=7
                        pase=0
                        atacar=1
                        keyboard.press_and_release("z")
                    imagen_a_buscar_piso4_1 = "b1f/piso4_1.png"  # Reemplaza con la ruta de tu propia imagen
                    piso4_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso4_1)
                    if piso4_1!=False :
                        raton_posicion (piso4_1[0], piso4_1[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(3)
                        time.sleep(0.5)
                        print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                        posicion_actual = pyautogui.position()
                        # keyboard.press("alt")
                        # time.sleep(0.5)
                        keyboard.press_and_release(".")
                        time.sleep(1)
                        keyboard.press_and_release(",")
                        time.sleep(0.5)
                        etapa=7
                        pase=0
                        atacar=1
                        keyboard.press_and_release("z")
            if etapa==7 and atacar==1:
                imagen_a_buscar_piso6_6 = "b1f/piso6_6.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_6 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_6)
                if piso6_6!=False :
                    raton_posicion (piso6_6[0], piso6_6[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso6_6{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0

            if etapa==7 and atacar==0 and contadormostruos1>0:
                imagen_a_buscar_piso6_1 = "b1f/piso6_1.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_1)
                if piso6_1!=False :
                    raton_posicion (piso6_1[0], piso6_1[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    keyboard.press_and_release("z")
                    atacar=1
                imagen_a_buscar_piso3_9 = "b1f/piso3_9.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_9 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_9)
                if piso3_9!=False :
                    raton_posicion (piso3_9[0], piso3_9[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    keyboard.press_and_release("z")
                    atacar=1
                imagen_a_buscar_piso6 = "b1f/piso6.png"  # Reemplaza con la ruta de tu propia imagen
                piso6 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6)
                if piso6!=False :
                    raton_posicion (piso6[0], piso6[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    keyboard.press_and_release("z")
                    atacar=1
                imagen_a_buscar_piso6_7 = "b1f/piso6_7.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_7 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_7)
                if piso6_7!=False :
                    raton_posicion (piso6_7[0], piso6_7[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    keyboard.press_and_release("z")
                    atacar=1
                imagen_a_buscar_piso6_2 = "b1f/piso6_2.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_2)
                if piso6_2!=False :
                    raton_posicion (piso6_2[0], piso6_2[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso6_2{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(",")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                imagen_a_buscar_piso6_3 = "b1f/piso6_3.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_3)
                if piso6_3!=False :
                    raton_posicion (piso6_3[0], piso6_3[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso6_3{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(",")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso6_4 = "b1f/piso6_4.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_4)
                if piso6_4!=False :
                    raton_posicion (piso6_4[0], piso6_4[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    print(f"El centro de la ventana2 de etapa 4 piso6_4{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(",")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso6_ = "b1f/piso6_.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_ = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_)
                if piso6_!=False :
                    raton_posicion (piso6_[0], piso6_[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso6_{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso6_5 = "b1f/piso6_5.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_5)
                if piso6_5!=False :
                    raton_posicion (piso6_5[0], piso6_5[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    atacar=1
                imagen_a_buscar_piso7 = "b1f/piso7.png"  # Reemplaza con la ruta de tu propia imagen
                piso7 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7)
                if piso7!=False :
                    raton_posicion (piso7[0]-(15)-100, piso7[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso7{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso6_6 = "b1f/piso6_6.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_6 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_6)
                if piso6_6!=False :
                    raton_posicion (piso6_6[0], piso6_6[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso7{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso7_1 = "b1f/piso7_1.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_1)
                if piso7_1!=False :
                    raton_posicion (piso7_1[0]-(15)-100, piso7_1[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso7_1{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso7_2 = "b1f/piso7_2.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_2)
                if piso7_2!=False :
                    raton_posicion (piso7_2[0]-80, piso7_2[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso7_2{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]-20, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso7_3 = "b1f/piso7_3.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_3)
                if piso7_3!=False :
                    raton_posicion (piso7_3[0]-80, piso7_3[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso7_3{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]-20, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso7_4 = "b1f/piso7_4.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_4)
                if piso7_4!=False :
                    raton_posicion (piso7_4[0]+120, piso7_4[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    print(f"El centro de la ventana2 de etapa 4 piso7_4{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25)+5, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1.5)
                    keyboard.press_and_release(".")
                    time.sleep(1.5)
                    keyboard.press_and_release(",")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso7_5 = "b1f/piso7_5.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_5)
                if piso7_5!=False :
                    raton_posicion (piso7_5[0]+120, piso7_5[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    print(f"El centro de la ventana2 de etapa 4 piso7_5{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25)+5, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1.5)
                    keyboard.press_and_release(".")
                    time.sleep(1.5)
                    keyboard.press_and_release(",")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso7_7 = "b1f/piso7_7.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_7 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_7)
                if piso7_7!=False :
                    raton_posicion (piso7_7[0], piso7_7[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                imagen_a_buscar_piso7_6 = "b1f/piso7_6.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_6 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_6)
                if piso7_6!=False :
                    raton_posicion (piso7_6[0]+120, piso7_6[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    print(f"El centro de la ventana2 de etapa 4 piso7_6{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25)+5, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1.5)
                    keyboard.press_and_release(".")
                    time.sleep(1.5)
                    keyboard.press_and_release(",")
                    time.sleep(1)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso5 = "b1f/piso5.png"  # Reemplaza con la ruta de tu propia imagen
                piso5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso5)
                if piso5!=False :
                    raton_posicion (piso5[0]+100, piso5[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso5{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                imagen_a_buscar_piso5_1 = "b1f/piso5_1.png"  # Reemplaza con la ruta de tu propia imagen
                piso5_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso5_1)
                if piso5_1!=False :
                    raton_posicion (piso5_1[0]+100, piso5_1[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 piso5_1{nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+(25), centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release("z")
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    
                    # etapa=6
                    atacar=0
                    lanzabuff=0
                    keyboard.press_and_release("z")
                
                imagen_a_buscar_portal1 = "b1f/portal1.png"  # Reemplaza con la ruta de tu propia imagen
                portal1 = buscar_imagen_en_pantalla(imagen_a_buscar_portal1)
                if portal1!=False :
                    raton_posicion (portal1[0], portal1[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                imagen_a_buscar_portal2 = "b1f/portal2.png"  # Reemplaza con la ruta de tu propia imagen
                portal2 = buscar_imagen_en_pantalla(imagen_a_buscar_portal2)
                if portal2!=False :
                    raton_posicion (portal2[0], portal2[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                imagen_a_buscar_portal3 = "b1f/portal3.png"  # Reemplaza con la ruta de tu propia imagen
                portal3 = buscar_imagen_en_pantalla(imagen_a_buscar_portal3)
                if portal3!=False :
                    raton_posicion (portal3[0], portal3[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                imagen_a_buscar_portal = "b1f/npc.png"  # Reemplaza con la ruta de tu propia imagen
                portal = buscar_imagen_en_pantalla(imagen_a_buscar_portal)
                if portal!=False :
                    keyboard.press_and_release("space")
                    time.sleep(1.5)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+40)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    # keyboard.press("alt")
                    # time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    # keyboard.release("alt")
                    # time.sleep(0.5)
                    time.sleep(0.5)
                    keyboard.press_and_release("z")
                    atacar=1
                    etapa=9

        if etapa==9 and atacar==0:
            imagen_a_buscar_portal1 = "b1f/portal1.png"  # Reemplaza con la ruta de tu propia imagen
            portal1 = buscar_imagen_en_pantalla(imagen_a_buscar_portal1)
            if portal1!=False :
                raton_posicion (portal1[0], portal1[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(0.5)
            imagen_a_buscar_portal2 = "b1f/portal2.png"  # Reemplaza con la ruta de tu propia imagen
            portal2 = buscar_imagen_en_pantalla(imagen_a_buscar_portal2)
            if portal2!=False :
                raton_posicion (portal2[0], portal2[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(0.5)
            imagen_a_buscar_portal3 = "b1f/portal3.png"  # Reemplaza con la ruta de tu propia imagen
            portal3 = buscar_imagen_en_pantalla(imagen_a_buscar_portal3)
            if portal3!=False :
                raton_posicion (portal3[0], portal3[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(0.5)
            imagen_a_buscar_portal = "b1f/npc.png"  # Reemplaza con la ruta de tu propia imagen
            portal = buscar_imagen_en_pantalla(imagen_a_buscar_portal)
            if portal!=False :
                keyboard.press_and_release("space")
                time.sleep(1.5)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=9
            imagen_a_buscar_piso9_9 = "b1f/piso9_9.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_9 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_9)
            if piso9_9!=False and atacar==0:
                raton_posicion (piso9_9[0], piso9_9[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(3)
            imagen_a_buscar_piso9_1 = "b1f/piso9_1.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_1)
            if piso9_1!=False and atacar==0:
                raton_posicion (piso9_1[0], piso9_1[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9 = "b1f/piso9.png"  # Reemplaza con la ruta de tu propia imagen
            piso9 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9)
            if piso9!=False and atacar==0:
                raton_posicion (piso9[0], piso9[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_2 = "b1f/piso9_2.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_2)
            if piso9_2!=False and atacar==0:
                raton_posicion (piso9_2[0], piso9_2[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_3 = "b1f/piso9_3.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_3)
            if piso9_3!=False and atacar==0:
                raton_posicion (piso9_3[0], piso9_3[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_4 = "b1f/piso9_4.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_4)
            if piso9_4!=False and atacar==0:
                raton_posicion (piso9_4[0], piso9_4[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_8 = "b1f/piso9_8.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_8 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_8)
            if piso9_8!=False and atacar==0:
                raton_posicion (piso9_8[0], piso9_8[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_10 = "b1f/piso9_10.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_10 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_10)
            if piso9_10!=False and atacar==0:
                raton_posicion (piso9_10[0], piso9_10[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_5 = "b1f/piso9_5.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_5)
            if piso9_5!=False and atacar==0:
                raton_posicion (piso9_5[0], piso9_5[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_6 = "b1f/piso9_6.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_6 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_6)
            if piso9_6!=False and atacar==0:
                raton_posicion (piso9_6[0], piso9_6[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_11 = "b1f/piso9_11.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_11 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_11)
            if piso9_11!=False and atacar==0:
                raton_posicion (piso9_11[0], piso9_11[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_12 = "b1f/piso9_12.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_12 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_12)
            if piso9_12!=False and atacar==0:
                raton_posicion (piso9_12[0], piso9_12[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso9_7 = "b1f/piso9_7.png"  # Reemplaza con la ruta de tu propia imagen
            piso9_7 = buscar_imagen_en_pantalla(imagen_a_buscar_piso9_7)
            if piso9_7!=False and atacar==0:
                raton_posicion (piso9_7[0], piso9_7[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
            imagen_a_buscar_piso10 = "b1f/piso10.png"  # Reemplaza con la ruta de tu propia imagen
            piso10 = buscar_imagen_en_pantalla(imagen_a_buscar_piso10)
            if piso10!=False and atacar==0:
                raton_posicion (piso10[0], piso10[1])
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(2)
                print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+40)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                # keyboard.press("alt")
                # time.sleep(0.5)
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
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
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
                keyboard.press_and_release("2")
                time.sleep(3)
                # keyboard.press("alt")
                # time.sleep(0.5)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                keyboard.press_and_release(".")
                time.sleep(1)
                keyboard.press_and_release(",")
                time.sleep(0.9)
                # keyboard.release("alt")
                # time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
        if etapa==10 and atacar==0:
            print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
            raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+40)
            posicion_actual = pyautogui.position()
            time.sleep(0.5)
            # keyboard.press("alt")
            # time.sleep(0.5)
            keyboard.press_and_release(".")
            time.sleep(1)
            keyboard.press_and_release(",")
            time.sleep(0.9)
            # keyboard.release("alt")
            # time.sleep(0.5)
            time.sleep(0.5)
            vidamostruo = buscar_imagen_en_pantalla("otros/mostrous.jpg")
            if vidamostruo:
                atacar=1
            else:
                keyboard.press_and_release("z")
                if contadormostruos1>=10:
                    atacar=0
                
        if etapa>=10:
            keyboard.press_and_release("space")
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
# Configurar la función de detección del evento de Escape

# Inicializar la variable de parada
stop_flag = False
contardg=0
contadormostruos1=0
dungeon=0
etapa=0
contardgok=0
contarsp=0
terminar=False
vidamostruo=False
bm3WI1=False
bosfinal=False
conteocabal=0
terminando=0
final=0
atacar=0
pase=0
lanzabuff=0
conteo=0
nombre_proceso = "cabal"
tiempo_inicio = time.time()
# Crear un ThreadPoolExecutor con, por ejemplo, 2 hilos

funciones = [
    funcionSP,
    funciologin,
    # funcionvida,
    funcionmostruo,
    funcionBM,
    funcionBM3,
    funcionBM2,
    funcionfail,
    funcionmuerte,
    funcioiniciar,
    funcionterminar,
    funcionetapa,
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