import time
import os
from agents import Environment

class ReflorestamentoEnv(Environment):
    def __init__(self, largura, altura, base_pos, cova_coords, max_capacity):
        super().__init__()
        self.largura = largura #largura do grid
        self.altura = altura #altura do grid
        self.base_pos = base_pos
        self.covas = set(cova_coords)
        self.planted = set() # Histórico do que foi plantado
        self.max_capacity = max_capacity

    def percept(self, agent):
        #O que o agente vê: Posição, Sementes, Covas Restantes
        return (agent.location, agent.seeds, frozenset(self.covas))

    def execute_action(self, agent, action):
        #Altera o estado do mundo baseado na ação do agente
        x, y = agent.location

        if action == 'Cima' and y > 0:
            agent.location = (x, y - 1)
        elif action == 'Baixo' and y < self.altura - 1:
            agent.location = (x, y + 1)
        elif action == 'Direita' and x < self.largura - 1:
            agent.location = (x + 1, y)
        elif action == 'Esquerda' and x > 0:
            agent.location = (x - 1, y)
        
        elif action == 'Plantar':
            if agent.location in self.covas and agent.seeds > 0:
                self.covas.remove(agent.location)
                self.planted.add(agent.location)
                agent.seeds -= 1
        
        elif action == 'Recarregar':
            if agent.location == self.base_pos:
                agent.seeds = self.max_capacity

    def step(self):
        #Um passo de tempo
        if self.is_done():
            return

        #Solicita a ação ao Agente 
        #OBS: Essa parte dá pra simplificar, já que só tem um agente, mas... Dá na mesma.
        for agent in self.agents:
            percepcao = self.percept(agent)
            acao = agent.program(percepcao)
            
            # Executa a ação
            if acao:
                self.execute_action(agent, acao)

    #Verifica se acabou
    def is_done(self):
        return len(self.covas) == 0

    #Renderiza a visualização no terminal
    def render(self):
        os.system('clear') 
        
        print(f"--- REFLORESTAMENTO ({self.largura}x{self.altura}) ---")
        print(f"Legenda: [R]=Robô | [B]=Base | [o]=Cova | [x]=Planta\n")

        #Loop aninhado pra montar o grid passando pelas posições e desenhando.
        for y in range(self.altura):
            line = ""
            for x in range(self.largura):
                pos = (x, y)
                
                # Verifica se o robô está aqui
                agente_aqui = None
                for a in self.agents:
                    if a.location == pos:
                        agente_aqui = a
                        break
                
                if agente_aqui:
                    # Mostra R + qtd sementes (ex: R3, R0)
                    line += f"R{agente_aqui.seeds} "
                elif pos == self.base_pos:
                    line += "[B]"
                elif pos in self.covas:
                    line += "[o]"
                elif pos in self.planted:
                    line += "[x]"
                else:
                    line += " . "
            print(line)
        print("-" * 30)
        time.sleep(0.4) # Velocidade da animação