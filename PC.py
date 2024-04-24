from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from lxml import etree
import pandas as pd
import xmltodict
import re
import warnings
warnings.filterwarnings("ignore")
nltk.download('punkt')
nltk.download('stopwords')


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

    return palavras_filtradas


def calcula_votos(s):
    # Inicializar contadores para cada dígito (0, 1, 2)
    count_0 = count_1 = count_2 = 0

    # Contar a frequência de cada dígito na string
    for digit in s:
        if digit == '0':
            count_0 += 1
        elif digit == '1':
            count_1 += 1
        elif digit == '2':
            count_2 += 1
    # Determinar o número mais frequente (com regra de desempate)
    if count_2 >= count_1 and count_2 >= count_0:
        return '2'
    elif count_1 >= count_0 and count_1 >= count_2:
        return '1'
    else:
        return '0'


def processador_de_consultas():
    with open('PC.CFG', 'r') as CFG:
        for linha in CFG:
            if linha[0] == 'L':
                arquivo = (linha.split('=')[1])[1:-2]
                parser = etree.XMLParser(dtd_validation=True)

                tree = etree.parse(f'data/{arquivo}', parser)
                dict = xmltodict.parse(etree.tostring(tree))
                xml = dict['FILEQUERY']['QUERY']

            elif linha[0] == 'C':
                arquivo = (linha.split('=')[1])[1:-2]
                df = pd.DataFrame(xml)
                df = df[['QueryNumber', 'QueryText']]

                df['QueryText'] = df['QueryText'].apply(processamento)

                df.to_csv(f'RESULT/{arquivo}.csv', index=False, sep=';')

            elif linha[0] == 'E':
                arquivo = (linha.split('=')[1])[1:-2]
                df = pd.DataFrame(xml)
                df = df[['QueryNumber', 'Records']]
                df['Records'] = df['Records'].apply(lambda x: x['Item'])
                df = df.explode('Records')
                df['DocVotes'] = df['Records'].apply(lambda x: x['@score'])

                df['DocVotes'] = df['DocVotes'].apply(calcula_votos)
                df['DocNumber'] = df['Records'].apply(lambda x: x['#text'])
                df.drop(columns=['Records'], inplace=True)
                df.to_csv(f'RESULT/{arquivo}.csv', index=False, sep=';')
