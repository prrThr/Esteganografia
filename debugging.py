#-----------------------------------------------------------------------------#
# USAR ESTE CÓDIGO NO PROGRAMA PRINCIPAL CASO QUERIA VERIFICAR AS INFORMAÇÕES #
#-----------------------------------------------------------------------------#
import numpy as np
import cv2 as cv


def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]


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


def encriptar(img2, arrayBits, altura, largura):
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



def debuggin(img, img2, altura, largura, arrayBits):
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


def lastRed_secretos(img2, arrayBits, altura, largura):
    lista = []
    i = 0
    pararLoop = False

    for y in range(altura-1, 0, -1):
        if pararLoop == True:
            break
        for x in range(largura-1, 0, -1):
            if i == arrayBits.size:
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


def main():
    img = cv.imread('parrot.jpg')
    secret = cv.imread('secret.jpg')

    print(f"\nDimensões da imagem: {img.shape}")

    altura, largura, canais = img.shape
    lastPixel = img[altura-1, largura-1, 2]

    print(f"Último pixel em:  X:{altura}   Y:{largura}")
    print(f"Nível de vermelho no ultimo pixel = {lastPixel}")

    texto = input(str("Digite sua mensagem secreta: "))
    arrayBits = gerar_mensagem(texto)  # Transformar o TEXTO em BINÁRIO

    img2 = img.copy()
    encriptar(img2, arrayBits, altura, largura)
    debuggin(img, img2, altura, largura, arrayBits)

    lastReds = []
    lastReds = lastRed_secretos(img2, arrayBits, altura, largura)
    lastBits = lastBits_secretos(lastReds)
    #print(f"ArrayBits = {arrayBits}")   Apenas para
    #print(f"Last Reds = {lastReds}")    verificar se
    #print(f"Last Bits = {lastBits}")    estão certos
    #print(f"ArrayBits traduzido = {converter_mensagem(arrayBits)}")
    print(f"Mensagem secreta traduzida = {converter_mensagem(lastBits)}")

main()
