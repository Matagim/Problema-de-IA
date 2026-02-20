from agents import Agent
# >>> ADICIONADO: importando outros algoritmos de busca
from search import astar_search, breadth_first_graph_search, depth_first_graph_search, uniform_cost_search, greedy_best_first_graph_search
from problems.robo_de_reflorestamento_problem import ReflorestamentoProblem


class ReflorestamentoAgent(Agent):
    # >>> Adicionei altura e largura para suportar grid de qualquer tamanho.
    # >>> ADICIONADO: parâmetro search_algo para permitir escolher o algoritmo
    def __init__(self, initial_seeds, max_capacity, base_pos, altura, largura, search_algo=astar_search):

        super().__init__(self.program)

        self.seeds = initial_seeds

        self.max_capacity = max_capacity

        self.base_pos = base_pos

        self.plan = []

        self.location = base_pos
        
        self.altura = altura
        
        self.largura = largura
        
        


        # >>> ADICIONADO: guarda histórico de ações executadas
        self.action_history = []


        # >>> ADICIONADO: guarda quantos planos já foram gerados
        self.replans = 0


        # >>> ADICIONADO: guarda último estado para evitar recalcular plano sem necessidade
        self.last_state = None

        # >>> ADICIONADO: guarda algoritmo de busca escolhido
        self.search_algo = search_algo


    def program(self, percept):

        location, seeds, covas_restantes = percept


        # >>> ADICIONADO: atualiza posição e sementes internas
        self.location = location
        self.seeds = seeds


        # >>> ADICIONADO: cria estado atual completo
        current_state = (location, seeds, covas_restantes)


        # >>> ADICIONADO: evita recalcular plano se estado não mudou
        if self.last_state == current_state and self.plan:

            action = self.plan.pop(0)

            self.action_history.append(action)  # >>> ADICIONADO

            return action


        # Se já temos um plano em andamento, executamos a próxima ação
        if self.plan:

            action = self.plan.pop(0)

            self.action_history.append(action)  # >>> ADICIONADO

            return action


        # Definimos o estado atual para o problema
        initial_state = current_state


        # Criamos a instância do problema
        problem = ReflorestamentoProblem(

            initial=initial_state,

            base_pos=self.base_pos,

            max_capacity=self.max_capacity,

            largura=self.largura,   # >>> ADICIONADO: suporte ao tamanho do grid

            altura=self.largura     # >>> ADICIONADO: suporte ao tamanho do grid

        )


        print(f"Estado atual: {location} | Sementes: {seeds}. Calculando rota...")


        # >>> ADICIONADO: conta quantas vezes recalculou plano
        self.replans += 1


        # >>> MODIFICADO: usa o algoritmo definido no parâmetro search_algo
        node = self.search_algo(problem)


        if node:

            self.plan = node.solution()


            # >>> ADICIONADO: salva estado atual
            self.last_state = current_state


            print("Plano encontrado:", self.plan)  # >>> ADICIONADO


            if self.plan:

                next_action = self.plan.pop(0)

                self.action_history.append(next_action)  # >>> ADICIONADO

                return next_action


        # >>> ADICIONADO: mensagem de erro se não encontrou plano
        print("Nenhum plano encontrado!")


        return None
