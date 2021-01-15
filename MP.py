import random

# --- Classe necessaria para a implementação da memoria principal --- #
class MP:

    def __init__(self, quantidade_celulas, tamanho_bloco, valor_maximo):
        self.memory = list() # Inicia a lista da memoria pricipal

        self.tamanho_bloco = tamanho_bloco # Tamanho de cada bloco
        self.quantidade_celulas = quantidade_celulas # Quantidade total de celulas

        # Gera valores aleatorios para inicialização da MP
        for x in range(quantidade_celulas):
            value = random.randint(0,int(valor_maximo,0))
            self.memory.append(hex(value))

    # --- Funções secundarias --- #
    # -- Retorna em qual bloco determinado endereço está contido -- #   
    def blockNumber(self, endereco):
        bloco = endereco // self.tamanho_bloco

        return bloco

    # -- Retorna qual o primeiro e ultimo endereço de determinado bloco -- #
    def dimensoesDoBloco(self,bloco):
        # Variaveis para o laço iterador
        contador_de_bloco = 0
        endereco = 0

        # Laço iterador para passar pelos endereços da MP e descobrir o primeiro endereço do bloco
        for endereco in range(0,len(self.memory),self.tamanho_bloco): # Vai do endereço 0 ate o final pulando a quantidade de celulas por bloco
            if bloco == contador_de_bloco:
                inicio = endereco
                break
            contador_de_bloco += 1 
        
        # Variaveis de inicio e final do bloco
        inicio = endereco 
        final = inicio + self.tamanho_bloco

        return inicio,final

    # --- Funções principais --- #
    # -- Imprime a MP -- #
    def imprime(self):
        quantidade_de_colunas = 5 # Quantidade de colunas a serem imprimidas
        
        # Laço para saber o número máximo de colunas possiveis 
        for divisor in range(5,0,-1):

            # Quando acha um modulo pelo numero, acha o maior divisor possivel
            if self.quantidade_celulas % divisor == 0:
                break
        
            quantidade_de_colunas -= 1

        # Calcula a quantidade de espaços necessarios para a impressao
        tamanho_dos_espacos = (((len('+-----------+--------+') * quantidade_de_colunas) - (len('Memoria Principal'))) // 2) - 1
        espacos = ' ' * tamanho_dos_espacos

        # Quantidade de ifens para a impressao
        tamanho_dos_ifens = (len('+-----------+--------+') * quantidade_de_colunas) - 3
        ifens = '-' * (tamanho_dos_ifens + 1)

        print('+' + ifens + '+')
        # Verifica se a quantidade de colunas é par, imprime um espaço a mais para dar certo as medidas
        if quantidade_de_colunas % 2 == 0:
            print('|' + espacos + 'Memoria Principal ' + espacos + '|')
        else:
            print('|' + espacos + 'Memoria Principal' + espacos + '|')

        # Imprime a divisão das colunas
        divisor = '+-----------+--------+' * quantidade_de_colunas
        rotulos = '|  Address  |  Value |' * quantidade_de_colunas
        print(divisor + '\n' + rotulos + '\n' + divisor)
        
        # Imprime os endereços e os valores
        quantidade_de_enderecos_por_coluna = self.quantidade_celulas // quantidade_de_colunas
        inicio = 0
        limite = (len(self.memory) - quantidade_de_enderecos_por_coluna) + 1
        # Laço que adiciona as linhas
        for inicio in range(quantidade_de_enderecos_por_coluna):

            # Laço que adiciona as colunas
            for address in range(inicio, limite, quantidade_de_enderecos_por_coluna): 

                value = str(self.memory[address])

                address = str(bin(address))
                
                # Verifica os tamanhos para a impressão
                if len(address) % 2 == 0:
                    address = address + ' '
                if len(value) % 2 != 0:
                    value = value + ' '

                # Realiza a formatação dos espaços em branco para o endereço
                calculo_espaco = (len('-----------') - len(address)) // 2
                espaco = ' ' * calculo_espaco
                address = espaco + address + espaco
                
                # Realiza a formatação dos espaços em branco para o valor
                calculo_espaco = (len('--------') - len(value)) // 2
                espaco = ' ' * calculo_espaco
                value = espaco + value + espaco

                print('|{}|{}|'.format(address,value), end='')
                # Converte para inteiro para ser somado
                address = int(address,0)

            # Incrementa as variaveis
            inicio += 1
            limite += 1
            print('\n' + divisor)
        
    # -- Escreve um bloco dentro da MP -- #
    def write(self, endereco, valor):
        self.memory[endereco] = valor

    # -- Le um bloco da MP -- #
    def read(self, endereco):
        # Altera o tipo da entrada para acessar a lista
        if "0b" in str(endereco):
            endereco = int(endereco,0)
        numeroBloco = self.blockNumber(endereco)
        inicio,final = self.dimensoesDoBloco(numeroBloco)
        return numeroBloco, self.memory[inicio:final].copy()
