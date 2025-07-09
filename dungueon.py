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
    # Cargar la imagen a buscar
    imagen = cv2.imread(imagen_path)
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

        # Obtener el color del borde de la imagen
        borde_color = imagen[0, 0].tolist()  # Color del píxel en la esquina superior izquierda

        # Dibujar un rectángulo alrededor de las coincidencias con el color del borde de la imagen original
        for pt in zip(*loc[::-1]):
            cv2.rectangle(captura_pantalla_cv, pt,
                          (pt[0] + imagen.shape[1], pt[1] + imagen.shape[0]),
                          borde_color, 2)

        # Mostrar la captura de pantalla con los rectángulos de coincidencia
        # cv2.imshow('Captura de pantalla', captura_pantalla_cv)
        # cv2.waitKey(0)

        if len(loc[0]) > 0:
            x = loc[1][0]
            y = loc[0][0]

            # Obtener las dimensiones de la imagen
            ancho, alto = imagen_gris.shape[::-1]

            # Calcular el centro de la coincidencia
            centro_x = x + ancho // 2
            centro_y = y + alto // 2

            return centro_x, centro_y
        else:
            return False

    except Exception as e:
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
    search = buscar_imagen_en_pantalla("otros/mostrous.jpg")
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
            dungeon=0
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
            ordenar_reinicio()
            tiempo_inicio = time.time()
            time.sleep(0.5)
        if fail!= False and dungeon==0: #and puertita==0 and terminar== False and muriendo==0
            ok=imagenok()
            if ok!= False:
                print('salir2')
                click_raton_posicion (ok[0], ok[1])
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



def buscar_y_hacer_click(imagen, offset_x, offset_y, button='left'):
    """
    Busca una imagen en la pantalla y, si se encuentra, mueve el ratón a la posición con un offset dado y hace clic.
    """
    ubicacion = buscar_imagen_en_pantalla(imagen)
    if ubicacion:
        raton_posicion(ubicacion[0] + offset_x, ubicacion[1] + offset_y)
        time.sleep(0.5)
        pyautogui.click(button=button)
    return ubicacion

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
        global terminando
        global confirmatronco
        global puertita
        global lanzabuff
        global atacar
        global fin2
        time.sleep(1)
        imagen_a_buscar_dgfuera = "dungueon/dgfuera.png"  # Reemplaza con la ruta de tu propia imagen
        dgfuera = buscar_imagen_en_pantalla(imagen_a_buscar_dgfuera)
        time.sleep(0.5)
        if dgfuera!=False:
            dungeon=0
        
        if dungeon==0:
            keyboard.press_and_release("i")
            time.sleep(1)
            imagen_a_buscar_inventario = "dungueon/inventario.png"
            inventario = buscar_imagen_en_pantalla(imagen_a_buscar_inventario)
            time.sleep(0.5)

            imagen_a_buscar_inventario2 = "dungueon/inventario2.png"
            inventario2 = buscar_imagen_en_pantalla(imagen_a_buscar_inventario2)
            time.sleep(0.5)

            if inventario and not inventario2:
                # Abrir inventario 2 si no está abierto
                buscar_y_hacer_click(imagen_a_buscar_inventario, -170, 35)
                time.sleep(0.5)
                inventario2 = buscar_imagen_en_pantalla(imagen_a_buscar_inventario2)

            if inventario2:
                # Coordenadas de las posiciones relativas a `inventario2`
                offsets = [(-20, 40), (30, 40), (70, 40), (120, 40), (170, 40), (210, 40), (250, 40), (300, 40),
                           (-20, 85), (30, 85), (70, 85), (120, 85), (170, 85), (210, 85), (250, 85), (300, 85),]

                i = 0  # Iniciar el índice del bucle en 5 para saltar los primeros 5 intentos

                for i, (offset_x, offset_y) in enumerate(offsets[i:], start=i):
                    print(f"Intento {i} con offset ({offset_x}, {offset_y})")
                    if inventario2:
                        buscar_y_hacer_click(imagen_a_buscar_inventario2, offset_x, offset_y, button='right')
                        time.sleep(0.5)
                        
                        # Buscar warp después de hacer clic derecho
                        imagen_a_buscar_warp = "dungueon/warp.png"
                        warp = buscar_imagen_en_pantalla(imagen_a_buscar_warp)
                        time.sleep(0.5)
                        if warp:
                            print("Warp encontrado, saliendo del bucle.")
                            break
            imagen_a_buscar_warp = "dungueon/warp.png"  # Reemplaza con la ruta de tu propia imagen
            warp = buscar_imagen_en_pantalla(imagen_a_buscar_warp)
            time.sleep(0.5)
            if warp!=False:
                imagen_a_buscar_siwarp = "dungueon/siwarp.png"  # Reemplaza con la ruta de tu propia imagen
                siwarp = buscar_imagen_en_pantalla(imagen_a_buscar_siwarp)
                time.sleep(0.5)
                if siwarp!=False:
                    raton_posicion (siwarp[0], siwarp[1]) 
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    pyautogui.click(button='left')

            imagen_a_buscar_selectdg = "otros/selectdg.png"  # Reemplaza con la ruta de tu propia imagen
            selectdg = buscar_imagen_en_pantalla(imagen_a_buscar_selectdg)
            time.sleep(0.5)
            if selectdg!=False:
                entrar = imagenentrar()
                if entrar!= False :
                    click_raton_posicion (entrar[0], entrar[1])
                    print('clic entrar1')
            imagen_a_buscar_salix = "otros/salix.png"  # Reemplaza con la ruta de tu propia imagen
            salix = buscar_imagen_en_pantalla(imagen_a_buscar_salix)
            time.sleep(0.5)
            if salix!=False:
                dungeon=1



    print("funcioiniciar terminada")




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

