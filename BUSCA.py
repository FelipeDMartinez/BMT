from collections import defaultdict
import pandas as pd
import numpy as np
import json

def buscador():
    with open('BUSCA.CFG', 'r') as CFG:
        for linha in CFG:
            if linha[0] == 'M':
                arquivo = (linha.split('=')[1])[1:-2]
                with open(arquivo, 'r') as f:
                    modelo = json.load(f)

                idf = modelo['idf']
                tfidf = pd.DataFrame(modelo['tfidf'])
                norma_euclidiana = modelo['norma_euclidiana']

            elif linha[0] == 'C':
                arquivo = (linha.split('=')[1])[1:-2]
                df_consulta = pd.read_csv(arquivo, sep=';', dtype={'QueryNumber': str})
                df_consulta['QueryText'] = df_consulta['QueryText'].apply(lambda x: eval(x))

            elif linha[0] == 'R':
                arquivo = (linha.split('=')[1])[1:-1]

                resultados = []
                for numero,texto in zip(df_consulta['QueryNumber'],df_consulta['QueryText']):
                    tfidf_query = pd.Series({t:v for t,v in idf.items() if t in texto})
                    
                    norma_euclidiana_query = np.sqrt((tfidf_query**2).sum())
                    
                    produto_escalar_query = tfidf.T[tfidf_query.index].multiply(tfidf_query, axis='columns').sum(axis=1)
                    
                    similaridade_query = produto_escalar_query.values.astype(float) / (norma_euclidiana_query * np.array(list(norma_euclidiana.values())))
                    similaridade_query =  pd.Series(similaridade_query, index=produto_escalar_query.index)
                    similaridade_query = similaridade_query.sort_values(ascending=False)
                    
                    resultados_query = []
                    for i, (documento, similaridade) in enumerate(similaridade_query.items(), start=1):
                        if(i > 15):
                            break
                        resultados_query.append((i, documento, similaridade))
                    
                    resultados.append((numero,resultados_query))

                df = pd.DataFrame(resultados, columns=['Query', 'Resultados'])
                df.to_csv(f'RESULT/{arquivo}.csv', index=False, sep=';')
