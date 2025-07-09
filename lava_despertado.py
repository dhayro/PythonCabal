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
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os

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

        # Dibujar un rectángulo alrededor de las coincidencias
        for pt in zip(*loc[::-1]):
            cv2.rectangle(captura_pantalla_cv, pt, (pt[0] + imagen.shape[1], pt[1] + imagen.shape[0]), (0, 255, 0), 2)

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
    global etapa
    global contardg
    global stop_flag
    while not stop_flag and not keyboard.is_pressed('delete'):
        print("funcionSP en ejecución")
        time.sleep(1)
        imagen_a_buscar_bufsp = "otros/bufsp.png"  # Reemplaza con la ruta de tu propia imagen
        bufsp = buscar_imagen_en_pantalla(imagen_a_buscar_bufsp)
        if bufsp!=False :
            keyboard.press_and_release("ctrl+3")
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
    while not stop_flag and not keyboard.is_pressed('delete'): 
        if dungeon==1 and atacar==1 and terminando==0:
            print("funcionmostruo en ejecución")
            time.sleep(1)
            # imagen_a_buscar_bosfinal = "lava/bosfinal.png"  # Reemplaza con la ruta de tu propia imagen
            # bosfinal = buscar_imagen_en_pantalla(imagen_a_buscar_bosfinal)
            # time.sleep(1)
            # if bosfinal!=False:
            #     keyboard.press_and_release("alt+9")
            #     final=1
            #     time.sleep(1)
            #     keyboard.press_and_release("f11")
            #     time.sleep(1)
            vidamostruo = imagenmostruo()
            if vidamostruo!= False:
                contadormostruos1=0
                # etapa=0
                print('variable atacar')
                # if vidamostruo <=25:
                #     keyboard.press_and_release("z") 
            else:
                if etapa>1:
                    atacar=0
                else:
                    keyboard.press_and_release("z") 
                    contadormostruos1=contadormostruos1+1
                    if contadormostruos1>=4 and dungeon==1:
                        atacar=0
            # if bosfinal!=False:
            #     etapa=0
            #     final=1
      
            
    print("funcionmostruo terminada")


def funcionBM():
    global bm3GL1
    while not stop_flag and not keyboard.is_pressed('delete'): 
        print("funcionBM en ejecución")
        time.sleep(1)
        if vidamostruo!= False and dungeon==1 and etapa>0 :
            imagen_a_buscar_bm2GL = "otros/bm2GL.png"  # Reemplaza con la ruta de tu propia imagen
            bm2GL = buscar_imagen_en_pantalla(imagen_a_buscar_bm2GL)

            imagen_a_buscar_bm2GL1 = "otros/bm2GL1.png"  # Reemplaza con la ruta de tu propia imagen
            bm2GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2GL1)

            imagen_a_buscar_bm2GL2 = "otros/bm2GL2.png"  # Reemplaza con la ruta de tu propia imagen
            bm2GL2 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2GL2)

            # imagen_a_buscar_bm3GL = "otros/bm3GL.png"  # Reemplaza con la ruta de tu propia imagen
            # bm3GL = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL)

            # imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
            # bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)

            # imagen_a_buscar_bm3GL2 = "otros/bm3GL2.png"  # Reemplaza con la ruta de tu propia imagen
            # bm3GL2 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL2)
            # if bm3GL!=False and etapa>1 and (bm3GL1==False and bm2GL1==False ):
            #     # raton_posicion (bm3GL[0], bm3GL[1])
            #     # posicion_actual = pyautogui.position()
            #     # pyautogui.click(button='right')
            #     # pyautogui.click(button='right')
            #     keyboard.press_and_release("f12")
            #     time.sleep(0.5)
            #     keyboard.press_and_release("f12")
            #     time.sleep(0.5)
            #     if bm3GL2!=False:
            #         time.sleep(2)
            if bm2GL!=False and (bm3GL1==False and bm2GL1==False ):
                # raton_posicion (bm2GL[0], bm2GL[1])
                # posicion_actual = pyautogui.position()
                # pyautogui.click(button='right')
                # pyautogui.click(button='right')
                keyboard.press_and_release("f10")
                time.sleep(0.5)
                keyboard.press_and_release("f10")
                time.sleep(0.5)
                if bm2GL2!=False:
                    time.sleep(5)

    print("funcionBM terminada")

