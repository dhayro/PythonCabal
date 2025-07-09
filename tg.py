import concurrent.futures
import pyautogui
import pygetwindow as gw
import time

import keyboard
import threading

from pynput.mouse import Button, Controller
import time
from screen_search import Search

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
contardg=contadormostruos1= atacar= etapa=contardgok=wavecuenta=esperandocuenta=bosscuenta=entrartg=dungeon=conteocabal=0
piso=""

def crear_ventana_info():
    global contardg, atacar,tipotg, etapa, contardgok, piso, contadormostruos1, wavecuenta, esperandocuenta, bosscuenta, entrartg, dungeon, conteocabal
    ventana = tk.Tk()
    ventana.title("Información en tiempo real")
    ventana.geometry("300x350")  # Increased height to accommodate new labels

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

    etiqueta_tipotg = ttk.Label(ventana, text="Cuenta Wave: ")
    etiqueta_tipotg.pack()

    etiqueta_esperandocuenta = ttk.Label(ventana, text="Esperando Cuenta: ")
    etiqueta_esperandocuenta.pack()

    etiqueta_cuentaboss = ttk.Label(ventana, text="Cuenta Boss: ")
    etiqueta_cuentaboss.pack()

    # Add new labels for entrartg, dungeon, and conteocabal
    etiqueta_entrartg = ttk.Label(ventana, text="Entrar TG: ")
    etiqueta_entrartg.pack()

    etiqueta_dungeon = ttk.Label(ventana, text="Dungeon: ")
    etiqueta_dungeon.pack()

    etiqueta_conteocabal = ttk.Label(ventana, text="Conteo Cabal: ")
    etiqueta_conteocabal.pack()

    def actualizar_info():
        global contardg, atacar,tipotg, etapa, contardgok, piso, contadormostruos1, wavecuenta, esperandocuenta, bosscuenta, entrartg, dungeon, conteocabal
        etiqueta_dg.config(text=f"DG : {contardg}")
        etiqueta_dgok.config(text=f"DG ok: {contardgok}")
        etiqueta_atacar.config(text=f"Atacar: {atacar}")
        etiqueta_mostruos.config(text=f"Mostruos: {contadormostruos1}")
        etiqueta_piso.config(text=f"Piso: {piso}")
        etiqueta_etapa.config(text=f"Etapa inicial: {etapa}")
        etiqueta_tipotg.config(text=f"tipotg: {tipotg}")
        etiqueta_esperandocuenta.config(text=f"Esperando Cuenta: {esperandocuenta}")
        etiqueta_cuentaboss.config(text=f"Cuenta Boss: {bosscuenta}")
        # Update new labels
        etiqueta_entrartg.config(text=f"Entrar TG: {entrartg}")
        etiqueta_dungeon.config(text=f"Dungeon: {dungeon}")
        etiqueta_conteocabal.config(text=f"Conteo Cabal: {conteocabal}")
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
    # time.sleep(3)
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

# def buscar_imagen_en_pantalla(imagen_path, confianza=0.9):
#     # Cargar la imagen a buscar
#     imagen = cv2.imread(imagen_path)
#     imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

#     try:
#         # Capturar la pantalla
#         captura_pantalla = pyautogui.screenshot()

#         # Convertir la captura de pantalla a una imagen OpenCV
#         captura_pantalla_np = np.array(captura_pantalla)
#         captura_pantalla_cv = cv2.cvtColor(captura_pantalla_np, cv2.COLOR_RGB2BGR)
#         captura_pantalla_gris = cv2.cvtColor(captura_pantalla_cv, cv2.COLOR_BGR2GRAY)

#         # Buscar la imagen en la captura de pantalla
#         coincidencias = cv2.matchTemplate(captura_pantalla_gris, imagen_gris, cv2.TM_CCOEFF_NORMED)
#         loc = np.where(coincidencias >= confianza)

#         # Obtener el color del borde de la imagen
#         borde_color = imagen[0, 0].tolist()  # Color del píxel en la esquina superior izquierda

#         # Dibujar un rectángulo alrededor de las coincidencias con el color del borde de la imagen original
#         for pt in zip(*loc[::-1]):
#             cv2.rectangle(captura_pantalla_cv, pt,
#                           (pt[0] + imagen.shape[1], pt[1] + imagen.shape[0]),
#                           borde_color, 2)

#         # Mostrar la captura de pantalla con los rectángulos de coincidencia
#         # cv2.imshow('Captura de pantalla', captura_pantalla_cv)
#         # cv2.waitKey(0)

#         if len(loc[0]) > 0:
#             x = loc[1][0]
#             y = loc[0][0]

