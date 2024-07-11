from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
from lxml import etree
import pandas as pd
from collections import defaultdict
import xmltodict
import re
import warnings
warnings.filterwarnings("ignore")
nltk.download('punkt')
nltk.download('stopwords')

usar_porter_stemmer = False

def processamento(texto):
    # Remover pontuações usando expressão regular
    texto = re.sub(r'[^\w\s]', '', texto)

    # Tokenizar o texto em palavras
    palavras = word_tokenize(texto)

    # Carregar as stop words em inglês
    stop_words = set(stopwords.words('english'))

    # Filtrar palavras com mais de 3 caracteres e que não são stop words
    palavras_filtradas = [palavra.upper() for palavra in palavras if len(
        palavra) > 3 and palavra.lower() not in stop_words]

    if(usar_porter_stemmer):
        ps = PorterStemmer()
        palavras_filtradas = [ps.stem(palavra) for palavra in palavras_filtradas]

    return palavras_filtradas

def gerador_de_lista_invertida():
    global usar_porter_stemmer
    lista_xml = []
    with open('GLI.CFG', 'r') as CFG:
        for linha in CFG:
            if linha[0] == 'S':
                usar_porter_stemmer = True

            elif linha[0] == 'L':
                arquivo = (linha.split('=')[1])[1:-2]
                parser = etree.XMLParser(dtd_validation=True)
                tree = etree.parse(f'data/{arquivo}', parser)
                dicionario = xmltodict.parse(etree.tostring(tree))
                xml = dicionario['FILE']['RECORD']
                lista_xml.append(xml)

            elif linha[0] == 'E':
                arquivo = (linha.split('=')[1])[1:-1]
                lista_invertida = defaultdict(list)
                for xml in lista_xml:
                    df = pd.DataFrame(xml)
                    df['ABSTRACT'].fillna(df['EXTRACT'], inplace=True)
                    df = df[['RECORDNUM', 'ABSTRACT']]
                    df = df.dropna()
                    df['ABSTRACT'] = df['ABSTRACT'].apply(lambda x: str(x))
                    df['ABSTRACT'] = df['ABSTRACT'].apply(processamento)
                    for indice, linha in df.iterrows():
                        codigo = linha['RECORDNUM']
                        termos = linha['ABSTRACT']
                        for termo in termos:
                            if termo in lista_invertida:
                                lista_invertida[termo].append(codigo)
                            else:
                                lista_invertida[termo] = [codigo]
                            # lista_invertida[termo].append(codigo)

                    lista_invertida = dict(lista_invertida)
                    lista_invertida = dict(sorted(lista_invertida.items()))
                    df_lista_invertida = pd.DataFrame(
                        list(lista_invertida.items()), columns=['Termos', 'Documentos'])
                    df_lista_invertida.to_csv(
                        f'RESULT/{arquivo}.csv', index=False, header=False, sep=';')