def funcionBM2():
    global bm3GL1
    global dungeon
    global contadormostruos1
    global nombre_proceso
    global vidamostruo
    global stop_flag
    global etapa
    while not stop_flag and not keyboard.is_pressed('delete'): 
        print("funcionBM2 en ejecución")
        time.sleep(1)
        if vidamostruo!= False and dungeon==1 and etapa>0 and atacar==1:
            
            while True:  
                # centro_ventananormal = obtener_centro_ventana(nombre_proceso)
                # print(f"El centro de la ventananormal de {nombre_proceso} es ({centro_ventananormal[0]}, {centro_ventananormal[1]}).")
                # raton_posicion (centro_ventananormal[0], centro_ventananormal[1])
                
                print('ataque normal con mostruos')
                
                keyboard.press_and_release("2")
                keyboard.press_and_release("space")
                time.sleep(0.5)
                
                imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                if bm3GL1!=False:
                    break
                if vidamostruo==False and contadormostruos1>=2:
                    keyboard.press_and_release("space")
                    time.sleep(0.5)
                    break
                
                keyboard.press_and_release("3")
                keyboard.press_and_release("space")
                time.sleep(0.5)
                
                imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                if bm3GL1!=False:
                    break
                if vidamostruo==False and contadormostruos1>=2:
                    keyboard.press_and_release("space")
                    time.sleep(0.5)
                    break
                
                keyboard.press_and_release("4")
                keyboard.press_and_release("space")
                time.sleep(0.5)
                
                imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                if bm3GL1!=False:
                    break
                if vidamostruo==False and contadormostruos1>=2:
                    keyboard.press_and_release("space")
                    time.sleep(0.5)
                    break
        
                keyboard.press_and_release("8")
                keyboard.press_and_release("space")
                time.sleep(0.5)
                
                imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                if bm3GL1!=False:
                    break
                if vidamostruo==False and contadormostruos1>=2:
                    keyboard.press_and_release("space")
                    time.sleep(0.5)
                    break
                    
    print("funcionBM2 terminada")

def funcionBM3():
    global bm3GL1
    global dungeon
    global nombre_proceso
    global vidamostruo
    global stop_flag
    global etapa
    while not stop_flag and not keyboard.is_pressed('delete'): 
        print("funcionBM3 en ejecución")
        time.sleep(1)
        if vidamostruo!= False and dungeon==1 and etapa>0 and atacar==1:
            
            if bm3GL1!=False:
                while True:
                    # centro_ventanabm3 = obtener_centro_ventana(nombre_proceso)
                    # print(f"El centro de la ventanabm3 de {nombre_proceso} es ({centro_ventanabm3[0]}, {centro_ventanabm3[1]}).")
                    # raton_posicion (centro_ventanabm3[0], centro_ventanabm3[1])
                    
                    print('ataque BM3 con mostruos')
                    
                    keyboard.press_and_release("5")
                    keyboard.press_and_release("space")
                    time.sleep(0.9)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    keyboard.press_and_release("space")
                    time.sleep(0.9)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("6")
                    keyboard.press_and_release("space")
                    time.sleep(0.9)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    keyboard.press_and_release("space")
                    time.sleep(0.9)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    keyboard.press_and_release("space")
                    time.sleep(0.9)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("6")
                    keyboard.press_and_release("space")
                    time.sleep(0.9)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    keyboard.press_and_release("space")
                    time.sleep(0.9)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    keyboard.press_and_release("space")
                    time.sleep(0.9)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("7")
                    keyboard.press_and_release("space")
                    time.sleep(1.1)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("7")
                    keyboard.press_and_release("space")
                    time.sleep(1.1)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("7")
                    keyboard.press_and_release("space")
                    time.sleep(0.9)
                    imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                    if bm3GL1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=2:
                        keyboard.press_and_release("space")
                        time.sleep(0.5)
                        break
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
    