#             # Obtener las dimensiones de la imagen
#             ancho, alto = imagen_gris.shape[::-1]

#             # Calcular el centro de la coincidencia
#             centro_x = x + ancho // 2
#             centro_y = y + alto // 2

#             return centro_x, centro_y
#         else:
#             return False

#     except Exception as e:
#         return False

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

def buscar_imagenes():
    imagenes = {
        'esperandotg4': "tg/esperandotg4.png",
        'marcafin': "otros/marcafin.png",
        'salix': "otros/confirmasalir.png",
        'bandera': "tg/bandera.png"
    }
    return {nombre: buscar_imagen_en_pantalla(ruta) for nombre, ruta in imagenes.items()}

def actualizar_estados(resultados):
    global dungeon, atacar, lanzabuff, entrartg, etapa

    if resultados['bandera']:
        if resultados['salix']  and not resultados['marcafin'] and not resultados['esperandotg4']: #and dungeon != 2
            dungeon, atacar, lanzabuff, entrartg = 1, 1, 1, 2
            print("entrekong1")
        elif not resultados['salix']  and not resultados['marcafin'] and resultados['esperandotg4']: #and dungeon != 2
            dungeon, entrartg, etapa = 0, 1, 0
            print("entrekong2")
        elif not resultados['marcafin'] and not resultados['salix'] and not resultados['esperandotg4']:
            entrartg, dungeon, etapa = 1, 2, 0
            print("entrekong3")
    elif not resultados['bandera'] and not resultados['marcafin'] and  resultados['salix'] and not resultados['esperandotg4']:
        entrartg, dungeon, atacar, etapa = 0, 0, 0, 0
        print("entrekong4")

    return dungeon, atacar, lanzabuff, entrartg, etapa
def funcionSP():
    global etapa
    global contardg
    global lanzabuff
    global stop_flag
    global dungeon
    global atacar
    global entrartg
    while not stop_flag and not keyboard.is_pressed('delete'):
        if entrartg == 0 :
            time.sleep(0.5)
            continue
        print("funcionSP en ejecución")
        time.sleep(1)
        imagen_a_buscar_bufsp = "otros/bufsp.png"  # Reemplaza con la ruta de tu propia imagen
        bufsp = buscar_imagen_en_pantalla(imagen_a_buscar_bufsp)
        if bufsp!=False and lanzabuff==1 :
            keyboard.press_and_release("f8")
            time.sleep(1)
        sp = imagenSP()
        if sp!= False:
            imagen_capturada = capturar_pantalla(sp[0], sp[1], 62, 10)

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
        print('atacar: ',atacar)
        print('etapa inicial: ',etapa)
        print('dungeon: ',dungeon)
        if len(ctns)<=5 and dungeon==1:
            keyboard.press_and_release("ctrl+5")

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

def imagenmostruo():
    search = buscar_imagen_en_pantalla("otros/tgmostrous.png")
    if search== False:
        if path.exists('captura/captura_pantalla_mostruo.png'):
            remove("captura/captura_pantalla_mostruo.png")
        return False
    else:
        imagen_capturada = capturar_pantalla_mostruo(int(search[0])-4, int(search[1])-7, 270, 15)
        image = cv2.imread('captura/captura_pantalla_mostruo.png', cv2.IMREAD_GRAYSCALE)

        # Establecer umbrales para identificar la parte llena de la barra
        # Puedes ajustar estos valores según tus necesidades
        _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

        # Calcular la cantidad de píxeles blancos (llenados) y la cantidad total de píxeles
        pixels_filled = np.sum(thresh == 255)
        total_pixels = thresh.size

        # Calcular el porcentaje de llenado
        return (pixels_filled / total_pixels) * 100
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

    global contadormostruos1
    global stop_flag
    global bosfinal
    global dungeon
    global etapa
    global terminar
    global vidamostruo
    global terminando
    global final
    global atacar
    global tipotg
    global lanzabuff
    global entrartg
    while not stop_flag and not keyboard.is_pressed('delete'):
        if entrartg == 0 :
            time.sleep(0.5)
            continue
        imagen_a_buscar_vidamostruo = "otros/tgmostrous.png"  # Reemplaza con la ruta de tu propia imagen
        vidamostruo = buscar_imagen_en_pantalla(imagen_a_buscar_vidamostruo)
        imagen_a_buscar_combo = "otros/combo1.png"  # Reemplaza con la ruta de tu propia imagen
        combo = buscar_imagen_en_pantalla(imagen_a_buscar_combo)
        imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
        bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
        imagen_a_buscar_jeisson = "tg/jeisson.png"  # Reemplaza con la ruta de tu propia imagen
        jeisson = buscar_imagen_en_pantalla(imagen_a_buscar_jeisson)
        if dungeon==1 and atacar==1 :
            print("funcionmostruo en ejecución")
            time.sleep(0.5)
            if vidamostruo!= False and (combo!=False or bm3WI1!=False) and jeisson==False:
                print("entrekong")
                contadormostruos1=0

                atacar=1
                etapa=0
                lanzabuff=1

                # etapa=0
                print('variable atacar')
                # if vidamostruo <=25:
                #     keyboard.press_and_release("z")
            else:
                keyboard.press_and_release("z")
                contadormostruos1=contadormostruos1+1
                if contadormostruos1>=3 and dungeon==1:
                    atacar=0
                    etapa_mapping = {
                        'TG': 3,
                        'IP': 2,
                        'MC': 4
                    }
                    if buscar_imagen_en_pantalla("tg/marcafin.png"):
                        etapa = 0
                    else:
                        etapa = etapa_mapping.get(tipotg, etapa)  # Default to current etapa if tipotg not found
                    lanzabuff=0
            # if bosfinal!=False:
            #     etapa=0
            #     final=1
        if dungeon==1 and atacar==0:
            print("funcionmostruo en ejecución")
            time.sleep(0.5)

            if vidamostruo!= False and (combo!=False or bm3WI1!=False) and jeisson==False:
                atacar=1
                etapa=0
                lanzabuff=1
            else:
                keyboard.press_and_release("z")
                contadormostruos1=contadormostruos1+1
                if contadormostruos1>=4 and dungeon==1:
                    atacar=0
                    etapa_mapping = {
                        'TG': 3,
                        'IP': 2,
                        'MC': 4
                    }
                    if buscar_imagen_en_pantalla("tg/marcafin.png"):
                        etapa = 0
                    else:
                        etapa = etapa_mapping.get(tipotg, etapa)  # Default to current etapa if tipotg not found
                    lanzabuff=0
            # atacar=1


    print("funcionmostruo terminada")


