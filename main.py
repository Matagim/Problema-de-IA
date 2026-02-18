from env.robo_de_reflorestamento_env import ReflorestamentoEnv
from agentes.robo_de_reflorestamento_program import ReflorestamentoAgent

def main():
    #CONFIGURAÇÃO do grid, base e capacidade de inventário
    WIDTH, HEIGHT = 10, 10
    BASE = (0, 0)
    MAX_CAP = 3
    
    # Coordenadas das covas (dá pra deixar aleatório depois para os testes)
    COVAS = [(2, 1), (8, 8), (1, 8), (9, 2), (5, 5)]

    # Inicializa Ambiente
    env = ReflorestamentoEnv(WIDTH, HEIGHT, BASE, COVAS, MAX_CAP)

    # Inicializa Agente
    robot = ReflorestamentoAgent(initial_seeds=MAX_CAP, max_capacity=MAX_CAP, base_pos=BASE)

    # Adiciona Agente ao Ambiente
    # O método add_thing adiciona à lista self.agents do ambiente
    env.add_thing(robot, location=BASE)

    # Loop de Simulação
    print("Iniciando simulação...")
    env.render() # Mostra estado inicial

    step_count = 0
    while not env.is_done():
        env.step()    # Agente Pensa -> Age -> Ambiente Atualiza
        env.render()  # Visualiza
        step_count += 1
        
        # Trava de segurança para loops infinitos em testes (aumentar de acordo com o tamanho do grid e passos necessários)
        if step_count > 100:
            print("Limite de passos excedido.")
            break
    
    #Informa quantos passos foram necessários para completar o trajeto
    #OBS: Outras informações podem ser imprimidas caso necessário para comparar os algoritmos depois.
    print(f"\nMissão Cumprida em {step_count} passos!")

if __name__ == "__main__":
    main()