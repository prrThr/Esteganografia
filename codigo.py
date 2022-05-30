import numpy as np
import cv2 as cv
from pandas import array
#import matplotlib.pyplot as plt

img = cv.imread('parrot.jpg')
secret = cv.imread('secret.jpg')

#print(f"\nDimensões da imagem: {img.shape}")

#-----------------------------------------------------------------------------------#
#                     PROCURANDO O ULTIMO BIT VERMELHO #
#-----------------------------------------------------------------------------------#
altura, largura, canais = img.shape
lastPixel = img[altura-1, largura-1, 2]

#print(f"Último pixel em:  X:{altura}   Y:{largura}")
#print(f"Nível de vermelho no ultimo pixel = {lastPixel}")

#-----------------------------------------------------------------------------------#
#          CONVERTENDO A QUANTIDADE DE VERMELHO PARA BINÁRIO #
#-----------------------------------------------------------------------------------#


def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]


lastPixel_binario = bitfield(lastPixel)
#print(f"{lastPixel} em binario = {lastPixel_binario}")


def gerar_mensagem(mensagem):
    lista = []
    for m in mensagem:
        val = ord(m)
        bits = bitfield(val)

        if len(bits) < 8:
            for a in range(8-len(bits)):
                bits.insert(0, 0)
        lista.append(bits)
    arr = np.array(lista)
    arr = arr.flatten()
    return arr


texto = "MENSAGEM SECRETA"
arrayBits = gerar_mensagem(texto)  # Transformar o TEXTO em BñINÁRIO
# print(arrayBits)

img2 = img.copy()


def encriptar(img2):
    i = 0
    pararLoop = False

    for y in range(altura-1, 0, -1):
        if pararLoop == True:
            break
        for x in range(largura-1, 0, -1):
            if i == arrayBits.size-1:
                print(f"Parou no indice {i}")
                print(f"Valor binario final: {arrayBits[i-1]} Y:{y} x:{x+1}")
                pararLoop = True
                break

            if i == 0:
                print(f"Valor binario inicial: {arrayBits[i]} Y:{y} x:{x}")

            if arrayBits[i] == 0 and img2[y, x, 2] % 2 != 0:
                img2[y, x, 2] = img2[y, x, 2] - 1

            if arrayBits[i] == 1 and img2[y, x, 2] % 2 == 0:
                img2[y, x, 2] = img2[y, x, 2] - 1
            i = i + 1


encriptar(img2)


def debuggin(altura, largura, arrayBits):
    i = 0
    pararLoop = False
    for y in range(altura-1, 0, -1):
        if pararLoop == True:
            break
        for x in range(largura-1, 0, -1):
            if i == 25:
                print(f"Parou no indice {i}")
                print(f"Valor binario final: {arrayBits[i-1]} Y:{y} x:{x}")
                pararLoop = True
                break
                
            print(f"\nValor binario atual = {arrayBits[i]}")
            print(f"img  -> Y:{y} X:{x} - Red Value = {img[y, x, 2]}")
            print(f"img2 -> Y:{y} X:{x} - Red Value = {img2[y, x, 2]}")
            i = i + 1


debuggin(altura, largura, arrayBits)