def funcionBM():
    global stop_flag, bm3WI1, bm2WI1, vidamostruo, dungeon, tiempo_transcurrido, tiempo_inicio,atacar,entrartg

    imagen_presente = False
    
    while not stop_flag and not keyboard.is_pressed('delete'):
        if entrartg == 0 :
            time.sleep(0.5)
            continue
        if dungeon != 1 or atacar != 1:
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
    global stop_flag, bm3WI1, dungeon, nombre_proceso, vidamostruo, atacar,entrartg

    while not stop_flag and not keyboard.is_pressed('delete'):
        if entrartg == 0 :
            time.sleep(0.5)
            continue
        print("funcionBM2 en ejecución")
        time.sleep(0.3)  # Reduced sleep time

        
        if  not (dungeon == 1 and atacar == 1 ):
            continue

        bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
        if  bm3WI1:
            continue

     
        # if not buscar_imagen_en_pantalla("otros/tgmostrous.jpg"):
        #     continue

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
                time.sleep(0.5)
            
            # if buscar_imagen_en_pantalla("otros/bm3WI1.png") or not buscar_imagen_en_pantalla("otros/tgmostrous.jpg"):
            #     keyboard.press_and_release("space")
            #     time.sleep(0.2)
            #     break

    print("funcionBM2 terminada")


def funcionBM3():
    global stop_flag, bm3WI1, dungeon, vidamostruo, atacar,entrartg

    while not stop_flag and not keyboard.is_pressed('delete'):
        if entrartg == 0 :
            time.sleep(0.5)
            continue
        print("funcionBM3 en ejecución")
        time.sleep(0.5)  # Reducido de 1 a 0.5 segundos

        if not (vidamostruo and dungeon == 1 and atacar == 1)  and not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
            continue

        bm3WI1 = buscar_imagen_en_pantalla("otros/bm3WI1.png")
        if not bm3WI1:
            continue

        ataque_count = 0
        max_ataques = 15  # Límite de ataques antes de verificar condiciones nuevamente

        while ataque_count < max_ataques:
            # if buscar_imagen_en_pantalla("login/cabal.png"):
            #     break

            print('ataque BM3 con monstruos')
            keyboard.press_and_release("6")
            keyboard.press_and_release("space")
            time.sleep(0.1)  # Reducido de 0.3 a 0.2 segundos

            if not buscar_imagen_en_pantalla("otros/bm3WI1.png"):
                break

            # vidamostruo = buscar_imagen_en_pantalla("otros/tgmostrous.jpg")
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


