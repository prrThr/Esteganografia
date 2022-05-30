import numpy as np
import cv2 as cv

img = cv.imread('parrot.jpg')
secret = cv.imread('secret.jpg')

#print(f"\nDimensões da imagem: {img.shape}")                #* Tirar comentário após terminar

altura, largura, canais = img.shape
lastPixel = img[altura-1, largura-1, 2]

#print(f"Último pixel em:  X:{altura}   Y:{largura}")        #* Tirar comentário após terminar
#print(f"Nível de vermelho no ultimo pixel = {lastPixel}")   #* Tirar comentário após terminar

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]

#lastPixel_binario = bitfield(lastPixel) #! Provavelmente nao vai usar o lastPixel
#print(f"{lastPixel} em binario = {lastPixel_binario}")     #* Tirar comentário após terminar




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
# print(arrayBits)                                       #* Tirar comentário após terminar

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

'''
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
'''

def converter_mensagem(saida):
    bits = np.array(saida)
    mensagem_out = ''
    bits = bits.reshape((int(len(saida)/8), 8))
    for b in bits:
        sum = 0
        for i in range(8):
            sum += b[i]*(2**(7-i))
        mensagem_out += chr(sum)
    return mensagem_out


def lastRed_secretos(img2):
    lista = []
    i = 0
    pararLoop = False

    for y in range(altura-1, 0, -1):
        if pararLoop == True:
            break
        for x in range(largura-1, 0, -1):
            if i == arrayBits.size-1:
                pararLoop = True
                break

            if arrayBits[i] == 0:
                if img2[y, x, 2] % 2 == 0:
                    lista.append(img2[y, x, 2])
                else:
                    lista.append(img2[y, x, 2] + 1)

            if arrayBits[i] == 1:
                if img2[y, x, 2] % 2 != 0:
                    lista.append(img2[y, x, 2])
                else:
                    lista.append(img2[y, x, 2] + 1)
            i = i + 1
        return lista

def lastBits_secretos(lastReds):
    lista = []
    for i in range(len(lastReds)):
        aux = bitfield(lastReds[i])
        lista.append(aux[-1])
    arr = np.array(lista)
    arr = arr.flatten()
    return arr
    

lastReds = []    
lastReds = lastRed_secretos(img2)
lastBits = lastBits_secretos(lastReds)
print(f"ArrayBits = {arrayBits}")
#print(f"Last Reds = {lastReds}")
print(f"Last Bits = {lastBits}")
print(f"ArrayBits traduzido = {converter_mensagem(arrayBits)}") 
print(f"Bits Secretos traduzido = {converter_mensagem(lastBits)}") 


