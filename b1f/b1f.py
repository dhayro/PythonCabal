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
    global lanzabuff
    global stop_flag
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

        print('Número de sp: ', len(ctns))
        print('DG1: ',contardg)
        print('etapa inicial: ',etapa)
        # if len(ctns)==0:
        #     keyboard.press_and_release("-")
        
    print("funcionSP terminada")
def imagenhp():
    search = buscar_imagen_en_pantalla("otros/vida.png")
    if search== False:
        if path.exists('captura/captura_pantalla_HP.png'):
            remove("captura/captura_pantalla_HP.png")
        return False
    else:
        imagen_capturada = capturar_pantalla_hp(int(search[0])-10, int(search[1])-15, 165, 15)
        image = cv2.imread('captura/captura_pantalla_HP.png', cv2.IMREAD_GRAYSCALE)

        # Establecer umbrales para identificar la parte llena de la barra
        # Puedes ajustar estos valores según tus necesidades
        _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

        # Calcular la cantidad de píxeles blancos (llenados) y la cantidad total de píxeles
        pixels_filled = np.sum(thresh == 255)
        total_pixels = thresh.size

        # Calcular el porcentaje de llenado
        return (pixels_filled / total_pixels) * 100
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
    
    global stop_flag
    global tiempo_inicio
    while not stop_flag and not keyboard.is_pressed('delete'): 
        print("funcionvida en ejecución")
        time.sleep(1)
        vida = imagenhp()
        tiempo_transcurrido = time.time() - tiempo_inicio
        print(f"Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos")
        if vida!= False and vida <=23:
            keyboard.press_and_release("ctrl+9")
            time.sleep(1)
            keyboard.press_and_release("alt+6")
            time.sleep(18)
            vida = imagenhp()
            if vida!= False and vida <=23:
                keyboard.press_and_release("ctrl+9")
                time.sleep(1)
                keyboard.press_and_release("alt+5")
                time.sleep(30)
        
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
    global lanzabuff
    while not stop_flag and not keyboard.is_pressed('delete'): 
        if dungeon==1 and atacar==1 and terminando==0:
            print("funcionmostruo en ejecución")
            time.sleep(0.5)
            imagen_a_buscar_vidamostruo = "otros/mostrous.jpg"  # Reemplaza con la ruta de tu propia imagen
            vidamostruo = buscar_imagen_en_pantalla(imagen_a_buscar_vidamostruo)
            if vidamostruo!= False:
                contadormostruos1=0
                atacar=1
                lanzabuff=1
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
                # etapa=0
                print('variable atacar')
                # if vidamostruo <=25:
                #     keyboard.press_and_release("z") 
            else:
                keyboard.press_and_release("z") 
                contadormostruos1=contadormostruos1+1
                if contadormostruos1>=4 and dungeon==1:
                    atacar=0
                    lanzabuff=0
            # if bosfinal!=False:
            #     etapa=0
            #     final=1
        if dungeon==1 and atacar==0 and terminando==0:
            print("funcionmostruo en ejecución")
            time.sleep(0.5)
            imagen_a_buscar_vidamostruo = "otros/mostrous.jpg"  # Reemplaza con la ruta de tu propia imagen
            vidamostruo = buscar_imagen_en_pantalla(imagen_a_buscar_vidamostruo)
            if vidamostruo!= False:
                atacar=1
                lanzabuff=1
      
            
    print("funcionmostruo terminada")


def funcionBM():
    global bm3WI1
    global etapa
    global dungeon
    while not stop_flag and not keyboard.is_pressed('delete'): 
        print("funcionBM en ejecución")
        time.sleep(1)
        if vidamostruo!= False and dungeon==1 and etapa>0 :
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
    global bm3WI1
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
                # keyboard.press_and_release("z")
                time.sleep(0.5)
                
                imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                if bm3WI1!=False:
                    break
                if vidamostruo==False and contadormostruos1>=1:
                    keyboard.press_and_release("z")
                    time.sleep(0.5)
                    break
                
                keyboard.press_and_release("3")
                # keyboard.press_and_release("z")
                time.sleep(0.5)
                
                imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                if bm3WI1!=False:
                    break
                if vidamostruo==False and contadormostruos1>=1:
                    keyboard.press_and_release("z")
                    time.sleep(0.5)
                    break
                
                keyboard.press_and_release("4")
                # keyboard.press_and_release("z")
                time.sleep(0.5)
                
                imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                if bm3WI1!=False:
                    break
                if vidamostruo==False and contadormostruos1>=1:
                    keyboard.press_and_release("z")
                    time.sleep(0.5)
                    break
        
                keyboard.press_and_release("8")
                # keyboard.press_and_release("z")
                time.sleep(0.5)
                
                imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                if bm3WI1!=False:
                    break
                if vidamostruo==False and contadormostruos1>=1:
                    keyboard.press_and_release("z")
                    time.sleep(0.5)
                    break
                    
    print("funcionBM2 terminada")