def funcionmuerte():

    global dungeon
    global nombre_proceso
    global tiempo_inicio
    global etapa
    global final
    global terminar
    global positivo
    global muriendo
    global tipotg
    global stop_flag
    global entrartg
    while not stop_flag and not keyboard.is_pressed('delete'):
        if entrartg == 0 :
            time.sleep(0.5)
            continue
        print("funcionmuerte en ejecución")
        time.sleep(1)
        imagen_a_buscar_muerte = "otros/wrap-dead.bmp"  # Reemplaza con la ruta de tu propia imagen
        muerte = buscar_imagen_en_pantalla(imagen_a_buscar_muerte)

        if muerte!=False:
            print('muerte')
            muriendo=1
            click_raton_posicion (muerte[0], muerte[1])
            imagen_a_buscar_confirmar_muerte = "otros/confirmar_muerte.png"  # Reemplaza con la ruta de tu propia imagen
            confirmar_muerte = buscar_imagen_en_pantalla(imagen_a_buscar_confirmar_muerte)
            if confirmar_muerte!=False:
                print('confirmar_muerte')
                click_raton_posicion (confirmar_muerte[0], confirmar_muerte[1])
                lanzabuff=0
                time.sleep(1.5)
                muriendo=0

        imagen_a_buscar_portalprocyon4 = "tg/portalprocyon5.png"  # Reemplaza con la ruta de tu propia imagen
        portalprocyon4 = buscar_imagen_en_pantalla(imagen_a_buscar_portalprocyon4)
        if portalprocyon4!=False:
            click_raton_posicion (portalprocyon4[0]+95*(positivo), portalprocyon4[1]-75)
            time.sleep(5)
            etapa_mapping = {
                'TG': 3,
                'IP': 2,
                'MC': 4
            }
            if buscar_imagen_en_pantalla("tg/marcafin.png"):
                etapa = 0
            else:
                etapa = etapa_mapping.get(tipotg, etapa)  # Default to current etapa if tipotg not found
            muriendo=0
        else:
            imagen_a_buscar_portalprocyon = "tg/portalprocyon.png"  # Reemplaza con la ruta de tu propia imagen
            portalprocyon = buscar_imagen_en_pantalla(imagen_a_buscar_portalprocyon)
            if portalprocyon!=False:
                click_raton_posicion (portalprocyon[0], portalprocyon[1])
                time.sleep(5)
                etapa_mapping = {
                    'TG': 3,
                    'IP': 2,
                    'MC': 4
                }
                if buscar_imagen_en_pantalla("tg/marcafin.png"):
                    etapa = 0
                else:
                    etapa = etapa_mapping.get(tipotg, etapa)  # Default to current etapa if tipotg not found
                muriendo=0
        if tipotg != 'IP':
            imagen_a_buscar_portalprocyon6 = "tg/portalprocyon6.png"  # Reemplaza con la ruta de tu propia imagen
            portalprocyon6 = buscar_imagen_en_pantalla(imagen_a_buscar_portalprocyon6)
            if portalprocyon6!=False:
                click_raton_posicion (portalprocyon6[0], portalprocyon6[1])
                time.sleep(5)
                etapa_mapping = {
                    'TG': 3,
                    'IP': 2,
                    'MC': 4
                }
                if buscar_imagen_en_pantalla("tg/marcafin.png"):
                    etapa = 0
                else:
                    etapa = etapa_mapping.get(tipotg, etapa)  # Default to current etapa if tipotg not found
                muriendo=0


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
def funciologin():
    global stop_flag, contardg, dungeon, terminar, nombre_proceso, tiempo_inicio, bosfinal, conteocabal
    global entrartg, terminando, contadormostruos1, vidamostruo, bm3WI1, final, atacar, pase, lanzabuff, conteo, etapa

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funciologin en ejecución")
        time.sleep(1)

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
            'chwaron': "tg/chwaron.png",
            'channel': "login/channel/8.bmp",
            'character_list': "login/character-list.bmp",
            'sub_pass': "login/sub-pass.bmp",
            'ok': "login/ok.png",
            'duallogin': "login/duallogin.png",
            'tyes': "login/tyes.png"
        }

        # Agregar números para el login
        for i in range(10):
            imagenes[f'pass{i}'] = f"login/number/{i}.bmp"

        # Buscar todas las imágenes y guardar los resultados
        resultados = {nombre: buscar_imagen_en_pantalla(ruta) for nombre, ruta in imagenes.items()}

        if resultados['failconect'] or resultados['failconectserver']:
            click_offset = resultados['failconect'] or resultados['failconectserver']
            click_raton_posicion(click_offset[0], click_offset[1] + 135)
            time.sleep(1.5)

        if resultados['cabal']:
            conteocabal = 1
            stop_flag = False
            contardg = contadormostruos1 = dungeon = entrartg = etapa = 0
            terminar = vidamostruo = bm3WI1 = bosfinal = terminando = final = atacar = pase = lanzabuff = conteo = False
            print("conteocabal")

        if conteocabal == 1:
            if resultados['endsesion']:
                click_raton_posicion(resultados['endsesion'][0] + 90, resultados['endsesion'][1])

            if resultados['error'] and resultados['okerror']:
                click_raton_posicion(resultados['okerror'][0], resultados['okerror'][1])

            if resultados['disconected'] or resultados['failconect']:
                click_pos = resultados['disconected'] or resultados['failconect']
                click_raton_posicion(click_pos[0], click_pos[1] + 135)
                dungeon = etapa = 0

            if not resultados['caballogin'] and resultados['account_login']:
                click_raton_posicion(resultados['account_login'][0], resultados['account_login'][1] + 50)
                for _ in range(15):
                    keyboard.press_and_release("backspace")
                keyboard.write("dhayro")

                if resultados['account_login'] and not resultados['disconected'] and not resultados['failconect']:
                    click_raton_posicion(resultados['account_login'][0], resultados['account_login'][1] + 90)
                    keyboard.write("Dhakongto2710")
                    keyboard.press_and_release("enter")
                    time.sleep(1)
                    if resultados['duallogin'] and resultados['tyes']:
                        click_raton_posicion(resultados['tyes'][0], resultados['tyes'][1])
                        time.sleep(10)

            if resultados['server_select']:
                if resultados['chwaron']:
                    click_raton_posicion(resultados['chwaron'][0], resultados['chwaron'][1])
                elif resultados['channel']:
                    click_raton_posicion(resultados['channel'][0], resultados['channel'][1])
                pyautogui.click(clicks=2, interval=0.1)
                time.sleep(0.5)

            if resultados['character_list']:
                if resultados['sub_pass']:
                    password = [1, 0, 0, 5, 9, 3]
                    for digit in password:
                        click_raton_posicion(resultados[f'pass{digit}'][0], resultados[f'pass{digit}'][1])
                    click_raton_posicion(resultados['ok'][0], resultados['ok'][1])
                else:
                    keyboard.press_and_release("enter")



    print("funciologin terminada")