def imagenlava():
    ruta_imagen = 'lava/despertado.png'
    pos = buscar_imagen_en_pantalla(ruta_imagen)
    if pos == False:
        print('no encontre lava')
        return False
    else:
        print('encontre lava')
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
    global contardg
    global dungeon
    global terminar
    global nombre_proceso
    global tiempo_inicio
    global bosfinal
    global final
    global terminando
    global stop_flag
    global atacar
    global etapa
    while not stop_flag and not keyboard.is_pressed('delete'): 
        print("funcioiniciar en ejecución")
        time.sleep(1)
        if dungeon==0 and terminar== False:
            centro_ventana = obtener_centro_ventana(nombre_proceso)
            if centro_ventana:
                dungeon=0
                etapa=0
                terminar= False
                bosfinal=False
                terminando=0
                final=0
                tiempo_inicio = time.time()
                imagen_a_buscar_bm2GL1 = "otros/bm2GL1.png"  # Reemplaza con la ruta de tu propia imagen
                bm2GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2GL1)

                imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                time.sleep(1)
                if bm3GL1!=False:
                    raton_posicion (bm3GL1[0], bm3GL1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
                    pyautogui.click(button='right')
                time.sleep(1)
                if bm2GL1!=False:
                    raton_posicion (bm2GL1[0], bm2GL1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
                    pyautogui.click(button='right')
                print(f"El centro de la ventana de {nombre_proceso} es ({centro_ventana[0]}, {centro_ventana[1]}).")
                raton_posicion (centro_ventana[0], centro_ventana[1]-120)
                posicion_actual = pyautogui.position()
                pyautogui.click(button='left')
                time.sleep(1)
                # pyautogui.click(button='left')
                # raton_posicion (centro_ventana[0], centro_ventana[1]+20)
                imagen_a_buscar_selectdg = "otros/selectdg.png"  # Reemplaza con la ruta de tu propia imagen
                selectdg = buscar_imagen_en_pantalla(imagen_a_buscar_selectdg)
                time.sleep(1)
                if selectdg!=False:
                    Lava = imagenlava()
                    if Lava!= False :
                        # click_raton_posicion (Lava[0], Lava[1])
                        print('clic lava')
                        noentrar = imagennoentrar()
                        entrar = imagenentrar()
                        time.sleep(2)
                        if noentrar!= False :
                            print('clic no entrar lava')
                            stop_flag = True
                            # os.system("shutdown /s /t 10")
                            break
                        else:
                            if entrar!= False :
                                click_raton_posicion (entrar[0], entrar[1])
                                print('clic entrar lava')
                    time.sleep(1)
                iniciar = imageniniciar()
                if iniciar!= False :
                    click_raton_posicion (iniciar[0], iniciar[1])
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]-50, centro_ventana2[1]-100)
                        time.sleep(0.5)
                        keyboard.press_and_release("alt+3")
                        time.sleep(1)
                        keyboard.press_and_release("alt+4")
                        time.sleep(1)
                        keyboard.press("alt")
                        time.sleep(0.5)
                        keyboard.press_and_release("1")
                        time.sleep(0.5)
                        keyboard.release("alt")
                        keyboard.press_and_release("z")
                        etapa=1
                        dungeon=1
                        atacar=1
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
                terminando=1
                imagen_a_buscar_bm2GL1 = "otros/bm2GL1.png"  # Reemplaza con la ruta de tu propia imagen
                bm2GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm2GL1)

                imagen_a_buscar_bm3GL1 = "otros/bm3GL1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3GL1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3GL1)
                time.sleep(1)
                if bm3GL1!=False:
                    raton_posicion (bm3GL1[0], bm3GL1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
                    pyautogui.click(button='right')
                time.sleep(1)
                if bm2GL1!=False:
                    raton_posicion (bm2GL1[0], bm2GL1[1]+5)
                    posicion_actual = pyautogui.position()
                    time.sleep(1)
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
            etapa=0
        imagen_a_buscar_salir = "otros/salir.png"  # Reemplaza con la ruta de tu propia imagen
        salir = buscar_imagen_en_pantalla(imagen_a_buscar_salir)
        time.sleep(1)
        if salir!= False and dungeon==1:
            print('salir1')
            click_raton_posicion (salir[0], salir[1])
            dungeon=0
            etapa=0
            terminar= False
            bosfinal=False
            final=0
            terminando=0
            tiempo_inicio = time.time()
            time.sleep(5)

def funcionetapa():
    global contardg
    global bosfinal
    global dungeon
    global terminar
    global contadormostruos1
    global vidamostruo
    global etapa
    global final
    global nombre_proceso
    global tiempo_inicio
    global stop_flag
    global atacar
    while not stop_flag and not keyboard.is_pressed('delete'): 
        print("funcionetapa en ejecución")
        time.sleep(1)
        
        if etapa>0 and vidamostruo==False  and dungeon==1 and final==0 and bosfinal==False and terminar== False:
            
            if etapa==1:
                imagen_a_buscar_lava0_1 = "lava/lava0_1.png"  # Reemplaza con la ruta de tu propia imagen
                lava0_1 = buscar_imagen_en_pantalla(imagen_a_buscar_lava0_1)
                if lava0_1!=False :
                    print('lava0_1')
                    atacar=0
                    raton_posicion (lava0_1[0], lava0_1[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                imagen_a_buscar_lava0_1_1 = "lava/lava0_1_1.png"  # Reemplaza con la ruta de tu propia imagen
                lava0_1_1 = buscar_imagen_en_pantalla(imagen_a_buscar_lava0_1_1)
                if lava0_1_1!=False :
                    print('lava0_1_1')
                    atacar=0
                    raton_posicion (lava0_1_1[0], lava0_1_1[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                imagen_a_buscar_lava1_1_1 = "lava/lava1_1_1.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_1_1 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_1_1)
                if lava1_1_1!=False :
                    print('lava1_1_1')
                    atacar=0
                    raton_posicion (lava1_1_1[0], lava1_1_1[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                imagen_a_buscar_lava1_1_1_1 = "lava/lava1_1_1_1.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_1_1_1 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_1_1_1)
                if lava1_1_1_1!=False :
                    print('lava1_1_1_1')
                    atacar=0
                    raton_posicion (lava1_1_1_1[0], lava1_1_1_1[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                imagen_a_buscar_lava1_1 = "lava/lava1_1.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_1 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_1)
                if lava1_1!=False :
                    print('lava1_1')
                    atacar=0
                    raton_posicion (lava1_1[0], lava1_1[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                imagen_a_buscar_lava1_12 = "lava/lava1_12.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_12 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_12)
                if lava1_12!=False :
                    print('lava1_12')
                    atacar=0
                    raton_posicion (lava1_12[0], lava1_12[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                imagen_a_buscar_lava1_2 = "lava/lava1_2.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_2 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_2)
                if lava1_2!=False :
                    print('lava1_2')
                    atacar=0
                    raton_posicion (lava1_2[0], lava1_2[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.mouseDown(button='left')
                    time.sleep(13)
                    pyautogui.mouseUp(button='left')
                imagen_a_buscar_lava1_3 = "lava/lava1_3.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_3 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_3)
                if lava1_3!=False :
                    print('lava1_3')
                    atacar=0
                    raton_posicion (lava1_3[0], lava1_3[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.mouseDown(button='left')
                    time.sleep(5)
                    pyautogui.mouseUp(button='left')
                imagen_a_buscar_bicho1_pecho = "lava/bicho1_pecho.png"  # Reemplaza con la ruta de tu propia imagen
                bicho1_pecho = buscar_imagen_en_pantalla(imagen_a_buscar_bicho1_pecho)
                if bicho1_pecho!=False :
                    raton_posicion (bicho1_pecho[0], bicho1_pecho[1]+10)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    print('detecte bicho1_pecho')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_bicho1_CABEZA = "lava/bicho1_CABEZA.png"  # Reemplaza con la ruta de tu propia imagen
                bicho1_CABEZA = buscar_imagen_en_pantalla(imagen_a_buscar_bicho1_CABEZA)
                if bicho1_CABEZA!=False :
                    raton_posicion (bicho1_CABEZA[0], bicho1_CABEZA[1]+10)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    print('detecte bicho1_CABEZA')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_bicho1_name = "lava/bicho1_name.png"  # Reemplaza con la ruta de tu propia imagen
                bicho1_name = buscar_imagen_en_pantalla(imagen_a_buscar_bicho1_name)
                if bicho1_name!=False :
                    raton_posicion (bicho1_name[0], bicho1_name[1]+10)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    print('detecte bicho1_name')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1])
            if etapa==2:
                imagen_a_buscar_bicho1_name = "lava/bicho1_name.png"  # Reemplaza con la ruta de tu propia imagen
                bicho1_name = buscar_imagen_en_pantalla(imagen_a_buscar_bicho1_name)
                if bicho1_name!=False :
                    raton_posicion (bicho1_name[0], bicho1_name[1]+10)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    print('detecte bicho1_name')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_bicho2_name3 = "lava/bicho2_name3.png"  # Reemplaza con la ruta de tu propia imagen
                bicho2_name3 = buscar_imagen_en_pantalla(imagen_a_buscar_bicho2_name3)
                if bicho2_name3!=False :
                    raton_posicion (bicho2_name3[0], bicho2_name3[1]+30)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    print('detecte bicho2_name3')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_bicho2_name = "lava/bicho2_name.png"  # Reemplaza con la ruta de tu propia imagen
                bicho2_name = buscar_imagen_en_pantalla(imagen_a_buscar_bicho2_name)
                if bicho2_name!=False :
                    raton_posicion (bicho2_name[0], bicho2_name[1]+10)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    print('detecte bicho2_name')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_bicho2_name2 = "lava/bicho2_name2.png"  # Reemplaza con la ruta de tu propia imagen
                bicho2_name2 = buscar_imagen_en_pantalla(imagen_a_buscar_bicho2_name2)
                if bicho2_name2!=False :
                    raton_posicion (bicho2_name2[0], bicho2_name2[1]+30)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    print('detecte bicho2_name2')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_bicho1_pecho = "lava/bicho1_pecho.png"  # Reemplaza con la ruta de tu propia imagen
                bicho1_pecho = buscar_imagen_en_pantalla(imagen_a_buscar_bicho1_pecho)
                if bicho1_pecho!=False :
                    raton_posicion (bicho1_pecho[0], bicho1_pecho[1]+10)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    print('detecte bicho1_pecho')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_lava1_5 = "lava/lava1_5.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_5 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_5)
                if lava1_5!=False :
                    raton_posicion (lava1_5[0], lava1_5[1]+10)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    keyboard.press_and_release("f11")
                    time.sleep(0.5)
                    keyboard.press_and_release("f11")
                    print('detecte lava1_5')
                imagen_a_buscar_lava1_9 = "lava/lava1_9.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_9 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_9)
                if lava1_9!=False :
                    raton_posicion (lava1_9[0], lava1_9[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=0
                    etapa=2
                    print('detecte lava1_9')
                imagen_a_buscar_lava1_4 = "lava/lava1_4.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_4 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_4)
                if lava1_4!=False :
                    print('lava1_4')
                    atacar=0
                    raton_posicion (lava1_4[0], lava1_4[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.mouseDown(button='left')
                    time.sleep(5)
                    pyautogui.mouseUp(button='left')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+100, centro_ventana2[1]-100)
                        time.sleep(0.5)
                        keyboard.press("alt")
                        time.sleep(0.5)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.press_and_release("2")
                        time.sleep(0.9)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.press_and_release("2")
                        time.sleep(0.9)
                        keyboard.release("alt")
                        time.sleep(1)
                        centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                        if centro_ventana2:
                            iniciar = False
                            print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                            raton_posicion (centro_ventana2[0]-230, centro_ventana2[1]-100)
                            time.sleep(0.5)
                            keyboard.press("alt")
                            time.sleep(0.5)
                            keyboard.press_and_release("1")
                            time.sleep(1)
                            keyboard.press_and_release("2")
                            time.sleep(0.9)
                            keyboard.press_and_release("1")
                            time.sleep(1)
                            keyboard.press_and_release("2")
                            time.sleep(0.9)
                            keyboard.release("alt")
                            time.sleep(1)
                imagen_a_buscar_lava1_6 = "lava/lava1_6.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_6 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_6)
                if lava1_6!=False :
                    print('lava1_6')
                    atacar=0
                    raton_posicion (lava1_6[0], lava1_6[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.mouseDown(button='left')
                    time.sleep(5)
                    pyautogui.mouseUp(button='left')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+100, centro_ventana2[1]-100)
                        time.sleep(0.5)
                        keyboard.press("alt")
                        time.sleep(0.5)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.press_and_release("2")
                        time.sleep(0.9)
                        keyboard.press_and_release("1")
                        # time.sleep(1)
                        # keyboard.press_and_release("2")
                        time.sleep(0.9)
                        keyboard.release("alt")
                        time.sleep(1)
                        centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                        if centro_ventana2:
                            iniciar = False
                            print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                            raton_posicion (centro_ventana2[0]-230, centro_ventana2[1]-100)
                            time.sleep(0.5)
                            keyboard.press("alt")
                            time.sleep(0.5)
                            keyboard.press_and_release("1")
                            time.sleep(1)
                            keyboard.press_and_release("2")
                            time.sleep(0.9)
                            keyboard.press_and_release("1")
                            time.sleep(1)
                            keyboard.press_and_release("2")
                            time.sleep(0.9)
                            keyboard.release("alt")
                            time.sleep(1)
                imagen_a_buscar_lava1_7 = "lava/lava1_7.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_7 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_7)
                if lava1_7!=False :
                    print('lava1_7')
                    atacar=0
                    raton_posicion (lava1_7[0], lava1_7[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.mouseDown(button='left')
                    time.sleep(10)
                    pyautogui.mouseUp(button='left')
                    imagen_a_buscar_gate_name = "lava/gate_name.png"  # Reemplaza con la ruta de tu propia imagen
                    gate_name = buscar_imagen_en_pantalla(imagen_a_buscar_gate_name)
                    if gate_name!=False :
                        raton_posicion (gate_name[0], gate_name[1]+10)
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        atacar=1
                        etapa=2
                        print('detecte gate_name')
                        centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                        if centro_ventana2:
                            iniciar = False
                            print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                            raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_lava1_10 = "lava/lava1_10.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_10 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_10)
                if lava1_10!=False :
                    print('lava1_10')
                    atacar=0
                    raton_posicion (lava1_10[0], lava1_10[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.mouseDown(button='left')
                    time.sleep(10)
                    pyautogui.mouseUp(button='left')
                    imagen_a_buscar_gate_name = "lava/gate_name.png"  # Reemplaza con la ruta de tu propia imagen
                    gate_name = buscar_imagen_en_pantalla(imagen_a_buscar_gate_name)
                    if gate_name!=False :
                        raton_posicion (gate_name[0], gate_name[1]+10)
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        atacar=1
                        etapa=2
                        print('detecte gate_name')
                        centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                        if centro_ventana2:
                            iniciar = False
                            print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                            raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_lava1_11 = "lava/lava1_11.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_11 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_11)
                if lava1_11!=False :
                    print('lava1_11')
                    atacar=0
                    raton_posicion (lava1_11[0], lava1_11[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.mouseDown(button='left')
                    time.sleep(10)
                    pyautogui.mouseUp(button='left')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+100, centro_ventana2[1]-100)
                        time.sleep(0.5)
                        keyboard.press("alt")
                        time.sleep(0.5)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.press_and_release("2")
                        time.sleep(0.9)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.release("alt")
                        time.sleep(1)
                    imagen_a_buscar_gate_name = "lava/gate_name.png"  # Reemplaza con la ruta de tu propia imagen
                    gate_name = buscar_imagen_en_pantalla(imagen_a_buscar_gate_name)
                    if gate_name!=False :
                        raton_posicion (gate_name[0], gate_name[1]+10)
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        atacar=1
                        etapa=2
                        print('detecte gate_name')
                        centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                        if centro_ventana2:
                            iniciar = False
                            print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                            raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_gate_name = "lava/gate_name.png"  # Reemplaza con la ruta de tu propia imagen
                gate_name = buscar_imagen_en_pantalla(imagen_a_buscar_gate_name)
                if gate_name!=False :
                    raton_posicion (gate_name[0], gate_name[1]+10)
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    atacar=1
                    etapa=2
                    print('detecte gate_name')
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0], centro_ventana2[1])
                imagen_a_buscar_lava1_8 = "lava/lava1_8.png"  # Reemplaza con la ruta de tu propia imagen
                lava1_8 = buscar_imagen_en_pantalla(imagen_a_buscar_lava1_8)
                if lava1_8!=False :
                    print('lava1_8')
                    raton_posicion (lava1_8[0], lava1_8[1]) #piso9
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2.5)
                    centro_ventana2 = obtener_centro_ventana(nombre_proceso)
                    if centro_ventana2:
                        iniciar = False
                        print(f"El centro de la ventana2 de {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                        raton_posicion (centro_ventana2[0]+300, centro_ventana2[1]+20)
                        time.sleep(0.5)
                        keyboard.press("alt")
                        time.sleep(0.5)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.press_and_release("2")
                        time.sleep(0.9)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.release("alt")
                        time.sleep(1)
                        atacar=1
                        etapa=1
        #         print('etapa 3')
        #         conteo=0
        #         while True:
        #             if etapa>0 and vidamostruo==False and contadormostruos1>=4  and dungeon==1 and bosfinal==False and terminar== False:
        #                 conteo=conteo+1
        #                 centro_ventana3 = obtener_centro_ventana(nombre_proceso)
        #                 if conteo > 10:
        #                     valore=170
        #                 else:
        #                     valore=160
        #                 if centro_ventana3:
        #                     print(f"El centro de la ventana3 de {nombre_proceso} es ({centro_ventana3[0]}, {centro_ventana3[1]}).")
        #                     raton_posicion (centro_ventana3[0]-80, centro_ventana3[1]-valore)
        #                     desplazamiento_x = 130  # Ajusta según sea necesario
        #                     desplazamiento_y = 0
        #                     mover_raton_clic_derecho(desplazamiento_x, desplazamiento_y)
        #                     posicion_actual = pyautogui.position()
        #                     iportal = "lava/portal2.png"  # Reemplaza con la ruta de tu propia imagen
        #                     portal = buscar_imagen_en_pantalla(iportal) 
        #                     time.sleep(1)
        #                     if portal!=False:
        #                         keyboard.press_and_release("space")
        #                         contadormostruos1=0
        #                         etapa=0
        #                         time.sleep(3)
        #                         keyboard.press_and_release("z")
        #                         break
        #                     keyboard.press_and_release("z")
        #                     if vidamostruo!=False:
        #                         etapa=0
        #                         break
        #                     if terminar!=False:
        #                         etapa=0
        #                         break
        #                     if bosfinal!=False:
        #                         etapa=0
        #                         break
        #                     imagen_a_buscar_fail = "otros/fail.png"  # Reemplaza con la ruta de tu propia imagen
        #                     fail = buscar_imagen_en_pantalla(imagen_a_buscar_fail)
        #                     if fail!= False:
        #                         etapa=0
        #                         break
        #             else:
        #                 etapa=0
        #                 break


# Configurar la función de detección del evento de Escape

# Inicializar la variable de parada
stop_flag = False
contardg=0
contadormostruos1=0
dungeon=0
etapa=0
terminar=False
vidamostruo=False
bm3GL1=False
bosfinal=False
terminando=0
final=0
atacar=0
nombre_proceso = "cabal"
tiempo_inicio = time.time()
# Crear un ThreadPoolExecutor con, por ejemplo, 2 hilos
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    # Programar las funciones para su ejecución concurrente
    futuros = [executor.submit(funcionSP),
    executor.submit(funcionvida),
    executor.submit(funcionmostruo),
    executor.submit(funcionBM),
    executor.submit(funcionBM3),
    executor.submit(funcionBM2),
    executor.submit(funcionfail),
    executor.submit(funcionmuerte),
    executor.submit(funcioiniciar),
    executor.submit(funcionterminar),
    executor.submit(funcionetapa) ]
    


    # Esperar a que todas las funciones hayan terminado
    keyboard.wait('delete')

        # Cancelar las funciones que aún estén en ejecución
    for futuro in futuros:
        futuro.cancel()


print("Programa terminado.")