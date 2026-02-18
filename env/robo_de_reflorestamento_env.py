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


        # >>> ADICIONADO: guarda quantos passos o robô executou
        self.steps = 0


        # >>> ADICIONADO: guarda o custo total da solução
        self.total_cost = 0


        # >>> ADICIONADO: guarda histórico de ações
        self.history = []


        # >>> ADICIONADO: guarda estatísticas de eficiência por ação
        self.efficiency_history = []


        # >>> ADICIONADO: guarda posições visitadas pelo robô
        self.visited_positions = set()



    def percept(self, agent):

        #O que o agente vê: Posição, Sementes, Covas Restantes

        return (agent.location, agent.seeds, frozenset(self.covas))



    def execute_action(self, agent, action):

        #Altera o estado do mundo baseado na ação do agente

        x, y = agent.location


        # >>> ADICIONADO: salva histórico
        self.history.append(action)


        # >>> ADICIONADO: custo depende da quantidade de sementes
        movement_cost = 1 + 0.5 * agent.seeds



        if action == 'Cima' and y > 0:

            agent.location = (x, y - 1)


            # >>> ADICIONADO: soma custo
            self.total_cost += movement_cost



        elif action == 'Baixo' and y < self.altura - 1:

            agent.location = (x, y + 1)


            # >>> ADICIONADO
            self.total_cost += movement_cost



        elif action == 'Direita' and x < self.largura - 1:

            agent.location = (x + 1, y)


            # >>> ADICIONADO
            self.total_cost += movement_cost



        elif action == 'Esquerda' and x > 0:

            agent.location = (x - 1, y)


            # >>> ADICIONADO
            self.total_cost += movement_cost



        elif action == 'Plantar':

            if agent.location in self.covas and agent.seeds > 0:

                self.covas.remove(agent.location)

                self.planted.add(agent.location)

                agent.seeds -= 1


                # >>> ADICIONADO: custo plantar
                self.total_cost += 2


        elif action == 'Recarregar':

            if agent.location == self.base_pos:

                agent.seeds = self.max_capacity


                # >>> ADICIONADO: custo recarregar
                self.total_cost += 1



        # >>> ADICIONADO: conta passos
        self.steps += 1


        # >>> ADICIONADO: registra posição visitada
        self.visited_positions.add(agent.location)


        # >>> ADICIONADO: registra eficiência parcial
        if self.steps > 0:
            efficiency = len(self.planted) / self.steps
            self.efficiency_history.append(efficiency)





    def step(self):

        #Um passo de tempo

        if self.is_done():

            return


        for agent in self.agents:

            percepcao = self.percept(agent)

            acao = agent.program(percepcao)


            if acao:

                self.execute_action(agent, acao)





    def is_done(self):

        return len(self.covas) == 0



    # >>> ADICIONADO: método novo para mostrar estatísticas detalhadas
    def show_statistics(self):

        print("\n===========================")

        print("REFLORESTAMENTO FINALIZADO")

        print("===========================")

        print("Passos:", self.steps)

        print("Custo Total:", round(self.total_cost,2))

        print("Plantadas:", len(self.planted))

        print("Histórico:", self.history)

        print("Eficiência média:", round(sum(self.efficiency_history)/len(self.efficiency_history), 4) if self.efficiency_history else 0)

        print("Posições visitadas:", len(self.visited_positions))

        print("===========================")





    def render(self):

        # >>> CORRIGIDO: compatível com Windows e Linux
        os.system('cls' if os.name == 'nt' else 'clear')


        print(f"--- REFLORESTAMENTO ({self.largura}x{self.altura}) ---")


        # >>> ADICIONADO: mostra estatísticas durante execução
        print(f"Passos: {self.steps}")

        print(f"Custo: {round(self.total_cost,2)}")

        print(f"Covas restantes: {len(self.covas)}\n")


        print(f"Legenda: [R]=Robô | [B]=Base | [o]=Cova | [x]=Planta\n")



        for y in range(self.altura):

            line = ""

            for x in range(self.largura):

                pos = (x, y)


                agente_aqui = None

                for a in self.agents:

                    if a.location == pos:

                        agente_aqui = a

                        break


                if agente_aqui:

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

        time.sleep(0.4)