def click_imagen(imagen, offset_x=0, offset_y=0, button='left', clicks=1):
    raton_posicion(imagen[0] + offset_x, imagen[1] + offset_y)
    time.sleep(0.5)
    pyautogui.click(button=button, clicks=clicks)


def funcionentrartg():
    global  positivo
    global stop_flag
    global entrartg
    
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcioiniciar en ejecución")
        capella = buscar_imagen_en_pantalla("otros/capella.bmp")
        procyon = buscar_imagen_en_pantalla("otros/procyon.bmp")

        if capella:
            positivo = -1
            click_raton_posicion(capella[0]+230, capella[1]+13)
            print('clic tg')
            time.sleep(0.1)
            keyboard.press_and_release("enter")
            entrartg = 1
        elif procyon:
            positivo = 1
            click_raton_posicion(procyon[0]+230, procyon[1]+13)
            print('clic tg')
            time.sleep(0.1)
            keyboard.press_and_release("enter")
            entrartg = 1
        chwar1 = buscar_imagen_en_pantalla("tg/chwar1.png")
        if chwar1 and not buscar_imagen_en_pantalla("tg/yesi.png"):
            print('clic chwar1')
            click_raton_posicion(chwar1[0], chwar1[1])
            pyautogui.click(clicks=2, interval=0.1)
            yessi=buscar_imagen_en_pantalla("tg/yesi.png")
            if yessi:
                click_raton_posicion(yessi[0], yessi[1])
        yessi=buscar_imagen_en_pantalla("tg/yesi.png")
        if yessi:
            click_raton_posicion(yessi[0], yessi[1])

