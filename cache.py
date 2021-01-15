import random

class Quadro:

    def __init__(self, tamanho_do_bloco, numero_maximo):
        self.linha = list() # Lista onde os valores irão ficar
        self.valid = 0 # Bit de validade
        self.tag = bin(random.randint(0,7)) # Tag do endereço
        self.contadorLRU = 0 # Contador LRU

        # Variaveis de estatisticas
        self.hitWrite = 0
        self.missWrite = 0
        self.hitRead = 0
        self.missRead = 0

        for f in range(tamanho_do_bloco):
            self.linha.append(hex(random.randint(0,int(str(numero_maximo),0))))
    
    # -- Responsavel pelo retorno dos valor -- #
    def read(self):
        return [self.valid, self.tag, self.linha]

    # -- Responsavel pelo contador LRU -- #
    def contador(self, used):
        if used:
            self.contadorLRU = 0
        else:
            self.contadorLRU += 1

class Cache:
    
    def __init__(self, MP, tamanho_do_bloco, numero_maximo ,linhas_da_cache, linhas_conjunto):
        self.cache = list() # Inicia matriz da cache

        for j in range( linhas_da_cache // linhas_conjunto ):
            lista = list()
            for i in range(linhas_conjunto):
                lista.append(Quadro(tamanho_do_bloco, numero_maximo))
            self.cache.append(lista)
    
    # --- Funções secundarias --- #
    # -- Função responsavel por inserir um quadro na cache -- #
    def insert(self, quadro, conjunto):
        
        # Laço verifica qual quadro deve sair
        linha = 0
        contador = 0
        for quadro in self.cache[conjunto]:
            if not quadro.valid:
                break
            if quadro.contadorLRU > contador:
                break
            
            linha += 1

    # -- Imprime a memória cache dentro de linhas -- #
    def imprimir(self):
        print('\n+---------------------------------------------------+')
        print('|                    Memoria Cache                  |')
        print('+---------------------------------------------------+')
        print('| Block | Valid |  Tag  |          Values           |')
        print('+---------------------------------------------------+')
        
        # Passa pelos conjuntos
        for conjunto in range(len(self.cache)):
            
            # Faz o calculo de espaço a serem implementados na impressão do conjunto
            conjunto_bin = str(bin(conjunto))
            espaco = (7 - len(conjunto_bin)) // 2
            espaco = ' ' * espaco
            # Verifica se o tamanho é par então deve-se somar mais um espaço
            if len(conjunto_bin) % 2 == 0:
                conjunto_bin += ' '
            conjunto_bin = espaco + conjunto_bin + espaco
            print('|{}|'.format(conjunto_bin),end='')
            
            # Variavel de controle de quebra de linha
            rodadas = 1

            # Passa pelas listas dos conjuntos
            for linha in self.cache[conjunto]:

                retorno_MP = linha.read() # Pega os dados de uma linha especifica
                
                # Imprime o bit de validade
                espaco = ' ' * 3 # O tamanho do bit é sempre 1 e o espaço é sempre 7 entao temos que 7 - 1 // 2
                valid = espaco + str(retorno_MP[0]) + espaco
                print('{}|'.format(valid),end='')

                # Imprime tag da lista
                tag = str(retorno_MP[1])
                # Verifica se o tamanho é par então deve-se somar mais um espaço
                if len(tag) % 2 == 0:
                    tag += ' '
                
                espaco = (7 - len(tag)) // 2
                espaco = ' ' * espaco
                tag = espaco + tag + espaco
                print('{}|'.format(tag),end='')

                # Passa pelos valores das listas
                for value in retorno_MP[2]:
                    # Realiza os calculos de soma de espaços
                    value = str(value)
                    espaco = (7 - len(value)) // 2
                    espaco = ' ' * espaco
                    
                    # Verifica se o tamanho é par então deve-se somar mais um espaço
                    if len(value) % 2 != 0:
                       value = value[:-1]

                    value = espaco + value + espaco

                    print('{}|'.format(value),end='')
                
                # Somente imprime se for a primeira lista a ser printada
                if rodadas == 1:
                    espaco_conjunto = ' ' * len(conjunto_bin)
                    print('\n+       +-------+-------+---------------------------+\n|{}|'.format(espaco_conjunto),end='')
                else:
                    print('\n+-------+-------+-------+---------------------------+')

                rodadas += 1

    # --- Funções principais --- #
    # -- Responsavel pela leitura da cache -- #  
    def read(self, endereco):
        # Transforma em decimal se for binario
        if '0b' in endereco:
            conjunto = int('0b' + str(endereco)[5:7],0)
        
        rotulo = str(endereco)[2:5]

        # Passa pelos quadros instanciados dentro do conjunto selecionado no endeço
        for quadro in self.cache[conjunto]:
        
            # Verifica se o endereço fornecido esta no conjunto 
            if quadro.tag == rotulo:
        
                # Caso o endereço esta dentro da cache verifica se ele é valido
                if quadro.valid:
        
                    self.hitRead += 1
        
                    # Retorna o quadro
                    return quadro.read(), conjunto
        
        self.missRead += 1
        
        # Caso não esteja na cache ou o bit de validade for false, insere o quadro na cache
        self.insert(MP.read(endereco), conjunto)
    
    def write(self):
        pass
