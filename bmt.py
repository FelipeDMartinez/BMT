from PC import processador_de_consultas
from GLI import gerador_de_lista_invertida
from INDEX import indexador
# from BUSCA import buscador
# from AVALIA import avaliacao
import time

if __name__ == "__main__":
    ini = time.time()

    ini_pc = time.time()
    processador_de_consultas()
    fim_pc = time.time()
    print(f'Tempo do processador de consulta: {fim_pc-ini_pc}s')

    ini_gli = time.time()
    gerador_de_lista_invertida()
    fim_gli = time.time()
    print(f'Tempo para gerar a lista invertida: {fim_gli-ini_gli}s')

    ini_index = time.time()
    indexador()
    fim_index = time.time()
    print(f'Tempo para indexador: {fim_index-ini_index}s')

    # ini_busca = time.time()
    # buscador()
    # fim_busca = time.time()
    # print(f'Tempo para buscador: {fim_busca-ini_busca}s')

    # ini_avalia = time.time()
    # avaliacao()
    # fim_avalia = time.time()
    # print(f'Tempo para avaliação: {fim_avalia-ini_avalia}s')

    fim = time.time()
    print(f'tempo total para rodar todo o sistema {fim-ini} s')