def funcioiniciar():
    global contardg, dungeon, terminar, nombre_proceso, tiempo_inicio, bosfinal, positivo, final
    global terminando, stop_flag,tipotg
    global atacar, conteocabal, etapa, entrartg, lanzabuff
    global permiso

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcioiniciar en ejecución")
        time.sleep(1)
        if entrartg == 0 :
            time.sleep(0.5)
            continue
    
        comentarios = buscar_imagen_en_pantalla("otros/comentarios.png")
        if comentarios and not buscar_imagen_en_pantalla("otros/selectdg.png"):
            click_imagen(comentarios, offset_y=-10)
            poder = buscar_imagen_en_pantalla("login/poder.png")
            if poder:
                click_imagen(poder)
                keyboard.press_and_release("F1")

        cerrarmen = buscar_imagen_en_pantalla("otros/cerrarmen.png")
        if cerrarmen and entrartg == 1 and not buscar_imagen_en_pantalla("otros/selectdg.png"):
            while not buscar_imagen_en_pantalla("login/cabal.png"):
                click_imagen(cerrarmen)
                cerrarmen = buscar_imagen_en_pantalla("otros/cerrarmen.png")
                if not cerrarmen:
                    break

        mision = buscar_imagen_en_pantalla("tg/mision.png")
        if mision:
            keyboard.press_and_release("esc")

        bloquearok2 = buscar_imagen_en_pantalla("tg/bloquearok2.png")
        if bloquearok2:
            keyboard.press_and_release("esc")

        if buscar_imagen_en_pantalla("tg/esperandotg1.png"):
            tipotg = "IP"
        elif buscar_imagen_en_pantalla("tg/esperandotg2.png"):
            tipotg = "TG"
        elif buscar_imagen_en_pantalla("tg/esperandotg3.png"):
            tipotg = "MC"

        esperando_images = [ "tg/esperandotg4.png"]
        esperando = all(not buscar_imagen_en_pantalla(img) for img in esperando_images)

        if esperando and entrartg == 1 and dungeon != 2:
            entrartg, dungeon, conteocabal, etapa = 2, 1, 0, 1

        # if dungeon == 0 and not terminar and entrartg != 1:
        #     centro_ventana = obtener_centro_ventana(nombre_proceso)
        #     if centro_ventana:
        #         dungeon, etapa, terminar, bosfinal = 0, 0, False, False
        #         terminando, final = 0, 0
        #         tiempo_inicio = time.time()

                
        #             # time.sleep(25)

        #         # if procyon or capella:
        #         #     noty = buscar_imagen_en_pantalla("otros/noty.png")
        #         #     if noty:
                        
        #     else:
        #         print(f"El programa {nombre_proceso} no está abierto o no se pudo obtener la información de la ventana.")

    print("funcioiniciar terminada")

def mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y, duracion_clic=1):
    global nombre_proceso
    try:
        # # Obtener la posición actual del ratón
        # centro_ventana = obtener_centro_ventana(nombre_proceso)
        # if centro_ventana:
        #     print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
        #     click_raton_posicion (centro_ventana[0]+400, centro_ventana[1]-60)
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
def funcionestados():
    global dungeon, atacar, lanzabuff, entrartg, etapa
    global stop_flag
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionestados en ejecución")
        resultados = buscar_imagenes()
        dungeon, atacar, lanzabuff, entrartg, etapa = actualizar_estados(resultados)
    
    print("funcionestados terminada")
    

