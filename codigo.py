import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('parrot.jpg')
secret = cv.imread('secret.jpg')

#print(f"\nDimensões da imagem: {img.shape}")

# ---------------------------------#
# PROCURANDO O ULTIMO BIT VERMELHO #
# ---------------------------------#
altura, largura, canais = img.shape
lastPixel = img[altura-1, largura-1, 2]

#print(f"Último pixel em:  X:{altura}   Y:{largura}")
#print(f"Nível de vermelho no ultimo pixel = {lastPixel}")

#---------------------------------------------------#
# CONVERTENDO A QUANTIDADE DE VERMELHO PARA BINÁRIO #
#---------------------------------------------------#


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
arrayBits = gerar_mensagem(texto)  # Transformar o TEXTO em BINÁRIO
# print(arrayBits)

img2 = img.copy()


def encriptar(img):
    i = 0
    pararLoop = False
    altura, largura, canais = img.shape
    for y in range(altura-1, 0, -1):
        if pararLoop == True:
            break
        for x in range(largura-1, 0, -1):
            if i == 0:
                print("---------------------------------")
                print(f"Valor binario inicial: {arrayBits[i]} Y:{y} x:{x}")
                print("---------------------------------")

            if arrayBits[i] == 0:
                if img[y, x, 2] % 2 != 0:
                    img[y, x, 2] = img[y, x, 2] - 1
            else:
                if img[y, x, 2] % 2 == 0:
                    img[y, x, 2] = img[y, x, 2] - 1
            i = i + 1
            if i == arrayBits.size-1:
                print(f"Parou no indice {i}")
                print(f"Valor binario final: {arrayBits[i]} Y:{y} x:{x}")
                pararLoop = True
                break


encriptar(img2)
i = 0
altura, largura, canais = img.shape
for y in range(altura-1, altura-6, -1):
    for x in range(largura-1, largura-6, -1):
        print(f"\nValor binario atual = {arrayBits[i]}")
        print(f"img -> Y:{y} X:{x} - Quantidade de vermelho = {img[y, x, 2]}")
        print(
            f"img2 -> Y:{y} X:{x} - Quantidade de vermelho = {img2[y, x, 2]}")
        i = i + 1
