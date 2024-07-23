import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def avaliacao():
    with open('AVALIA.CFG', 'r') as CFG:
        for linha in CFG:
            if linha[0] == 'R':
                arquivo = (linha.split('=')[1])[1:-2]
                resultados = pd.read_csv(arquivo, sep=';',dtype={'Query': str})
                resultados['Resultados'] = resultados['Resultados'].apply(lambda x: eval(x))
 
            elif linha[0] == 'E':
                arquivo = (linha.split('=')[1])[1:-1]
                esperados = pd.read_csv(arquivo, sep=';',dtype={'QueryNumber': str})

        listaPrecisaoRevocacao = []
        listaF1 = []
        listaPrecisaoK5 = []
        listaPrecisaoK10 = []
        listaRPrecisao = []
        for query, resultados in zip(resultados['Query'], resultados['Resultados']):
            documentosRelevantes = esperados[esperados['QueryNumber'] == query]['DocNumber'].tolist()

            documentosRecuperados = [int(resultado[1]) for resultado in resultados]
            documentosRecuperadosK5 = [int(resultado[1]) for resultado in resultados][:5]
            documentosRecuperadosK10 = [int(resultado[1]) for resultado in resultados][:10]
            documentosRecuperadosRelevantes = [int(resultado[1]) for resultado in resultados][:len(documentosRelevantes)]

            relevantesRecuperados = [doc for doc in documentosRecuperados if doc in documentosRelevantes]
            relevantesRecuperadosK5 = [doc for doc in documentosRecuperadosK5 if doc in documentosRelevantes]
            relevantesRecuperadosK10 = [doc for doc in documentosRecuperadosK10 if doc in documentosRelevantes]
            relevantesRecuperadosRP = [doc for doc in documentosRecuperadosRelevantes if doc in documentosRelevantes]

            precisao = len(relevantesRecuperados) / len(documentosRecuperados)
            revocacao = len(relevantesRecuperados) / len(documentosRelevantes)
            
            # Gráfico de 11 pontos de precisão e revocação
            listaPrecisaoRevocacao.append((precisao, revocacao))

            # F1
            if(precisao+revocacao > 0):
                f1 = (2*precisao*revocacao) / (precisao+revocacao)
            else:
                f1 = 0
            listaF1.append(f1)

            # Precisao@5
            precisaoK5 = len(relevantesRecuperadosK5) / 5
            listaPrecisaoK5.append(precisaoK5)

            # Precisao@10
            precisaoK10 = len(relevantesRecuperadosK10) / 10
            listaPrecisaoK10.append(precisaoK10)

            # R-Precision
            r_precisao = len(relevantesRecuperadosRP) / len(documentosRelevantes)
            listaRPrecisao.append(r_precisao)

        # Gráfico de 11 pontos de precisão e revocação
        df = pd.DataFrame(listaPrecisaoRevocacao, columns=['Precisao', 'Revocacao'])
        df = df.sort_values(by='Revocacao',ascending=False)
        intervalosRevocacao = np.linspace(0, 1, 11)
        valoresPrecisao = []
        for intervalo in intervalosRevocacao:
            precisaoCorrespondente = df[df['Revocacao'] >= intervalo]['Precisao']
            if precisaoCorrespondente.empty:
                valoresPrecisao.append(0)
            else:
                valoresPrecisao.append(precisaoCorrespondente.max())
        plt.figure(figsize=(8, 6))
        plt.plot(intervalosRevocacao, valoresPrecisao, marker='o')
        plt.title('Gráfico de 11 Pontos de Precisão e Recall')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.savefig(f"AVALIA/11pontos.pdf")

        # F1
        f1 = sum(listaF1) / len(listaF1)
        print(f'F1 = {f1}')
              
        # Precisao@5
        precisaoK5 = sum(listaPrecisaoK5) / len(listaPrecisaoK5)
        print(f'Precisao@5 = {precisaoK5}')
              
        # Precisao@10
        precisaoK10 = sum(listaPrecisaoK10) / len(listaPrecisaoK10)
        print(f'Precisao@10 = {precisaoK10}')

        # R-Precision
        r_precisao = sum(listaRPrecisao) / len(listaRPrecisao)
        print(f'R-Precisao = {r_precisao}')
