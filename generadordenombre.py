from PIL import Image, ImageDraw, ImageFont

def generar_imagen_texto(texto, fuente_path, tamaño_fuente=12, nombre_archivo="manager_cabal.png", espaciado=-1):
    # Your current code is using:
    # - NotoSans-Regular.ttf
    # - Font size 11
    # - Character spacing of -1
    color_texto = (240, 155, 0)  # naranja exacto
    color_fondo = (0, 0, 0)
    
    fuente = ImageFont.truetype(fuente_path, tamaño_fuente)

    # Calcular dimensiones con el texto normal
    temp = Image.new("RGB", (1, 1))
    d_temp = ImageDraw.Draw(temp)
    bbox = d_temp.textbbox((0, 0), texto, font=fuente)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Crear imagen con un poco más de ancho para manejar el espaciado
    img = Image.new("RGB", (w, h), color=color_fondo)
    draw = ImageDraw.Draw(img)
    
    # Dibujar cada carácter con el espaciado personalizado
    x_pos = -bbox[0]
    for char in texto:
        draw.text((x_pos, -bbox[1]), char, font=fuente, fill=color_texto)
        # Obtener el ancho del carácter actual
        char_bbox = d_temp.textbbox((0, 0), char, font=fuente)
        char_width = char_bbox[2] - char_bbox[0]
        # Avanzar la posición x con el ancho del carácter más el espaciado
        x_pos += char_width + espaciado

    # Recortar la imagen al tamaño real del texto con espaciado
    img = img.crop((0, 0, max(1, x_pos + bbox[0]), h))
    
    img.save(nombre_archivo)
    print("Guardado como", nombre_archivo)

# Usa tu fuente descargada
generar_imagen_texto("Warrior", fuente_path="C:/Program Files (x86)/CABAL Online (NA - Global)/Data/Font/NotoSans-Regular.ttf", tamaño_fuente=11, espaciado=-1)
