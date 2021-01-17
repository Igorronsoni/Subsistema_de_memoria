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
# O trabalho prático desenvolvido tem como objetivo implementar uma politica de mapeamento, substituição e escrita de um subsistema de memória 

# -- Instruções especifica do projeto -- #
# Mapeamento: Associativo por Conjuntos (tamanho do conjunto especificado é 2)
# Escrita: em ambas
# Politica de substituição: LRU

# -- Detalhes sobre os dados -- #
# O tipo de dado escolhida para o armazenamento de dados será em hexadecimal e para os endereços usaremos binario

# -- Importação de modulos necessarios -- #
from MP import MP
from cache import Cache

# -- Bibliotecas externas -- #
from prettytable import PrettyTable

# -- Variáveis para a implementação -- #
# -- MP -- #
celulas_MP = 128            # Número de células na MP: 128
tamanho_bloco = 4           # Tamanho do bloco
tamanho_celula = 8          # Tamanho da célula em bits
# -- Cache -- #
linhas_cache = 8            # Número de linhas da cache
tamanho_conjunto = 2        # Tamanho do conjunto

# --- Funções --- #
# -- Função responsavel por imprimir o menu -- #
def Menu():
    print("\n+-------+----------------------------------+")
    print("| Opcao |               Menu               |")
    print("+-------+----------------------------------+")
    print("|   1   |    Ler o valor de um endereço    |")
    print("+-------+----------------------------------+")
    print("|   2   | Escrever um valor em um endereco |")
    print("+-------+----------------------------------+")
    print("|   3   |     Apresentar estatisticas      |")
    print("+-------+----------------------------------+")
    print("|   4   |          Mostrar Cache           |")
    print("+-------+----------------------------------+")
    print("|   5   |     Mostrar Memoria Principal    |")
    print("+-------+----------------------------------+")
    print("|   6   |               Sair               |")
    print("+-------+----------------------------------+")

# -- Imprime a saida da leitura/escrita da cache -- #
def saida(tupla):
    inCache  = 'Nao' if tupla[0] == 'miss' else 'Sim' # Salva o valor sim ou nao dependendo da saida miss ou hit
    
    # Altera o tamanho da string para dar certo na impressao
    blocoMP = str(bin(tupla[1]))
    if len(blocoMP) < 7:
        blocoMP = '0b' + ('0' * (5 - len(blocoMP[2:]))) + blocoMP[2:]

    # Altera o tamanho do conjunto
    conjunto = str(bin(tupla[2]))
    if len(conjunto) < 4:
        conjunto = '0b' + '0' + conjunto[2:]
    
    # Altera o tamanho do deslocamento
    deslocamento = str(bin(tupla[4]))
    if len(deslocamento) < 4:
        deslocamento = '0b' + '0' + deslocamento[2:]

    # Altera tamanho do valor
    valor = str(tupla[5])
    if len(valor) % 2 != 0:
        valor = ' ' + valor
    
    if len(tupla) > 6:
        antigo_valor = str(tupla[6])
        if len(antigo_valor) % 2 != 0:
            antigo_valor = ' ' + antigo_valor

        print("\n+---------------------------------------------------------------------------------------+")   
        print("|                                Retorno da Leitura da Cache                            |")
        print("+---------------------------------------------------------------------------------------+")
        print('| Estava na Cache | Bloco MP  | Conjunto | Quadro | Deslocamento | Valor Antigo | Valor |')
        print('+-----------------+-----------+----------+--------+--------------+--------------+-------+')
        print('|       {}       |  {}  |   {}   |  {}   |     {}     |     {}     | {}  |'.format(inCache, blocoMP,conjunto, bin(tupla[3]),deslocamento,antigo_valor, valor))
        print('+-----------------+-----------+----------+--------+--------------+--------------+-------+')
    
    else: 
        print("\n+------------------------------------------------------------------------+")   
        print("|                       Retorno da Leitura da Cache                      |")
        print("+------------------------------------------------------------------------+")
        print('| Estava na Cache | Bloco MP  | Conjunto | Quadro | Deslocamento | Valor |')
        print('+-----------------+-----------+----------+--------+--------------+-------+')
        print('|       {}       |  {}  |   {}   |  {}   |     {}     | {}  |'.format(inCache, blocoMP,conjunto, bin(tupla[3]),deslocamento,valor))
        print('+-----------------+-----------+----------+--------+--------------+-------+')

