tempo = 0  # tempo total da viagem em minutos
baldeacoes = 0  # numero de baldeacoes
dist = 0  # distancia total da viagem em km
linha_atual = 0  # linha atual

# define a estrutura para representar um no do grafo
class Node:
    def __init__(self, id, custo_acumulado, real_acumulado , g, h, linha, path):
        self.id = id  # identificador da estacao
        self.g = g * (60/40) # custo acumulado do caminho ate o no (transformando de km para min)
        self.h = h * (60/40) # estimativa heuristica do custo restante ate o destino (transformando de km para min)
        self.f = (g + h) * (60/40)  # f_cost = g_cost + h_cost ou seja o custo total (transformando de km para min)
        self.custo_acumulado = custo_acumulado + self.f # custo acumulado do caminho ate o no
        self.real_acumulado = real_acumulado + self.g # custo real acumulado do caminho ate o no
        self.linha = linha  # linha do metro
        self.path = path  # caminho percorrido ate o no

def read_adj_matrix(file_name, n, m):
    with open(file_name, 'r') as file:
        matrix = []
        for _ in range(n):
            row = list(map(float, file.readline().split()[:m]))
            matrix.append(row)
    return matrix

def verificar_baldeacao(linha_1, linha_2):
    if linha_1 != linha_2 and linha_1 != 0 and linha_2 != 0:
        return True
    else:
        return False

def verificar_linha(estacao_1, estacao_2, linhas_estacoes):
    """ 
    1.0 - linha vermelha
    2.0 - linha verde
    3.0 - linha azul
    4.0 - linha amarela
    verifica a linha da estacao 1 para a estacao 2"""
    
    linha = linhas_estacoes[estacao_1][estacao_2]
    return linha

def linha_correspondente(linha):
    if linha == 1.0:
        return "Vermelha"
    elif linha == 2.0:
        return "Verde"
    elif linha == 3.0:
        return "Azul"
    elif linha == 4.0:
        return "Amarela"

def a_star_metro(origem, LO, destino, LD):
    distancias_diretas = read_adj_matrix("metro\distancias_diretas.txt", 14, 14) # leitura da matriz de distancias diretas
    distancias_reais = read_adj_matrix("metro\distancias_reais.txt", 14, 14) # leitura da matriz de distancias reais
    linhas_estacoes = read_adj_matrix("metro\linhas_estacoes_copy.txt", 14, 14) # leitura da matriz de linhas das estacoes

    visitados = [False] * 14  # Vetor para verificar nos ja visitados
    
    # cria a fronteira
    fronteira = [] #lista que armazena os nos a serem expandidos

    # cria o no inicial
    #inicial = Node(origem, 0, distancias_reais[origem - 1][destino - 1] ,distancias_diretas[origem - 1][destino - 1], LO, [origem])
    inicial = Node(origem, 0, 0, 0 ,0, LO, [origem])

    # insere o no inicial na fronteira
    fronteira.append(inicial)

    global tempo, baldeacoes, dist, linha_atual
    
    passo = 1  # passo da arvore de busca

    while fronteira: # enquanto a fronteira nao estiver vazia

        # ordena a fronteira com base no custo acumulado
        fronteira.sort(key=lambda x: x.custo_acumulado)
        atual = fronteira.pop(0)      
        
        if atual.id == destino: # se chegou no destino

            linha_atual = LO
            for i in range(len(atual.path) - 1):
                estacao_atual = atual.path[i]
                estacao_vizinha = atual.path[i + 1]
                
                prox_linha = verificar_linha(estacao_atual - 1, estacao_vizinha - 1, linhas_estacoes)

                baldeacao = verificar_baldeacao(linha_atual,prox_linha)
                
                # print("Estacao atual: ", atual.path[i], "Linha: ", linha_atual)
                # print("Estacao vizinha: ", atual.path[i + 1], "Linha: ", prox_linha)
                # print("Baldeação: ", baldeacao)

                if baldeacao:
                    baldeacoes += 1
                
                linha_atual = prox_linha

            print("Caminho: ", "->".join(map(str, atual.path))) # imprime o caminho
            print("Numero de baldeacoes:  ", baldeacoes) # imprime o numero de baldeacoes
            print("Tempo: ", atual.real_acumulado,"min") # imprime o tempo total da viagem
            break

        else: # se nao chegou no destino
            
            if visitados[atual.id - 1]: # Ignora os nos ja visitados
                continue
            
            else: # Marca o no atual como visitado
                visitados[atual.id - 1] = True

            # encontrar os vizinhos
            for i in range(14):  # percorre todas as estacoes buscando vizinhos
                # se for vizinho
                linha_atual = atual.linha

                if linhas_estacoes[i][atual.id - 1] != 0 and not visitados[i]:
                    linha_vizinho = verificar_linha(atual.id - 1, i, linhas_estacoes)
                    baldeacao = verificar_baldeacao(linha_atual, linha_vizinho)
                    # print("Estacao atual: ", atual.id, "Linha: ", linha_atual)
                    # print("Estacao vizinha: ", i + 1, "Linha: ", linha_vizinho, "Baldeacao: ", baldeacao)
                    if baldeacao : 
                        Vizinho = Node(i + 1, atual.custo_acumulado, atual.real_acumulado, distancias_reais[i][atual.id - 1] + 2, distancias_diretas[i][destino - 1],
                                       linha_vizinho, atual.path + [i + 1])
                        fronteira.append(Vizinho)
                    else: 
                        Vizinho = Node(i + 1, atual.custo_acumulado, atual.real_acumulado, distancias_reais[i][atual.id - 1], distancias_diretas[i][destino - 1],
                                       linha_vizinho, atual.path + [i + 1])
                        fronteira.append(Vizinho)
        
        # printa o passo, o no atual e a fronteira
        print("Passo:", passo)
        linha_cor = linha_correspondente(atual.linha)
        print("\nNo atual: ")
        print(f"({atual.id}- {linha_cor}), Custo acumulado: {atual.custo_acumulado}")

        print("\nFronteiras")
        for node in fronteira:
            baldeacao = verificar_baldeacao(atual.linha, node.linha)
            linha_cor = linha_correspondente(node.linha)
            print(f"({node.id} - {linha_cor}), Custo acumulado: {node.custo_acumulado}, Baldeacao: {baldeacao}")
            print(f"g: {node.g}, h: {node.h}, f: {node.f} \n")
        
        passo += 1

        fronteira = [node for node in fronteira if not visitados[node.id - 1]]  # remove os nos ja visitados da fronteira

        print("-------------------------")

        

def main():
    print("\nInsira o numero da origem e do destino seguidos de suas respectinhas linhas de acordo com a tabela abaixo:")
    print("Linha vermelha: 1.0")
    print("Linha verde: 2.0")
    print("Linha azul: 3.0")
    print("Linha amarela: 4.0\n\n")

    origem,LO, destino, LD = map(int, input("\nInsira a origem e o destino (O LO D LD): ").split())
    a_star_metro(origem, LO, destino, LD)
    
if __name__ == "__main__":
    main()
