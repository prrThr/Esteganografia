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
    input("Presione ENTER para encriptar dentro da imagem")
    i = 0
    pararLoop = False

    for y in range(altura-1, 0, -1):
        if pararLoop == True:
            break
        for x in range(largura-1, 0, -1):
            if i == arrayBits.size-1:
                pararLoop = True
                break

            if arrayBits[i] == 0 and img2[y, x, 2] % 2 != 0:
                img2[y, x, 2] = img2[y, x, 2] - 1

            if arrayBits[i] == 1 and img2[y, x, 2] % 2 == 0:
                img2[y, x, 2] = img2[y, x, 2] - 1
            i = i + 1
    print("Mensagem encriptada!")


def converter_mensagem(saida):
    input("Presione ENTER para decriptar a mensagem")
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
    input("Presione ENTER para procurar os ultimos valores de vermelho dentro da imagem")
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
    input("Presione ENTER para retornar a mensagem em binario")
    lista = []
    for i in range(len(lastReds)):
        aux = bitfield(lastReds[i])
        lista.append(aux[-1])
    arr = np.array(lista)
    arr = arr.flatten()
    return arr


def main():
    img = cv.imread('parrot.jpg')
    cv.imshow("", img)
    cv.waitKey(0)

    texto = input(str("Digite o codigo para decriptar a imagem secreta: "))
    arrayBits = gerar_mensagem(texto)  # Transformar o TEXTO em BINÁRIO

    print(f"\n\nDimensões da imagem: {img.shape}")

    altura, largura, canais = img.shape

    img2 = img.copy()
    encriptar(img2, arrayBits, altura, largura)

    lastReds = []
    lastReds = lastRed_secretos(img2, arrayBits, altura, largura)
    print(f"Ultimos valores vermelhos = {lastReds}")
    lastBits = lastBits_secretos(lastReds)
    print(f"Mensagem nao traduzida = {lastBits}")
    mensagem_traduzida = converter_mensagem(lastBits)
    #print(f"\nMensagem traduzida = {mensagem_traduzida}")
    print("Mensagem decriptada com sucesso!")
    print("Mostrando imagem...")

    if mensagem_traduzida  == 'aviao.png':
        img2 = cv.imread('aviao.png')
        cv.imshow("", img2)
        cv.waitKey(0)
        print("Processo de decriptacao executado com sucesso!")
    else:
        print("Processo de decriptacao executado sem sucesso!")



main()