# -- Função de estatisticas -- #
def estatisticas(cache):

    # Pega o valor cheio para a geração das porcentagens
    totalRead = cache.estatisticasRead['hit'] + cache.estatisticasRead['miss']
    totalWrite = cache.estatisticasWrite['hit'] + cache.estatisticasWrite['miss']

    # Edita os espaços hit escrita
    hit_escrita = cache.estatisticasWrite['hit']
    hit_escrita_porcentagem = 100 * (cache.estatisticasWrite['hit'] / totalWrite) if totalWrite != 0 else '0' 

    # Edita os espaços hit leitura
    hit_leitura = cache.estatisticasRead['hit']
    hit_leitura_porcentagem = 100 * (cache.estatisticasRead['hit'] / totalRead) if totalRead != 0 else '0' 
    
    # Edita os espaços miss escrita
    miss_escrita = cache.estatisticasWrite['miss']
    miss_escrita_porcentagem = 100 * (cache.estatisticasWrite['miss'] / totalWrite) if totalWrite != 0 else '0' 

    # Edita os espaços miss leitura
    miss_leitura = cache.estatisticasRead['miss']
    miss_leitura_porcentagem = 100 * (cache.estatisticasRead['miss'] / totalRead) if totalRead != 0 else '0' 

    # Altera os valores de geral
    geral_hit = cache.estatisticasWrite['hit'] + cache.estatisticasRead['hit']
    geral_miss = cache.estatisticasWrite['miss'] + cache.estatisticasRead['miss']

    geral_hit_porcentagem = 100 * (geral_hit / (totalWrite + totalRead)) if (totalWrite + totalRead) != 0 else 0
    geral_miss_porcentagem = 100 * (geral_miss / (totalWrite + totalRead)) if (totalWrite + totalRead) != 0 else 0
    
    print()
    pt_estatistica = PrettyTable(['', 'Hit (abs)', 'Miss (abs)', 'Hit (%)', 'Miss (%)'])
    pt_estatistica.title = 'Estatisticas'
    pt_estatistica.add_row(['Leitura',hit_leitura, miss_leitura, hit_leitura_porcentagem, miss_leitura_porcentagem])
    pt_estatistica.add_row(['Escrita',hit_escrita,miss_escrita,hit_escrita_porcentagem,miss_escrita_porcentagem])
    pt_estatistica.add_row(['Geral',geral_hit,geral_miss,geral_hit_porcentagem,geral_miss_porcentagem])
    print(pt_estatistica)
    

# -- Variáveis de controle -- #
continua = True             # Controle de loop, True => mantendo a aplicação rodando
valor_maximo = '0b' + ('1' * tamanho_celula)  # Transforma o valor maximo em binario

# -- Inicia classes -- #
main_memory = MP(celulas_MP, tamanho_bloco, valor_maximo)
cache = Cache(main_memory, tamanho_bloco, valor_maximo, linhas_cache, tamanho_conjunto)

# Impressão da MP
main_memory.imprime()
# Impressão da Cache
cache.imprimir()

while continua:
    
    # -- Menu de seleção de opção -- #
    Menu() # Chama a função para a impressão das opções
    opcao = int(input("Opcao: "))
    
    # --- Opção 1 --- #
    # -- Ler o conteudo de um endereço da memoria especifico -- #
    if opcao == 1:
        print("OBS: O endereco pode ser escrito em binario ou decimal.\nCaso opte por binario, e necessario adicionar '0b' a frente do endereco")
        endereco = input("Digite um endereço entre 0 e 127 (0b0000000 - 0b1111111): ")
        tupla_de_retorno  = cache.read(endereco)

        cache.estatisticasRead[tupla_de_retorno[0]] += 1 # Atualiza o valor da estatistica

        saida(tupla_de_retorno) # Printa valores

    # --- Opção 2 --- #
    # -- Escrever em um determinado endereço de memória -- #
    elif opcao == 2:
        print("OBS: O endereco pode ser escrito em binario ou decimal.\nCaso opte por binario, e necessario adicionar '0b' a frente do endereco")
        endereco = input("Digite um endereço entre 0 e 127 (0b0000000 - 0b1111111): ")
        print("\nOBS: O valor pode ser escrito em hexadecimal ou decimal.\nCaso opte por hexadecimal, e necessario adicionar '0x' a frente do valor")
        valor =  input("Digite um valor entre 0 e 255 (0x00 - 0xFF): ")
        
        saida(cache.write(endereco,valor))
    
    # -- Opção 3 -- #
    # -- Apresenta as estatísticas de acertos e faltas (absolutos e percentuais) para as três situações: leitura, escrita e geral -- #
    elif opcao == 3:
        estatisticas(cache)

    # -- Opção 4 -- #
    # -- Imprime Cache -- #
    elif opcao == 4:
        cache.imprimir()
    
    # -- Opção 5 -- #
    # -- Imprime MP -- #
    elif opcao == 5:
        main_memory.imprime()
    
    # -- Opcao 6 -- #
    # -- Sair do programa -- #
    elif opcao == 6:
        continua = False
        print("Tenha um belo dia!!")
    
    # -- Opção invalida -- #
    else:
        print("Opção invalida. Tente novamente.")