# def funcionterminar():
#     global terminar
#     global dungeon
#     global vidamostruo
#     global etapa
#     global terminando
#     global ultimo
#     global bosfinal
#     global nombre_proceso
#     global tiempo_inicio
#     global terminarok
#     global stop_flag
#     global contadormostruos1
#     global bm3GL1

#     while not stop_flag and not keyboard.is_pressed('delete'):
#         print("funcionterminar en ejecución")
#         time.sleep(1)
#         terminar = imagenterminar()
#         time.sleep(1)
#         if terminar!= False :
#                 print('Terminando')
#                 terminando=1
#                 etapa=0
#                 click_raton_posicion (terminar[0], terminar[1])
#                 time.sleep(1)
#         imagen_a_buscar_dungeo = "otros/dungeo.png"  # Reemplaza con la ruta de tu propia imagen
#         dungeo = buscar_imagen_en_pantalla(imagen_a_buscar_dungeo)
#         time.sleep(0.5)
#         if dungeo!=False and dungeon==1:
#             stop_flag = False
#             contadormostruos1=0
#             terminarok=0
#             dungeon=2
#             etapa=0
#             terminando=0
#             terminar=False
#             vidamostruo=False
#             bm3GL1=False
#             bosfinal=False
#             ultimo=0
            
#             tiempo_inicio = time.time()

#         if dungeon==2 and dungeo!=False:
#             imagen_a_buscar_recibir = "otros/recibir.png"  # Reemplaza con la ruta de tu propia imagen
#             recibir = buscar_imagen_en_pantalla(imagen_a_buscar_recibir)
#             time.sleep(1)
#             if recibir!= False:
#                 click_raton_posicion (recibir[0], recibir[1])
#             imagen_a_buscar_obtenerpuntos = "otros/obtenerpuntos.png"  # Reemplaza con la ruta de tu propia imagen
#             obtenerpuntos = buscar_imagen_en_pantalla(imagen_a_buscar_obtenerpuntos)
#             time.sleep(1)
#             if obtenerpuntos!= False:
#                 click_raton_posicion (obtenerpuntos[0], obtenerpuntos[1])
#             imagen_a_buscar_dado = "otros/dado.png"  # Reemplaza con la ruta de tu propia imagen
#             dado = buscar_imagen_en_pantalla(imagen_a_buscar_dado)
#             time.sleep(1)
#             if dado!= False:
#                 click_raton_posicion (dado[0], dado[1])
#                 print('salir1')
#                 time.sleep(0.5)
#                 dungeon=0

#     print("funcionterminar terminada")

def funcionterminar():
    global terminar, dungeon, vidamostruo, etapa, terminando, ultimo, bosfinal, nombre_proceso
    global tiempo_inicio, terminarok, stop_flag, contadormostruos1, bm3GL1

    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionterminar en ejecución")
        
        terminar = imagenterminar()
        if terminar:
            print('Terminando')
            terminando = 1
            etapa = 0
            click_raton_posicion(terminar[0], terminar[1])
            time.sleep(0.5)  # Reduced sleep time
        
        dungeo = buscar_imagen_en_pantalla("otros/dungeo.png")
        if dungeo and dungeon == 1:
            stop_flag = False
            contadormostruos1 = terminarok = etapa = terminando = ultimo = 0
            dungeon = 2
            terminar = vidamostruo = bm3GL1 = bosfinal = False
            tiempo_inicio = time.time()
        
        if dungeon == 2 and dungeo:
        # Buscar y hacer clic en "recibir"
            recibir = buscar_imagen_en_pantalla("otros/recibir.png")
            if recibir:
                click_raton_posicion(recibir[0], recibir[1])
                time.sleep(0.3)
            
            # Buscar y hacer clic en "obtenerpuntos"
            obtenerpuntos = buscar_imagen_en_pantalla("otros/obtenerpuntos.png")
            if obtenerpuntos:
                click_raton_posicion(obtenerpuntos[0], obtenerpuntos[1])
                time.sleep(0.3)
            
            # Buscar y hacer clic en "dado"
            dado = buscar_imagen_en_pantalla("otros/dado.png")
            if dado:
                click_raton_posicion(dado[0], dado[1])
                print('salir1')
                dungeon = 0
                time.sleep(0.3)

        time.sleep(0.5)  # Reduced main loop sleep time

    print("funcionterminar terminada")



def detener_todo():
    global stop_flag
    while not stop_flag:
    # Verificar si se presionó la tecla 'End'
        if keyboard.is_pressed('end'):
            stop_flag = True
            print("Parando todas las funciones...")
            break  

# Inicia la búsqueda y ejecución de acciones en una ventana específica

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
nombre_proceso = "cabal"
grupo_actual="grupo1"
tiempo_inicio = time.time()
forzar_deshabilitar_bloq_mayus()


# Lista de funciones a ejecutar
funciones = [
    funcionSP,
    funcionmuerte,
    funcioiniciar,
    funcionterminar
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
# Lista de funciones a ejecutar
