import sys
import os
# Bloco para fazer os imports funcionarem
# Pega o caminho absoluto da pasta atual (teste/)
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Sobe um nível para chegar na pasta raiz (robo_de_reflorestamento/)
diretorio_pai = os.path.dirname(diretorio_atual)

# Adiciona a pasta raiz ao caminho de busca do Python
if diretorio_pai not in sys.path:
    sys.path.append(diretorio_pai)
import csv
import random
import matplotlib.pyplot as plt
from problems.robo_de_reflorestamento_problem import ReflorestamentoProblem
import numpy as np
from search import (
    astar_search, breadth_first_graph_search, depth_first_graph_search,
    uniform_cost_search, greedy_best_first_graph_search
)

# Testa os algoritmos com cenários diversos do problema, registra a média de passos e custo de cada um e salva um gráfico de barras para comparativo.
def teste_automatico(qtd_testes=30):
    print("\nINICIANDO TESTES AUTOMÁTICOS\n")
    resultados = {}
    
    
    algoritmos = {
        "A*": lambda p: astar_search(p),
        "BFS": lambda p: breadth_first_graph_search(p),
        "DFS": lambda p: depth_first_graph_search(p),
        "UCS": lambda p: uniform_cost_search(p),
        "GBFS": lambda p: greedy_best_first_graph_search(p, f=lambda n: p.h(n))
    }
    
    # Loop aninhado que roda cada algoritmo qtd_testes vezes 
    for nome, func in algoritmos.items():
        passos = 0
        custos = 0
        for i in range(qtd_testes):
                WIDTH, HEIGHT = 10, 10
                BASE = (0, 0)
                MAX_CAP = 3
                COVAS = [(random.randint(0, 9), random.randint(0, 9)) for _ in range(5)]
                
                problem = ReflorestamentoProblem(
                    initial=(BASE, MAX_CAP, frozenset(COVAS)),
                    base_pos=BASE,
                    max_capacity=MAX_CAP,
                    largura=WIDTH,
                    altura=HEIGHT
                )

                try:
                    node = func(problem)
                    if node:
                        solution = node.solution()
                        passos += len(solution)
                        custos += node.path_cost
                        resultados[nome] = {
                            "passos": passos,
                            "custos": custos
                        }
                    
                    else:
                        resultados[nome] = {
                            "passos": 0,
                            "custos": 0
                        }
                except Exception as e:
                    print(f"Erro {nome}: {e}")
                    resultados[nome] = {
                            "passos": 0,
                            "custos": 0
                        }
                
                
                
        media_passos = resultados[nome].get("passos")/qtd_testes
        media_custos = resultados[nome].get("custos")/qtd_testes
        print(f"{nome} teve média de {media_passos} passos e teve média de {media_custos} custo\n")
        print("-" * 60)
        
        
    # Daqui pra baixo é pura lógica para plotar o gráfico    
    algoritmos = list(resultados.keys())
    
    medias_passos = [resultados[alg]["passos"] / qtd_testes for alg in algoritmos]
    medias_custos = [resultados[alg]["custos"] / qtd_testes for alg in algoritmos]
    
    with open('resultados_comparativos.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Media_Passos", "Media_Custo"])
        for i in range(len(algoritmos)):
            writer.writerow([algoritmos[i], medias_passos[i], medias_custos[i]])
    
    x = np.arange(len(algoritmos))
    largura = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 7))   
    
    rects1 = ax.bar(x - largura/2, medias_passos, largura, label='Média de Passos', color='#3498db')
    rects2 = ax.bar(x + largura/2, medias_custos, largura, label='Média de Custo', color='#e67e22')
    
    ax.set_ylabel('Valores Médios')
    ax.set_title(f'Desempenho por Algoritmo: Passos vs Custo ({qtd_testes} Testes)')
    ax.set_xticks(x)
    ax.set_xticklabels(algoritmos)
    ax.legend()
    
    # Função de rótulos  
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)        
            
    fig.tight_layout()
    plt.savefig('grafico_comparativo.png')
    plt.close(fig)

    
    
    
if __name__ == "__main__":
    teste_automatico()