# Importações
from collections import Counter
import operator

# Variáveis Universais
alfabeto = 'abcdefghijklmnopqrstuvwxyz'
index_cc = 0.074

# ------------- Tamanho da Chave -------------

def gera_sequencias_chave(texto, tam_chave):
    
    sequencias = list()

    for chave in range(tam_chave):

        construtor = str()
        for pulo in range(0, len(texto[chave:]), tam_chave):
            construtor += texto[chave + pulo]

        sequencias.append(construtor) 

    return sequencias

def calcula_indice(sequencia):

    soma = 0
    tam_sequencia = len(sequencia)

    for letra in alfabeto:
        frequencia_letra = sequencia.count(letra)
        soma += frequencia_letra * (frequencia_letra - 1)

    return soma / (tam_sequencia * (tam_sequencia - 1))    

def gera_indices(texto):
    indices = list()

    for tam_chave in range(1, len(alfabeto) + 1):
        soma = 0
        sequencias = gera_sequencias_chave(texto, tam_chave)

        for sequencia in sequencias:
            soma += calcula_indice(sequencia)
        
        indices.append(soma / len(sequencias))

    return indices

def descobre_tamanho_chave(texto):

    indices = gera_indices(texto)
    range   = 0.01
    ic_diff = 1

    while ic_diff > range:
        tam_chave = 0
        for ic in indices:
            if ic_diff > range:
                ic_diff = index_cc - ic
                tam_chave += 1
        range += range

    return tam_chave

# ---------------- Decifrador ----------------

def descobre_chave(sequencias):
    
    chave = str()

    for sequencia in sequencias:
        freq_letra = Counter(sequencia)
        mais_freq = max(freq_letra.items(), key=operator.itemgetter(1))[0]
        distancia_letra = ord(mais_freq) - ord('a')
        
        if distancia_letra < 0:
            distancia_letra += 26
        
        chave += chr(distancia_letra + 97)

    return chave

def decifrador(texto, tam_chave):
    
    sequencias = gera_sequencias_chave(texto, tam_chave)
    chave = descobre_chave(sequencias)
    texto_decifrado = str()

    for indice_letra in range(len(texto)):
        distancia_letra = ord(texto[indice_letra]) - ord(chave[indice_letra % len(chave)])

        if distancia_letra < 0:
            distancia_letra += 26
        
        texto_decifrado += chr(distancia_letra + 97)
    
    return chave, texto_decifrado


if __name__ == "__main__":

    # Le o arquivo
    with open('./text/pt.txt') as f:
        texto = f.readlines()[0]

    # Acha o tamanho da chave
    tam_chave = descobre_tamanho_chave(texto)

    # Acha a chave
    chave, texto_decifrado = decifrador(texto, tam_chave)
    
    print(f"Tamanho da chave: {tam_chave}")
    print(f"Chave encontrada: {chave}")
    print(f"Texto decifrado : {texto_decifrado[:50]}")