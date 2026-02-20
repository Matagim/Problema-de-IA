import sys
import os

# Pega o caminho absoluto da pasta atual (teste/)
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Sobe um nível para chegar na pasta raiz (robo_de_reflorestamento/)
diretorio_pai = os.path.dirname(diretorio_atual)

# Adiciona a pasta raiz ao caminho de busca do Python
if diretorio_pai not in sys.path:
    sys.path.append(diretorio_pai)
from agentes.robo_de_reflorestamento_program import ReflorestamentoAgent
from problems.robo_de_reflorestamento_problem import ReflorestamentoProblem
from search import (
    astar_search, breadth_first_graph_search, depth_first_graph_search,
    uniform_cost_search, greedy_best_first_graph_search
)


def test_robo_cenario_avancado():
    print("=====================================")
    print("INICIANDO TESTE 2: CENÁRIO AVANÇADO")
    print("=====================================")

    # Estado inicial
    initial_location = (0, 0)
    initial_seeds = 3   # força recargas durante o teste
    initial_covas = [(2, 1), (4, 4), (1, 3), (3, 0), (0, 4)]
    base = (0, 0)
    capacidade = 3  # capacidade máxima
    largura = 10
    altura = 10

    estado = (initial_location, initial_seeds, tuple(initial_covas))

    # Cria agente
    agent = ReflorestamentoAgent(
        initial_seeds=initial_seeds,
        max_capacity=capacidade,
        base_pos=base,
        largura = largura,
        altura = altura
    )

    print("Estado inicial:", estado)
    print()

    # Executa passos do agente
    location = initial_location
    seeds = initial_seeds
    covas_restantes = initial_covas.copy()

    for i in range(50):  # limite de passos maior para cenário mais complexo
        print(f"---------- PASSO {i} ----------")
        acao = agent.program(estado)
        print("Ação:", acao)

        if acao is None:
            print("Nenhuma ação disponível")
            break

        x, y = location

        # Movimento
        if acao == "Cima":
            location = (x, y - 1)
        elif acao == "Baixo":
            location = (x, y + 1)
        elif acao == "Esquerda":
            location = (x - 1, y)
        elif acao == "Direita":
            location = (x + 1, y)

        # Plantar
        elif acao == "Plantar":
            if seeds > 0 and covas_restantes:
                seeds -= 1
                covas_restantes = covas_restantes[1:]
                print("Plantou árvore!")

        # Recarregar
        elif acao == "Recarregar":
            seeds = capacidade
            print("Recarregou sementes!")

        estado = (location, seeds, tuple(covas_restantes))
        print("Novo estado:", estado)
        print()

        if not covas_restantes:
            print("=====================================")
            print("TODAS AS ÁRVORES FORAM PLANTADAS")
            print("TESTE 2 FINALIZADO COM SUCESSO")
            print("=====================================")
            break

    print()
    print("=====================================")
    print("HISTÓRICO DE AÇÕES")
    print(agent.action_history)
    print()
    print("TOTAL DE REPLANOS:", agent.replans)
    print("=====================================")
    print()

    # ====================================
    # TESTANDO PROBLEMA COM ALGUNS ALGORITMOS DE BUSCA
    # ====================================
    print("=====================================")
    print("TESTANDO PROBLEMA COM ALGUNS ALGORITMOS")
    print("=====================================")

    problem = ReflorestamentoProblem(
        initial=(initial_location, initial_seeds, frozenset(initial_covas)),
        base_pos=base,
        max_capacity=capacidade,
        largura=5,
        altura=5
    )

    algoritmos = {
        "BFS": lambda p: breadth_first_graph_search(p),
        "DFS": lambda p: depth_first_graph_search(p),
        "UCS": lambda p: uniform_cost_search(p),
        "GBFS": lambda p: greedy_best_first_graph_search(p, f=lambda n: p.h(n)),
        "A*": lambda p: astar_search(p)
    }

    for nome, func in algoritmos.items():
        try:
            node = func(problem)
            if node:
                sol = node.solution()
                print(f"{nome} encontrou solução ({len(sol)} passos):")
                for i, acao in enumerate(sol, 1):
                    print(f"{i:03d}. {acao}")
            else:
                print(f"{nome} não encontrou solução")
        except Exception as e:
            print(f"Erro {nome}: {e}")


if __name__ == "__main__":
    test_robo_cenario_avancado()
