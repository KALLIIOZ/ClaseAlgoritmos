import os, time
from collections import Counter
import numpy as np

def read():

    file = './Gullivers_Travels.txt'

    fd = os.open(file, os.O_RDONLY)
    content = os.read(fd, os.path.getsize(file))

    os.close(fd)
    content = list(content.decode())

    return content

def my_counter(lista):
    conteos = {}

    for elemento in lista:
        if elemento in conteos:
            conteos[elemento] += 1
        else:
            conteos[elemento] = 1

    return conteos

def write(lista):
    frecuencia = my_counter(lista)
    with open('Gullivers_Travels_conteo.txt', 'w', encoding='utf-8') as archivo:
        for clave, valor in sorted(frecuencia.items(), key=lambda x: (x[0].isalpha(), x[0])):
            if clave == '\n':
                archivo.write(f"{'/',clave}:{valor}\n")
            else:
                archivo.write(f'{clave}:{valor}\n')


inicio= time.time()
#-----------------------------
write(read())
#-----------------------------
fin=time.time()

print('tiempo: ', fin-inicio)