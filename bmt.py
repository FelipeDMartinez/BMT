from PC import processador_de_consultas
from GLI import gerador_de_lista_invertida
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
    print(f'tempo para gerar a lista invertida: {fim_gli-ini_gli}s')
    fim = time.time()
    print(f'tempo total para rodar todo o sistema {fim-ini} s')