def funcionBM3():
    global bm3WI1
    global dungeon
    global nombre_proceso
    global vidamostruo
    global stop_flag
    global etapa
    while not stop_flag and not keyboard.is_pressed('delete'): 
        print("funcionBM3 en ejecución")
        time.sleep(1)
        if vidamostruo!= False and dungeon==1 and etapa>0 and atacar==1:
            
            if bm3WI1!=False:
                while True:
                    # centro_ventanabm3 = obtener_centro_ventana(nombre_proceso)
                    # print(f"El centro de la ventanabm3 de {nombre_proceso} es ({centro_ventanabm3[0]}, {centro_ventanabm3[1]}).")
                    # raton_posicion (centro_ventanabm3[0], centro_ventanabm3[1])
                    
                    print('ataque BM3 con mostruos')
                    
                    keyboard.press_and_release("5")
                    # keyboard.press_and_release("z")
                    time.sleep(0.7)
                    imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    if bm3WI1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=1:
                        keyboard.press_and_release("z")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    # keyboard.press_and_release("z")
                    time.sleep(0.7)
                    imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    if bm3WI1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=1:
                        keyboard.press_and_release("z")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("6")
                    # keyboard.press_and_release("z")
                    time.sleep(0.7)
                    imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    if bm3WI1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=1:
                        keyboard.press_and_release("z")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    # keyboard.press_and_release("z")
                    time.sleep(0.7)
                    imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    if bm3WI1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=1:
                        keyboard.press_and_release("z")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    # keyboard.press_and_release("z")
                    time.sleep(0.7)
                    imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    if bm3WI1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=1:
                        keyboard.press_and_release("z")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("6")
                    # keyboard.press_and_release("z")
                    time.sleep(0.7)
                    imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    if bm3WI1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=1:
                        keyboard.press_and_release("z")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    # keyboard.press_and_release("z")
                    time.sleep(0.7)
                    imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    if bm3WI1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=1:
                        keyboard.press_and_release("z")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("5")
                    # keyboard.press_and_release("z")
                    time.sleep(0.7)
                    imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    if bm3WI1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=1:
                        keyboard.press_and_release("z")
                        time.sleep(0.5)
                        break
                    
                    keyboard.press_and_release("7")
                    # keyboard.press_and_release("z")
                    time.sleep(0.8)
                    imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    if bm3WI1==False:
                        break
                    if vidamostruo==False and contadormostruos1>=1:
                        keyboard.press_and_release("z")
                        time.sleep(0.5)
                        break
                    
                    # keyboard.press_and_release("7")
                    # # keyboard.press_and_release("space")
                    # time.sleep(1.1)
                    # imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    # bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    # if bm3WI1==False:
                    #     break
                    # if vidamostruo==False and contadormostruos1>=1:
                    #     # keyboard.press_and_release("space")
                    #     time.sleep(0.5)
                    #     break
                    
                    # keyboard.press_and_release("7")
                    # # keyboard.press_and_release("space")
                    # time.sleep(0.9)
                    # imagen_a_buscar_bm3WI1 = "otros/bm3WI1.png"  # Reemplaza con la ruta de tu propia imagen
                    # bm3WI1 = buscar_imagen_en_pantalla(imagen_a_buscar_bm3WI1)
                    # if bm3WI1==False:
                    #     break
                    # if vidamostruo==False and contadormostruos1>=1:
                    #     # keyboard.press_and_release("space")
                    #     time.sleep(0.5)
                    #     break
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
                keyboard.press("alt")
                time.sleep(0.5)
                keyboard.press_and_release("1")
                time.sleep(0.5)
                keyboard.release("alt")
                time.sleep(0.5)
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
                            # os.system("shutdown /s /t 10")
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
                        raton_posicion (centro_ventana2[0], centro_ventana2[1]-120)
                        # time.sleep(0.5)
                        # keyboard.press_and_release("alt+3")
                        # time.sleep(1)
                        # keyboard.press_and_release("alt+4")
                        time.sleep(0.5)
                        keyboard.press("+")
                        time.sleep(1.5)
                        keyboard.release("+")
                        time.sleep(0.5)
                        keyboard.press("alt")
                        time.sleep(0.5)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.press_and_release("2")
                        time.sleep(0.9)
                        keyboard.release("alt")
                        time.sleep(0.5)
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
        
        if etapa>0 and vidamostruo==False  and dungeon==1 and final==0 and bosfinal==False and terminar== False:
            centro_ventana2 = obtener_centro_ventana(nombre_proceso)
            if atacar==0:
                conteo=conteo+1
            else:
                conteo=0
            if conteo>10 and conteo<20 :
                keyboard.press_and_release("z")
                time.sleep(1.5)
                print('delante')
                keyboard.press_and_release("w")
                time.sleep(1.5)
            if conteo>20:
                keyboard.press_and_release("z")
                time.sleep(1.5)
                keyboard.press_and_release("s")
                print('atras')
                time.sleep(1.5)
            if etapa==1 and atacar==0:
                keyboard.press_and_release("f12")
                time.sleep(0.5)
                keyboard.press_and_release("f12")
                time.sleep(0.5)
                print(f"El centro de la ventana2 de etapa 1 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                posicion_actual = pyautogui.position()
                time.sleep(0.5)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.7) 
                keyboard.press_and_release("5")
                time.sleep(0.7)
                keyboard.press_and_release("5")
                time.sleep(0.7)
                keyboard.press_and_release("5")
                time.sleep(0.7)
                etapa=2
            if etapa==2 and atacar==0:
                print(f"El centro de la ventana2 de etapa 2 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+20)
                posicion_actual = pyautogui.position()
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
                time.sleep(0.5)
                keyboard.press_and_release("z")
                etapa=3
                atacar=1
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
                    raton_posicion (piso3_10[0]-100, piso3_10[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)                
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
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.release("alt")
                        time.sleep(0.5)
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
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.release("alt")
                        time.sleep(0.5)
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
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.release("alt")
                        time.sleep(0.5)
                        pase=1
                    imagen_a_buscar_piso1_5 = "b1f/piso1_5.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_5)
                    if piso1_5!=False :
                        raton_posicion (piso1_5[0]-100, piso1_5[1])
                        posicion_actual = pyautogui.position()
                        pyautogui.click(button='left')
                        time.sleep(2)
                        time.sleep(0.5)
                        pase=1
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
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.release("alt")
                        time.sleep(0.5)
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
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.release("alt")
                        time.sleep(0.5)
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
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.release("alt")
                        time.sleep(0.5)
                        # pase=1
                    imagen_a_buscar_piso1_5 = "b1f/piso1_5.png"  # Reemplaza con la ruta de tu propia imagen
                    piso1_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso1_5)
                    if piso1_5!=False :
                        raton_posicion (piso1_5[0]-100, piso1_5[1])
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
                keyboard.press("alt")
                time.sleep(0.5)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.release("alt")
                time.sleep(0.5)
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
                    raton_posicion (piso3[0]+5, piso3[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    etapa=6
                    atacar=0 
                imagen_a_buscar_piso3_1 = "b1f/piso3_1.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_1)
                if piso3_1!=False :
                    raton_posicion (piso3_1[0]+5, piso3_1[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0 
                imagen_a_buscar_piso3_2 = "b1f/piso3_2.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_2)
                if piso3_2!=False :
                    raton_posicion (piso3_2[0]+5, piso3_2[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    etapa=6
                    atacar=0 
                imagen_a_buscar_piso3_3 = "b1f/piso3_3.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_3)
                if piso3_3!=False :
                    raton_posicion (piso3_3[0]+5, piso3_3[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)  
                    etapa=6 
                    atacar=0 
                imagen_a_buscar_piso3_4 = "b1f/piso3_4.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_4)
                if piso3_4!=False :
                    raton_posicion (piso3_4[0]+5, piso3_4[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)  
                    etapa=6 
                    atacar=0 
                imagen_a_buscar_piso3_7 = "b1f/piso3_7.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_7 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_7)
                if piso3_7!=False :
                    raton_posicion (piso3_7[0]+5, piso3_7[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)  
                    etapa=6 
                    atacar=0 
                imagen_a_buscar_piso3_8 = "b1f/piso3_8.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_8 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_8)
                if piso3_8!=False :
                    raton_posicion (piso3_8[0]+5, piso3_8[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)  
                    etapa=6 
                    atacar=0 
                imagen_a_buscar_piso3_5 = "b1f/piso3_5.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_5)
                if piso3_5!=False :
                    raton_posicion (piso3_5[0]+5, piso3_5[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)  
                    etapa=6 
                    atacar=0 
                imagen_a_buscar_piso3_6 = "b1f/piso3_6.png"  # Reemplaza con la ruta de tu propia imagen
                piso3_6 = buscar_imagen_en_pantalla(imagen_a_buscar_piso3_6)
                if piso3_6!=False :
                    raton_posicion (piso3_6[0]+5, piso3_6[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)  
                    etapa=6 
                    atacar=0 
            if etapa==6 and atacar==0:
                if pase==0:
                    time.sleep(1.5)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]-15, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
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
                    keyboard.press_and_release("1")
                    time.sleep(1)
                    keyboard.press_and_release("1")
                    time.sleep(1)
                    keyboard.press_and_release("2")
                    time.sleep(0.9)
                    keyboard.press_and_release("1")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
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
                        raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                        posicion_actual = pyautogui.position()
                        keyboard.press("alt")
                        time.sleep(0.5)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.press_and_release("2")
                        keyboard.release("alt")
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
                        raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                        posicion_actual = pyautogui.position()
                        keyboard.press("alt")
                        time.sleep(0.5)
                        keyboard.press_and_release("1")
                        time.sleep(1)
                        keyboard.press_and_release("2")
                        keyboard.release("alt")
                        time.sleep(0.5)
                        etapa=7
                        pase=0
                        atacar=1
                        keyboard.press_and_release("z")
            if etapa==7 and atacar==0:
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
                imagen_a_buscar_piso6_2 = "b1f/piso6_2.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_2)
                if piso6_2!=False :
                    raton_posicion (piso6_2[0], piso6_2[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press("alt")
                    time.sleep(0.5)
                    keyboard.press_and_release("2")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso6_3 = "b1f/piso6_3.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_3)
                if piso6_3!=False :
                    raton_posicion (piso6_3[0], piso6_3[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press("alt")
                    time.sleep(0.5)
                    keyboard.press_and_release("2")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso6_4 = "b1f/piso6_4.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_4)
                if piso6_4!=False :
                    raton_posicion (piso6_4[0], piso6_4[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press("alt")
                    time.sleep(0.5)
                    keyboard.press_and_release("2")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso6_ = "b1f/piso6_.png"  # Reemplaza con la ruta de tu propia imagen
                piso6_ = buscar_imagen_en_pantalla(imagen_a_buscar_piso6_)
                if piso6_!=False :
                    raton_posicion (piso6_[0], piso6_[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press("alt")
                    time.sleep(0.5)
                    keyboard.press_and_release("1")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
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
                    raton_posicion (piso7[0]-100, piso7[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
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
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso7_1 = "b1f/piso7_1.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_1)
                if piso7_1!=False :
                    raton_posicion (piso7_1[0]-100, piso7_1[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
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
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso7_2 = "b1f/piso7_2.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_2 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_2)
                if piso7_2!=False :
                    raton_posicion (piso7_2[0]-80, piso7_2[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]-20, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press("alt")
                    time.sleep(0.5)
                    keyboard.press_and_release("1")
                    time.sleep(1.5)
                    keyboard.press_and_release("1")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso7_3 = "b1f/piso7_3.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_3 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_3)
                if piso7_3!=False :
                    raton_posicion (piso7_3[0]-80, piso7_3[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]-20, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press("alt")
                    time.sleep(0.5)
                    keyboard.press_and_release("1")
                    time.sleep(1.5)
                    keyboard.press_and_release("1")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso7_4 = "b1f/piso7_4.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_4 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_4)
                if piso7_4!=False :
                    raton_posicion (piso7_4[0]+120, piso7_4[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+5, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press("alt")
                    time.sleep(0.5)
                    keyboard.press_and_release("1")
                    time.sleep(1.5)
                    keyboard.press_and_release("1")
                    time.sleep(1.5)
                    keyboard.press_and_release("2")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso7_5 = "b1f/piso7_5.png"  # Reemplaza con la ruta de tu propia imagen
                piso7_5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso7_5)
                if piso7_5!=False :
                    raton_posicion (piso7_5[0]+120, piso7_5[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(3)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+5, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press("alt")
                    time.sleep(0.5)
                    keyboard.press_and_release("1")
                    time.sleep(1.5)
                    keyboard.press_and_release("1")
                    time.sleep(1.5)
                    keyboard.press_and_release("2")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0
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
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0]+5, centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
                    time.sleep(0.5)
                    keyboard.press("alt")
                    time.sleep(0.5)
                    keyboard.press_and_release("1")
                    time.sleep(1.5)
                    keyboard.press_and_release("1")
                    time.sleep(1.5)
                    keyboard.press_and_release("2")
                    time.sleep(1)
                    keyboard.release("alt")
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso5 = "b1f/piso5.png"  # Reemplaza con la ruta de tu propia imagen
                piso5 = buscar_imagen_en_pantalla(imagen_a_buscar_piso5)
                if piso5!=False :
                    raton_posicion (piso5[0]+100, piso5[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
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
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_piso5_1 = "b1f/piso5_1.png"  # Reemplaza con la ruta de tu propia imagen
                piso5_1 = buscar_imagen_en_pantalla(imagen_a_buscar_piso5_1)
                if piso5_1!=False :
                    raton_posicion (piso5_1[0]+100, piso5_1[1])
                    posicion_actual = pyautogui.position()
                    pyautogui.click(button='left')
                    time.sleep(2)
                    print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
                    raton_posicion (centro_ventana2[0], centro_ventana2[1]-225)
                    posicion_actual = pyautogui.position()
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
                    time.sleep(0.5)
                    # etapa=8
                    pyautogui.click(button='left')
                    time.sleep(0.5)
                    # keyboard.press_and_release("space")
                    # etapa=6
                    atacar=0 
                imagen_a_buscar_portal = "b1f/portal.png"  # Reemplaza con la ruta de tu propia imagen
                portal = buscar_imagen_en_pantalla(imagen_a_buscar_portal)
                if portal!=False :
                    etapa=8
                    keyboard.press_and_release("space")
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
                
        if etapa==8 and atacar==0:
            time.sleep(3)
            print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
            raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+35)
            posicion_actual = pyautogui.position()
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
            time.sleep(0.5)
            time.sleep(0.5)
            keyboard.press_and_release("z")
            atacar=1
            etapa=9
        if etapa==9 and atacar==0:
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
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
                raton_posicion (centro_ventana2[0]+250, centro_ventana2[1]+35)
                posicion_actual = pyautogui.position()
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
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.press_and_release("2")
                time.sleep(0.9)
                keyboard.press_and_release("1")
                time.sleep(1)
                keyboard.release("alt")
                time.sleep(0.5)
                keyboard.press_and_release("z")
                time.sleep(0.5)
                keyboard.press_and_release("5")
                time.sleep(0.9) 
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("5")
                time.sleep(0.9)
                keyboard.press_and_release("2")
                time.sleep(3)
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
                time.sleep(0.5)
                keyboard.press_and_release("z")
                atacar=1
                etapa=10
        if etapa==10 and atacar==0:
            print(f"El centro de la ventana2 de etapa 4 {nombre_proceso} es ({centro_ventana2[0]}, {centro_ventana2[1]}).")
            raton_posicion (centro_ventana2[0]+225, centro_ventana2[1]+35)
            posicion_actual = pyautogui.position()
            time.sleep(0.5)
            keyboard.press("alt")
            time.sleep(0.5)
            keyboard.press_and_release("1")
            time.sleep(1)
            keyboard.press_and_release("2")
            time.sleep(0.9)
            keyboard.release("alt")
            time.sleep(0.5)
            time.sleep(0.5)
            keyboard.press_and_release("z")
            atacar=1
        if etapa>=10:
            keyboard.press_and_release("space")
            time.sleep(0.5)
             


# Configurar la función de detección del evento de Escape

# Inicializar la variable de parada
stop_flag = False
contardg=0
contadormostruos1=0
dungeon=0
etapa=0
terminar=False
vidamostruo=False
bm3WI1=False
bosfinal=False
terminando=0
final=0
atacar=0
pase=0
lanzabuff=0
conteo=0
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