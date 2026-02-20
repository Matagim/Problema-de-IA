from env.robo_de_reflorestamento_env import ReflorestamentoEnv
from agentes.robo_de_reflorestamento_program import ReflorestamentoAgent
from problems.robo_de_reflorestamento_problem import ReflorestamentoProblem
from search import (
    astar_search, breadth_first_graph_search, depth_first_graph_search,
    uniform_cost_search, greedy_best_first_graph_search
)

import time
import random


def imprimir_comparacao_iterativa(resultados):
    print("\n===== COMPARAÇÃO DE ALGORITMOS (Iterativa) =====\n")
    for nome, dados in resultados.items():
        passos = dados['passos']
        custo = dados['custo']
        #acoes = dados['acoes']
        print(f"{nome} encontrou solução em {passos} passos e teve {custo} de custo ")

        """for i, acao in enumerate(acoes, 1):
            print(f"{i:03d}. {acao}")"""
        print("-" * 60)
    

def main():
    # CONFIGURAÇÃO do grid, base e capacidade de inventário
    WIDTH, HEIGHT = 10, 10
    BASE = (0, 0)
    MAX_CAP = 3
    
    # Coordenadas das covas (fixo ou aleatório)
    COVAS = [(2, 1), (8, 8), (1, 8), (9, 2), (5, 5)]
    # COVAS = [(random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)) for _ in range(5)]

    # Inicializa Ambiente e Agente
    env = ReflorestamentoEnv(WIDTH, HEIGHT, BASE, COVAS, MAX_CAP)
    robot = ReflorestamentoAgent(initial_seeds=MAX_CAP, max_capacity=MAX_CAP, base_pos=BASE, largura=WIDTH, altura=HEIGHT)
    env.add_thing(robot, location=BASE)

    print("Iniciando simulação...\n")
    print("CONFIGURAÇÕES:")
    print(f"Grid: {WIDTH}x{HEIGHT} | Base: {BASE} | Capacidade: {MAX_CAP} | Covas: {COVAS}\n")

    start_time = time.time()
    env.render()  # Estado inicial
    step_count = 0

    while not env.is_done():
        env.step()
        env.render()
        step_count += 1
        if step_count > 100:
            print("Limite de passos excedido.")
            break

    execution_time = time.time() - start_time
    print(f"\nMissão Cumprida em {step_count} passos!\n")

    # =============================
    # MÉTRICAS DO ROBÔ
    # =============================
    print("===== RELATÓRIO =====")
    print(f"Tempo execução: {execution_time:.4f} segundos")
    print(f"Posição final: {robot.location}")
    print(f"Sementes restantes: {robot.seeds}")
    print(f"Total de covas: {len(COVAS)}")
    eficiencia = len(COVAS) / step_count if step_count > 0 else 0
    print(f"Eficiência: {eficiencia:.4f}")


#Execute quantas vezes quiser em um cenário de covas randomicas
def covas_randomicas(qtd_testes=5):
    
    
    for i in range(qtd_testes):
        print(f"\nTeste {i+1}")
        WIDTH, HEIGHT = 10, 10
        BASE = (0, 0)
        MAX_CAP = 3
        COVAS = [(random.randint(0, 9), random.randint(0, 9)) for _ in range(5)]

        env = ReflorestamentoEnv(WIDTH, HEIGHT, BASE, COVAS, MAX_CAP)
        robot = ReflorestamentoAgent(initial_seeds=MAX_CAP, max_capacity=MAX_CAP, base_pos=BASE, largura=WIDTH, altura=HEIGHT)
        env.add_thing(robot, location=BASE)

        print("Iniciando simulação...\n")
        print("CONFIGURAÇÕES:")
        print(f"Grid: {WIDTH}x{HEIGHT} | Base: {BASE} | Capacidade: {MAX_CAP} | Covas: {COVAS}\n")

        start_time = time.time()
        env.render()  # Estado inicial
        step_count = 0
        

        while not env.is_done():
            env.step()
            env.render()
            step_count += 1
            if step_count > 100:
                print("Limite de passos excedido.")
                break

        execution_time = time.time() - start_time
        print(f"\nMissão Cumprida em {step_count} passos!\n")

        # =============================
        # MÉTRICAS DO ROBÔ
        # =============================
        print("===== RELATÓRIO =====")
        print(f"Tempo execução: {execution_time:.4f} segundos")
        print(f"Posição final: {robot.location}")
        print(f"Sementes restantes: {robot.seeds}")
        print(f"Total de covas: {len(COVAS)}")
        eficiencia = len(COVAS) / step_count if step_count > 0 else 0
        print(f"Eficiência: {eficiencia:.4f}")
   
        print("Preparando a próxima iteração...")
        time.sleep(5)

if __name__ == "__main__":
    #main()
    covas_randomicas()
    
