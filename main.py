import os, io
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'api_vision_key.json'
client=vision.ImageAnnotatorClient()

path = r'./images/letrero.jpg'
path2 = r'./images/imagen.jpg' 
def leer_texto_imagen(path):
    with io.open(path,'rb') as imagen_f:
        contenido = imagen_f.read()

    image = vision.types.Image(content=contenido) # pylint: disable=no-member
    response = client.text_detection(image= image) # pylint: disable=no-member
    json_response = response.text_annotations

    texto = ''
    for text in json_response:
        texto += text.description
        break
    print(texto)

def leer_texto_a_mano(path):
    with io.open(path,'rb') as imagen_f:
        contenido = imagen_f.read()

    image = vision.types.Image(content=contenido) # pylint: disable=no-member
    response = client.document_text_detection(image= image) # pylint: disable=no-member
    json_response = response.full_text_annotation
    print("Este es el texto completo", json_response.text)
    for pag in json_response.pages:
        for block in pag.blocks:
            print('\nConfianza en todo el block: {}\n'.format(block.confidence))

            for parrafo in block.paragraphs:
                print('Confianza en el párrafo: {}'.format(
                    round(parrafo.confidence,2)))

                for palabra in parrafo.words:
                    palabra_texto = ''.join([
                        symbol.text for symbol in palabra.symbols
                    ])
                    print('Palabras: {} (Confianza: {})'.format(
                        palabra_texto, round(palabra.confidence,2)))

                    for simbolo in palabra.symbols:
                        print('\tSimbolos: {} (confianza: {})'.format(
                            simbolo.text, round(simbolo.confidence,2)))

   

leer_texto_a_mano(path2)