def funcionterminar():
    global terminar
    global dungeon
    global vidamostruo
    global etapa
    global atacar
    global final
    global nombre_proceso
    global terminando
    global tiempo_inicio
    global stop_flag
    global entrartg
    while not stop_flag and not keyboard.is_pressed('delete'):
        if entrartg == 0 :
            time.sleep(0.5)
            continue
        imagen_a_buscar_marcafin = "tg/marcafin.png"  # Reemplaza con la ruta de tu propia imagen
        marcafin = buscar_imagen_en_pantalla(imagen_a_buscar_marcafin)
        imagen_a_buscar_alert = "tg/alert.png"  # Reemplaza con la ruta de tu propia imagen
        alert = buscar_imagen_en_pantalla(imagen_a_buscar_alert)
        if alert:
            imagen_a_buscar_yesi = "tg/yesi.png"  # Reemplaza con la ruta de tu propia imagen
            yesi = buscar_imagen_en_pantalla(imagen_a_buscar_yesi)
            if yesi!=False : #and bloquearok==False and bloquearok1==False
                click_raton_posicion (yesi[0], yesi[1])

        print("funcionterminar en ejecución")
        time.sleep(1)
        imagen_a_buscar_recibir = "tg/recibir.png"  # Reemplaza con la ruta de tu propia imagen
        recibir = buscar_imagen_en_pantalla(imagen_a_buscar_recibir)
        time.sleep(0.5)
        if recibir!= False and marcafin:
            dungeon=2
            click_raton_posicion (recibir[0], recibir[1])

        
        time.sleep(0.5)
        if marcafin:
            imagen_a_buscar_salir = "tg/okfin.png"  # Reemplaza con la ruta de tu propia imagen
            salir = buscar_imagen_en_pantalla(imagen_a_buscar_salir)
            time.sleep(1)
            if salir!= False :
                print('salir1')
                etapa=0
                atacar=0
                keyboard.press_and_release("esc")

                click_raton_posicion (salir[0], salir[1])
                time.sleep(0.5)

            imagen_a_buscar_confirma3 = "tg/confirma3.png"  # Reemplaza con la ruta de tu propia imagen
            confirma3 = buscar_imagen_en_pantalla(imagen_a_buscar_confirma3)
            time.sleep(1)
            if confirma3!= False :
                print('confirma31')
                etapa=0
                atacar=0
                keyboard.press_and_release("esc")
                click_raton_posicion (confirma3[0], confirma3[1])
                time.sleep(0.5)

        imagen_a_buscar_selectch = "tg/selectch.png"  # Reemplaza con la ruta de tu propia imagen
        selectch = buscar_imagen_en_pantalla(imagen_a_buscar_selectch)
        if selectch!=False and not buscar_imagen_en_pantalla("otros/confirmasalir.png") :
            click_raton_posicion (selectch[0], selectch[1])
            time.sleep(1)
            dungeon=0
        if dungeon==2 and not buscar_imagen_en_pantalla("otros/confirmasalir.png"):
            keyboard.press_and_release("o")
            time.sleep(3)
            dungeon=0

        imagen_a_buscar_channel = "login/channel/7.png"  # Reemplaza con la ruta de tu propia imagen
        channel = buscar_imagen_en_pantalla(imagen_a_buscar_channel)
        if channel!=False and not buscar_imagen_en_pantalla("otros/confirmasalir.png"):
            click_raton_posicion (channel[0], channel[1])
            pyautogui.click(clicks=2, interval=0.1,button='left')
            time.sleep(1)
        # imagen_a_buscar_bloquearok1 = "tg/bloquearok1.png"  # Reemplaza con la ruta de tu propia imagen
        # bloquearok1 = buscar_imagen_en_pantalla(imagen_a_buscar_bloquearok1)
        # imagen_a_buscar_bloquearok = "tg/bloquearok.png"  # Reemplaza con la ruta de tu propia imagen
        # bloquearok = buscar_imagen_en_pantalla(imagen_a_buscar_bloquearok)
        # if  bloquearok1!=False:
        #     imagen_a_buscar_yesi = "tg/oknew.png"  # Reemplaza con la ruta de tu propia imagen
        #     okfin2 = buscar_imagen_en_pantalla(imagen_a_buscar_yesi)
        #     click_raton_posicion (okfin2[0], okfin2[1])
        imagen_a_buscar_yesi = "tg/yesi.png"  # Reemplaza con la ruta de tu propia imagen
        yesi = buscar_imagen_en_pantalla(imagen_a_buscar_yesi)
        if yesi!=False : #and bloquearok==False and bloquearok1==False
            click_raton_posicion (yesi[0], yesi[1])
            stop_flag = False
            contardg=0
            contadormostruos1=0
            dungeon=0
            entrartg=0
            permiso=0
            etapa=0
            terminar=False
            vidamostruo=False
            bm3WI1=False
            bosfinal=False
            terminando=0
            final=0
            conteocabal=0
            atacar=0
            pase=0
            lanzabuff=0
            conteo=0
          
            # stop_flag = True
            # os.system("shutdown /s /t 10")
            time.sleep(1)
           
    print("funcionterminar terminada")

