from search import Problem

class ReflorestamentoProblem(Problem):
    def __init__(self, initial, base_pos, max_capacity):
        
        
        #initial: tupla ((x, y), sementes, frozenset(covas))
        #frozenset para não dar problema com os algoritmos de busca.
        super().__init__(initial)
        self.base_pos = base_pos
        self.max_capacity = max_capacity

    def actions(self, state):
        pos, sementes, covas = state
        possible_actions = []
        x, y = pos

        
        # Assumindo grid 10x10 
        if y > 0: possible_actions.append('Cima')
        if y < 9: possible_actions.append('Baixo')
        if x < 9: possible_actions.append('Direita')
        if x > 0: possible_actions.append('Esquerda')

        # Lógica de Plantar
        if pos in covas and sementes > 0:
            possible_actions.append('Plantar')

        # Lógica de Recarregar
        if pos == self.base_pos and sementes < self.max_capacity:
            possible_actions.append('Recarregar')

        return possible_actions

    def result(self, state, action):
        pos, sementes, covas = state
        x, y = pos

        #Parece repetição de código, mas diferente de quando aparece no ambiente, aqui o retorno é um estado.
        if action == 'Cima': return ((x, y - 1), sementes, covas)
        if action == 'Baixo':   return ((x, y + 1), sementes, covas)
        if action == 'Direita': return ((x + 1, y), sementes, covas)
        if action == 'Esquerda': return ((x - 1, y), sementes, covas)

        if action == 'Plantar':
            new_covas = set(covas)
            new_covas.remove(pos)
            return (pos, sementes - 1, frozenset(new_covas))

        if action == 'Recarregar':
            return (pos, self.max_capacity, covas)

        return state

    #Definição de objetivo
    def goal_test(self, state):
        return len(state[2]) == 0

    #Definição de custo
    def path_cost(self, c, state1, action, state2):
        pos, sementes, covas = state1
        
        # Custo Variável: Quanto mais sementes, maior o custo de movimento.
        if action in ['Cima', 'Baixo', 'Direita', 'Esquerda']:
            return c + (1 + 0.5 * sementes)
        
        if action == 'Plantar':
            return c + 2
        
        if action == 'Recarregar':
            return c + 1
            
        return c + 1

    #Definição da heurística: Distância de Manhattan 
    def h(self, node):
        pos, _, covas = node.state
        if not covas:
            return 0
        
        # Consideramos o custo mínimo, ou seja, nenhuma semente, para ser admissível.
        distancias = []
        for c in covas: 
            distancias.append((pos[0]-c[0]) + abs(pos[1]-c[1]))
            

        return min(distancias)
