# --- Detalhes do trabalho pratico desenvolvido --- #

# -- Autores -- #
# Nome: Igor Ronsoni
# Matrícula: 1811100032
# E-mail: igorandrey@yahoo.com.br / igor.ronsoni2000@gmail.com
#
# Nome: Giovane Gonçalves da Silva
# Matrícula: 1811100005
# E-mail: giovanegsilva@outlook.com

# -- Resumo -- #
# O trabalho prático desenvolvido tem como objetivo implementar uma politica de mapeamento, substituição e escrita de um sistema de memória 

# -- Instruções especifica do projeto -- #
# Mapeamento: Associativo por Conjuntos (tamanho do conjunto especificado é 2)
# Escrita: em ambas
# Politica de substituição: LRU

# -- Detalhes sobre os dados -- #
# O tipo de dado escolhida para o armazenamento de dados será em binario

# -- Importação de modulos necessarios -- #
from MP import MP

# -- Variáveis para a implementação -- #
# -- MP -- #
celulas_MP = 128            # Número de células na MP: 128
tamanho_bloco = 4           # Tamanho do bloco
# -- Cache -- #
linhas_cache = 8            # Número de linhas da cache
tamanho_celula = 8          # Tamanho da celular em bits
tamanho_conjunto = 2        # Tamanho do conjunto

# -- Variáveis de controle -- #
continua = True             # Controle de loop, True => mantendo a aplicação rodando

# --- Funções --- #
# -- Função responsavel por imprimir o menu -- #
def Menu():
    print("+-------+----------------------------------+")
    print("| Opcao |               Menu               |")
    print("+-------+----------------------------------+")
    print("|   1   |    Ler o valor de um endereço    |")
    print("+-------+----------------------------------+")
    print("|   2   | Escrever um valor em um endereco |")
    print("+-------+----------------------------------+")
    print("|   3   |     Apresentar estatisticas      |")
    print("+-------+----------------------------------+")
    print("|   4   |               Sair               |")
    print("+-------+----------------------------------+")

# -- Inicia classes -- #
main_memory = MP(celulas_MP,tamanho_bloco)

while continua:
    # Impressão da MP
    main_memory.imprime()

    # -- Menu de seleção de opção -- #
    #Menu() # Chama a função para a impressão das opções
    opcao = int(input("Opcao: "))
    
    # --- Opção 1 --- #
    # -- Ler o conteudo de um endereço da memoria especifico -- #
    if opcao == 1:
        break

    # --- Opção 2 --- #
    # -- Escrever em um determinado endereço de memória -- #
    elif opcao == 2:
        break

    # -- Opção 3 -- #
    # -- Apresenta as estatísticas de acertos e faltas (absolutos e percentuais) para as três situações: leitura, escrita e geral -- #
    elif opcao == 3:
        break

    # -- Opção 4 -- #
    # -- Saida do programa -- #
    else:
        break 