def funcionetapa():
    global contardg
    global bosfinal
    global dungeon
    global terminar
    global contadormostruos1
    global vidamostruo
    global etapa
    global pase
    global muriendo
    global final
    global nombre_proceso
    global positivo
    global tiempo_inicio
    global stop_flag
    global atacar
    global tipotg
    global conteo
    global entrartg
    while not stop_flag and not keyboard.is_pressed('delete'):
        if entrartg == 0 :
            time.sleep(0.5)
            continue
        print("funcionetapa en ejecución")
        time.sleep(1)
        if etapa==1 and dungeon==1:
            time.sleep(5)
            centro_ventana = obtener_centro_ventana(nombre_proceso)
            if centro_ventana:
                print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                click_raton_posicion (centro_ventana[0]+(385*(positivo)), centro_ventana[1]+110)
                posicion_actual = pyautogui.position()
                pyautogui.mouseDown(button='left')
                time.sleep(7)
                pyautogui.mouseUp(button='left')
                keyboard.press_and_release("esc")
                print("entre estapa 1")

                # if tipotg=='TG':
                #     etapa = 3
                # if tipotg=='IP':
                #     etapa = 2
                # if tipotg=='MC':
                #     etapa = 4
                etapa_mapping = {
                    'TG': 3,
                    'IP': 2,
                    'MC': 4
                }
                if buscar_imagen_en_pantalla("tg/marcafin.png"):
                    etapa = 0
                else:
                    if buscar_imagen_en_pantalla("tg/marcafin.png"):
                        etapa = 0
                    else:
                        etapa = etapa_mapping.get(tipotg, etapa)  # Default to current etapa if tipotg not fo  und


        # if etapa==0 :
        #     centro_ventana = obtener_centro_ventana(nombre_proceso)
        #     if centro_ventana:
        #         print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
        #         click_raton_posicion (centro_ventana[0]+420, centro_ventana[1]+40)
        #         posicion_actual = pyautogui.position()
        #         pyautogui.mouseDown(button='left')
        #         time.sleep(7)
        #         pyautogui.mouseUp(button='left')
        #         keyboard.press_and_release("esc")
        #         print("entre estapa 0")
        #         keyboard.press_and_release("z")
        if etapa==2 and muriendo==0 and dungeon==1:
            if contadormostruos1<30:
                centro_ventana = obtener_centro_ventana(nombre_proceso)
                if centro_ventana:
                    print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                    click_raton_posicion (centro_ventana[0]+(400*(positivo)), centro_ventana[1]+40)
                    posicion_actual = pyautogui.position()
                    print("entre estapa 2")
                    
                    time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    
                    # desplazamiento_x =0   # Ajusta según sea necesario
                    # desplazamiento_y = 200
                    # mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y)
                    # keyboard.press_and_release("esc")
                    time.sleep(1)
                    keyboard.press_and_release("z")
            if contadormostruos1>30 and contadormostruos1<55:
                centro_ventana = obtener_centro_ventana(nombre_proceso)
                if centro_ventana:
                    print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                    click_raton_posicion (centro_ventana[0]+(400*(positivo)), centro_ventana[1]-60)
                    posicion_actual = pyautogui.position()
                    print("entre estapa 2")
                    
                    time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    
                    # desplazamiento_x =0   # Ajusta según sea necesario
                    # desplazamiento_y = 200
                    # mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y)
                    # keyboard.press_and_release("esc")
                    time.sleep(1)
                    keyboard.press_and_release("z")
            if contadormostruos1>55 and contadormostruos1<70:
                centro_ventana = obtener_centro_ventana(nombre_proceso)
                if centro_ventana:
                    print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                    click_raton_posicion (centro_ventana[0]+(400*(positivo)), centro_ventana[1]+230)
                    posicion_actual = pyautogui.position()
                    print("entre estapa 2")
                    
                    time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    
                    # desplazamiento_x =0   # Ajusta según sea necesario
                    # desplazamiento_y = 200
                    # mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y)
                    # keyboard.press_and_release("esc")
                    time.sleep(1)
                    keyboard.press_and_release("z")
            if contadormostruos1>70:
                centro_ventana = obtener_centro_ventana(nombre_proceso)
                if centro_ventana:
                    print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                    click_raton_posicion (centro_ventana[0]+(400*(positivo)), centro_ventana[1]-150)
                    posicion_actual = pyautogui.position()
                    print("entre estapa 2")
                    
                    time.sleep(0.5)
                    keyboard.press_and_release(".")
                    time.sleep(1)
                    keyboard.press_and_release(",")
                    time.sleep(0.9)
                    
                    # desplazamiento_x =0   # Ajusta según sea necesario
                    # desplazamiento_y = 200
                    # mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y)
                    # keyboard.press_and_release("esc")
                    time.sleep(1)
                    keyboard.press_and_release("z")
        if etapa==3 and dungeon==1:
            centro_ventana = obtener_centro_ventana(nombre_proceso)
            if centro_ventana:
                print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                click_raton_posicion (centro_ventana[0]+(200*(positivo)), centro_ventana[1]+80)
                posicion_actual = pyautogui.position()
                print("entre estapa 3")
                
                # time.sleep(0.5)
                # keyboard.press_and_release(".")
                # time.sleep(1)
                # keyboard.press_and_release(",")
                # time.sleep(0.9)
                
                # keyboard.press_and_release("esc")
                time.sleep(1)
                keyboard.press_and_release("z")


    print("funcionetapa terminada")



# Configurar la función de detección del evento de Escape

# Inicializar la variable de parada
stop_flag = False
contardg=0
contadormostruos1=0
dungeon=0
entrartg=0
etapa=0
tipotg='TG'
muriendo=0
terminar=False
vidamostruo=False
bm3WI1=False
bosfinal=False
terminando=0
final=0
conteocabal=0
atacar=0
pase=0
permiso=0
lanzabuff=0
positivo=(1)
conteo=0
nombre_proceso = "cabal"
tiempo_inicio = time.time()
forzar_deshabilitar_bloq_mayus()


funciones = [
    funcionentrartg,
    funcionSP,
    funcionvida,
    funcionmostruo,
    funcionBM,
    funcionBM3,
    funcionBM2,
    funcionmuerte,
    funciologin,
    funcionterminar,
    funcioiniciar,
    funcionetapa,
    funcionestados
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

