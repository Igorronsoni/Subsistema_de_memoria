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

    def write(self,quadro):
        self.linha = quadro

    # -- Responsavel pelo contador LRU -- #
    def contador(self, used):
        if used:
            self.contadorLRU = 0
        else:
            self.contadorLRU += 1

class Cache:
    
    def __init__(self, MP, tamanho_do_bloco, numero_maximo ,linhas_da_cache, linhas_conjunto):
        self.cache = list() # Inicia matriz da cache
        self.MP = MP # Para ter acesso as funções da MP

        for j in range( linhas_da_cache // linhas_conjunto ):
            lista = list()
            for i in range(linhas_conjunto):
                lista.append(Quadro(tamanho_do_bloco, numero_maximo))
            self.cache.append(lista)
    
    # --- Funções secundarias --- #
    # -- Função responsavel por inserir um quadro na cache -- #
    def inserirBloco(self, quadro, conjunto, rotulo, index):
        self.cache[conjunto][index].write(quadro)
        self.cache[conjunto][index].tag = rotulo
        self.cache[conjunto][index].valid = 1
        self.contadorLRU = 0

    # -- Atualiza todos os contadores para a substituição -- #
    def atualizaLRU(self, conjunto, index):
        for conj in range(len(self.cache)):
            for lista in range(len(self.cache[conj])):
                if conj != conjunto and lista != index:
                    self.cache[conj][lista].contadorLRU += 1

    # -- Decodifica o valor gerado na hora da pesquisa -- #
    def decodificador(self,codigo):
        if codigo == '01':
            return 0
        if codigo == '10':
            return 1
        else:
            return -1

    # --- Funções principais --- #
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

    # -- Responsavel pela leitura da cache -- #  
    def read(self, endereco):
        # Transforma em binario se for decimal
        if not '0b' in endereco:
            # Caso for um decimal faz a transformação para binario
            endereco = bin(int(endereco,0))
            
            # Verifica se o binario possui 7 bits
            if len(str(endereco)) < 9:
                valor = endereco[2:]
                zeros = '0' * (7 - len(valor))
                endereco = '0b' + zeros + valor

        rotulo = '0b' + str(int(str(endereco)[2:5])) # Pega qual o rotulo 
        conjunto = int('0b' + str(endereco)[5:7],0) # Pega o conjunto destinado
        deslocamento = int('0b' + str(endereco)[7:],0) # Deslocamento dentro do quadro

        # Valor para o codificador
        codigo = ''
        
        # Passa pelos quadros instanciados dentro do conjunto selecionado no endeço
        for quadro in self.cache[conjunto]:

            # Verifica se o endereço fornecido esta no conjunto 
            if quadro.tag == rotulo:
                codigo = '1' + codigo
            else:
                codigo = '0' + codigo
        
        # Verifica o bloco e o numero de onde o endereço esta na MP
        numeroBloco, bloco = self.MP.read(endereco)
        
        # Decodifica o codigo gerado na pesquisa
        index = self.decodificador(codigo)
        if index != -1: # Se o index for diferente de -1 então temos um indice de lista
            # Verifica se o quadro é valido dentro da cache
            if self.cache[conjunto][index].valid:
                self.atualizaLRU(conjunto,index) #Atualiza os contadores
                return 'hit', numeroBloco, conjunto, index, deslocamento 
            # Se não for, então deve-se procurar na MP o endereço para pegar o valor atual da posição 
    
        # Verifica qual das duas linhas deve sair 
        indice_a_ser_substituido = 0
        maiorLRU = 0 
        for index in range(len(self.cache[conjunto])):
            # Verifica se a linha é valida, se não for então o quadro deve ser trocado
            if not self.cache[conjunto][index].valid:
                indice_a_ser_substituido = index
                break
            # Verifica se ele deve ser substituido pela politica de substituição LRU
            if self.cache[conjunto][index].contadorLRU > maiorLRU:
                maiorLRU = self.cache[conjunto][index].contadorLRU
                indice_a_ser_substituido = index

        # Caso não esteja na cache ou o bit de validade for false, insere o quadro na cache
        self.inserirBloco(bloco, conjunto, rotulo, indice_a_ser_substituido)
        self.atualizaLRU(conjunto,index) # Atualiza os contadores
        return 'miss', numeroBloco, conjunto, index, deslocamento  

    def write(self):
        pass    
