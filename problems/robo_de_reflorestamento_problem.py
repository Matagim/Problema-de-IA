from search import Problem

class ReflorestamentoProblem(Problem):
    def __init__(self, initial, base_pos, max_capacity, largura, altura):
        
        
        # initial: tupla ((x, y), sementes, frozenset(covas))
        # frozenset para não dar problema com os algoritmos de busca.
        super().__init__(initial)
        self.base_pos = base_pos
        self.max_capacity = max_capacity

        # >>> ADICIONADO: usar largura e altura do grid em vez de fixo 10x10
        self.largura = largura
        self.altura = altura

    def actions(self, state):
        pos, sementes, covas = state
        possible_actions = []
        x, y = pos

        
        # >>> MODIFICADO: antes era fixo 10x10, agora usa largura e altura
        if y > 0: possible_actions.append('Cima')
        if y < self.altura - 1: possible_actions.append('Baixo')      # <<< ALTERADO
        if x < self.largura - 1: possible_actions.append('Direita')   # <<< ALTERADO
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

        # Parece repetição de código, mas diferente de quando aparece no ambiente,
        # aqui o retorno é um estado.

        if action == 'Cima':
            return ((x, y - 1), sementes, covas)

        if action == 'Baixo':
            return ((x, y + 1), sementes, covas)

        if action == 'Direita':
            return ((x + 1, y), sementes, covas)

        if action == 'Esquerda':
            return ((x - 1, y), sementes, covas)

        if action == 'Plantar':

            # >>> ADICIONADO: criar nova lista de covas corretamente
            new_covas = set(covas)
            new_covas.remove(pos)

            return (pos, sementes - 1, frozenset(new_covas))

        if action == 'Recarregar':

            # >>> ADICIONADO: volta sementes ao máximo
            return (pos, self.max_capacity, covas)

        return state

    # Definição de objetivo
    def goal_test(self, state):

        # >>> ADICIONADO: objetivo é quando não há covas
        return len(state[2]) == 0

    # Definição de custo
    def path_cost(self, c, state1, action, state2):

        pos, sementes, covas = state1
        
        # Custo Variável: Quanto mais sementes, maior o custo de movimento.
        if action in ['Cima', 'Baixo', 'Direita', 'Esquerda']:

            # >>> ADICIONADO: custo depende da quantidade de sementes
            return c + (1 + 0.5 * sementes)
        
        if action == 'Plantar':

            # >>> ADICIONADO: custo fixo plantar
            return c + 2
        
        if action == 'Recarregar':

            # >>> ADICIONADO: custo recarregar
            return c + 1
            
        return c + 1


    # Definição da heurística: Distância de Manhattan
    def h(self, node):

        pos, _, covas = node.state

        # >>> ADICIONADO: se não há covas, custo 0
        if not covas:
            return 0
        
        distancias = []

        for c in covas:

            # >>> CORRIGIDO: fórmula correta Manhattan
            dist = abs(pos[0] - c[0]) + abs(pos[1] - c[1])

            distancias.append(dist)

        # >>> ADICIONADO: retorna menor distância
        return min(distancias)


    # >>> ADICIONADO: suporte para BFS
    def bfs(self, node):

        from search import breadth_first_search
        return breadth_first_search(self)

    # >>> ADICIONADO: suporte para DFS
    def dfs(self, node):

        from search import depth_first_search
        return depth_first_search(self)

    # >>> ADICIONADO: suporte para UCS
    def ucs(self, node):

        from search import uniform_cost_search
        return uniform_cost_search(self)

    # >>> ADICIONADO: suporte para GBFS (Greedy Best First)
    def gbfs(self, node):

        from search import greedy_best_first_search
        return greedy_best_first_search(self)

    # >>> ADICIONADO: suporte para A*
    def astar(self, node):

        from search import astar_search
        return astar_search(self)
