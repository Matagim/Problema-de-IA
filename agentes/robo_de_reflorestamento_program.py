from agents import Agent
from search import astar_search
from problems.robo_de_reflorestamento_problem import ReflorestamentoProblem

class ReflorestamentoAgent(Agent):
    def __init__(self, initial_seeds, max_capacity, base_pos):
        super().__init__(self.program)
        
        self.seeds = initial_seeds
        self.max_capacity = max_capacity
        self.base_pos = base_pos
        self.plan = [] 
        self.location = base_pos 

    def program(self, percept):
        location, seeds, covas_restantes = percept

        # Se já temos um plano em andamento, executamos a próxima ação
        if self.plan:
            action = self.plan.pop(0)
            return action

        
        
        #  Definimos o estado atual para o problema
        initial_state = (location, seeds, covas_restantes)
        
        #  Criamos a instância do problema
        problem = ReflorestamentoProblem(
            initial=initial_state,
            base_pos=self.base_pos,
            max_capacity=self.max_capacity
        )

        #  Executamos a busca 
        print(f"Estado atual: {location} | Sementes: {seeds}. Calculando rota...") #print só pra ver como o programa tá indo.
        node = astar_search(problem)
        
        if node:
            #  A busca retorna uma solução e convertemos pra uma lista de ações
            self.plan = node.solution()
            
            # Se o plano não for vazio, retornamos a primeira ação (o mesmo que seria feito no início)
            if self.plan:
                next_action = self.plan.pop(0)
                return next_action
        
        return None