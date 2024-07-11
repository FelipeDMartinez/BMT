import time
import json
import xmltodict
import numpy as np
import pandas as pd
from lxml import etree
from collections import defaultdict

def indexador():
    with open('INDEX.CFG', 'r') as CFG:
        for linha in CFG:
            if linha[0] == 'L':
                arquivo = (linha.split('=')[1])[1:-2]
                csv = pd.read_csv(arquivo,sep=';',header=None)
                csv.columns = ['palavras', 'lista_documentos']
                csv['lista_documentos'] = csv['lista_documentos'].apply(lambda x: eval(x))
            
            elif linha[0] == 'E':
                arquivo = (linha.split('=')[1])[1:-1]
                # matriz termo documento
                frequencia = defaultdict(lambda: defaultdict(int))
                for palavra, lista_documentos in zip(csv['palavras'], csv['lista_documentos']):
                    for documento in lista_documentos:
                        frequencia[documento][palavra] += 1
                matriz_termo_documento = pd.DataFrame(frequencia).fillna(0)
                matriz_termo_documento = matriz_termo_documento.applymap(int)
                matriz_termo_documento = matriz_termo_documento.sort_index()
                matriz_termo_documento = matriz_termo_documento.reindex(sorted(matriz_termo_documento.columns), axis=1)

                # tf
                tf = matriz_termo_documento.div(matriz_termo_documento.max(axis=0), axis=1)

                # idf
                idf = np.log(len(matriz_termo_documento.columns)/matriz_termo_documento.astype(bool).sum(axis=1))

                # tfidf
                tfidf = tf.mul(idf, axis=0)

                # norma euclidiana
                norma_euclidiana = np.sqrt((tfidf**2).sum())

                modelo = {'idf':idf.to_dict(),'tfidf':tfidf.to_dict(),'norma_euclidiana':norma_euclidiana.to_dict()}

                with open(f'RESULT/{arquivo}.json', 'w') as f:
                    json.dump(modelo, f)
