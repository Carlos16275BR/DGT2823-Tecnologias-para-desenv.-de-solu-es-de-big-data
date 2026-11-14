import os
import sys

import numpy as np
import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CSV = os.path.join(PASTA, "dados.csv")
CAMINHO_SAIDA = os.path.join(PASTA, "saida.txt")


class Tee:
    def __init__(self, arquivo):
        self.tela = sys.stdout
        self.arquivo = arquivo

    def write(self, texto):
        self.tela.write(texto)
        self.arquivo.write(texto)

    def flush(self):
        self.tela.flush()
        self.arquivo.flush()


_arquivo_saida = open(CAMINHO_SAIDA, "w", encoding="utf-8")
sys.stdout = Tee(_arquivo_saida)


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def primeira_linha(erro):
    return str(erro).splitlines()[0]


pd.set_option("display.max_rows", 9999)

# ----------------------------------------------------------------------
# Passo 1 - Criar um novo arquivo/script
# ----------------------------------------------------------------------
# (arquivo/script criado: trabalho_pratico.py)

# ----------------------------------------------------------------------
# Passo 2 - Ler o conteúdo do CSV
# Separador ";", engine "python" e encoding utf-8.
# quotechar="'" remove as aspas simples que envolvem as datas no arquivo.
# ----------------------------------------------------------------------
leitura = pd.read_csv(CAMINHO_CSV, sep=";", engine="python", encoding="utf-8", quotechar="'")

# ----------------------------------------------------------------------
# Passo 3 - Atribuir os dados lidos a uma variável
# ----------------------------------------------------------------------
dados = leitura

# ----------------------------------------------------------------------
# Passo 4 - Verificar se os dados foram importados adequadamente
# ----------------------------------------------------------------------
titulo("Passo 1a - Informações gerais do conjunto de dados")
dados.info()

titulo("Passo 1b - Primeiras 5 linhas")
print(dados.head())
print("\nÚltimas 5 linhas")
print(dados.tail())

# ----------------------------------------------------------------------
# Passo 5 - Criar uma nova variável com uma cópia do conjunto original
# ----------------------------------------------------------------------
titulo("Passo 2 - Criar a variável 'limpo' com uma cópia dos dados")
limpo = dados.copy()
print("Variável 'limpo' criada como cópia de 'dados'.")

# ----------------------------------------------------------------------
# Passo 6 - Substituir nulos da coluna 'Calories' por 0
# ----------------------------------------------------------------------
titulo("Passo 3a - Substituir nulos de 'Calories' por 0")
limpo["Calories"] = limpo["Calories"].fillna(0)
print("Concluído.")

titulo("Passo 3b - Conjunto de dados após a substituição")
print(limpo.to_string())

# ----------------------------------------------------------------------
# Passo 7 - Substituir nulos da coluna 'Date' por '1900/01/01'
# ----------------------------------------------------------------------
titulo("Passo 4a - Substituir nulos de 'Date' por '1900/01/01'")
limpo["Date"] = limpo["Date"].fillna("1900/01/01")
print("Concluído.")

titulo("Passo 4b - Conjunto de dados após a substituição")
print(limpo.to_string())

# ----------------------------------------------------------------------
# Passo 8 - Transformar a coluna 'Date' em datetime
# ----------------------------------------------------------------------
titulo("Passo 5 - Tentativa de transformar 'Date' em datetime")
try:
    pd.to_datetime(limpo["Date"], format="%Y/%m/%d")
    print("Conversão executada sem erro.")
except Exception as erro:
    print("Erro encontrado:", primeira_linha(erro))

# ----------------------------------------------------------------------
# Passo 9 - Substituir '1900/01/01' por NaN e repetir a conversão
# ----------------------------------------------------------------------
titulo("Passo 6a - Substituir '1900/01/01' por NaN")
limpo["Date"] = limpo["Date"].replace("1900/01/01", np.nan)
print("Concluído.")

titulo("Passo 6b - Nova tentativa de transformar 'Date' em datetime")
try:
    pd.to_datetime(limpo["Date"], format="%Y/%m/%d")
    print("Conversão executada sem erro.")
except Exception as erro:
    print("Erro encontrado:", primeira_linha(erro))

titulo("Passo 6c - Conjunto de dados após as mudanças")
print(limpo.to_string())

# ----------------------------------------------------------------------
# Passo 10 - Corrigir o valor "20201226" (string em outro formato)
# Combina replace + to_datetime só para esse valor.
# ----------------------------------------------------------------------
titulo("Passo 7 - Corrigir o valor '20201226' da coluna 'Date'")
valor_corrigido = pd.to_datetime("20201226", format="%Y%m%d").strftime("%Y/%m/%d")
limpo["Date"] = limpo["Date"].replace("20201226", valor_corrigido)
print(f"'20201226' substituído por '{valor_corrigido}'.")

# ----------------------------------------------------------------------
# Passo 11 - Transformar toda a coluna 'Date' em datetime
# ----------------------------------------------------------------------
titulo("Passo 8 - Transformar toda a coluna 'Date' em datetime")
limpo["Date"] = pd.to_datetime(limpo["Date"], format="%Y/%m/%d")
print(limpo.dtypes)
print()
print(limpo.to_string())

# ----------------------------------------------------------------------
# Passo 12 - Remover registros com valores nulos (linha 22, coluna 'Date')
# ----------------------------------------------------------------------
titulo("Passo 9 - Remover os registros com valores nulos (linha 22)")
limpo = limpo.dropna(subset=["Date"])
print("Registro removido.")

# ----------------------------------------------------------------------
# Passo 13 - Imprimir o conjunto de dados final
# ----------------------------------------------------------------------
titulo("Passo 10 - Conjunto de dados final")
print(limpo.to_string())
print("\nNulos restantes por coluna:")
print(limpo.isnull().sum())
print(f"\nLinhas antes: {len(dados)} | linhas depois: {len(limpo)}")
limpo.info()

sys.stdout = sys.__stdout__
_arquivo_saida.close()