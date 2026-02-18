<p align="center"> <strong>O problema: Robô de reflorestamento autônomo</strong></p> 

**Conceito:** Um robô opera em um terreno 2D (matriz) com o objetivo de plantar mudas em covas pelo terreno.

**Objetivo adicional:** O robô deve realizar o plantio de forma **autônoma e eficiente**, minimizando o custo total de suas ações e gerenciando corretamente seu estoque de sementes.

---

<p align="center"> <strong>1. Especificação formal:</strong></p>

**Representação dos estados:** Uma tupla `(posicao_robo, sementes_no_inventario, covas_restantes)`.

* ***posicao_robo:*** uma tupla `(x, y)` representando a posição do robô no grid.
* ***sementes_no_inventario:*** um número inteiro que decresce a cada plantio.
* ***covas_restantes:*** um conjunto de coordenadas de covas que ainda precisam ser plantadas.

**Exemplo de estado:**

```python
((2, 3), 3, {(4, 5), (1, 2)})
```

**Estado inicial:** O robô começa na posição `(0,0)`, inventário com `n` sementes e `m` pontos de plantio distribuídos.
A posição `(0,0)` também representa a **base de recarga**, onde o robô pode reabastecer suas sementes.

---

**Conjunto de ações:**

* `Mover` (Cima, Baixo, Direita, Esquerda)
* `Plantar` (se estiver sobre uma cova e tiver sementes)
* `Recarregar` (se estiver na base de recarga e tiver menos sementes que a capacidade máxima)

Essas ações permitem que o robô navegue pelo ambiente e complete seu objetivo.

---

**Modelo de transição (result(estado, acao)):**

* **Mover:** Atualiza a `posicao_robo` no grid.
* **Plantar:** Atualiza `sementes_no_inventario` e remove a posição atual de `covas_restantes`.
* **Recarregar:** Atualiza `sementes_no_inventario = MAX_CAPACIDADE`.

Cada ação gera um **novo estado**, que será utilizado pelos algoritmos de busca.

---

**Teste de objetivo (`goal_test`):**

Verifica se `covas_restantes` está vazio.
Ou seja, o objetivo é alcançado quando **todas as covas foram plantadas**.

---

**Custo de caminho (`path_cost`):**

* **Mover:** `1 + (0.5 * sementes_no_inventario)`
* **Plantar:** `2`
* **Recarregar:** `1`

Esse modelo de custo simula o fato de que carregar mais sementes aumenta o esforço do robô.

---

<p align="center"> <strong>2. Classificação do Ambiente</strong></p>

* **Determinístico:** O resultado de cada ação é previsível.
* **Totalmente observável:** A posição do agente, quantidade de sementes e localização das covas são conhecidas.
* **Estático:** O grid e as localizações das covas não mudam.
* **Discreto:** O ambiente é composto por células e ações bem definidas.
* **Agente único:** Apenas o robô opera no ambiente.
* **Sequencial:** Cada ação influencia diretamente o próximo estado do sistema.

---

<p align="center"> <strong>3. Programa de agente e arquitetura</strong></p>

* **Ambiente:** Gerencia o estado do mundo, atualizando-o a partir das ações tomadas pelo agente e mostrando visualmente a partir da função `render()`.
* **Programa de agente:** Herda de `SimpleProblemSolvingAgentProgram` e traça um plano de ação para atingir o objetivo. O agente utiliza **algoritmos de busca** para gerar a sequência de ações.

---

<p align="center"> <strong>4. Algoritmos de busca utilizados</strong></p>

O agente pode utilizar diversos algoritmos clássicos de busca para planejar suas ações:

1. **BFS (Breadth-First Search):**

   * Explora todos os nós no mesmo nível antes de avançar.
   * Garante encontrar o caminho com **menor número de passos**, mas não considera custo variável.

2. **DFS (Depth-First Search):**

   * Explora profundamente antes de retroceder.
   * Pode encontrar solução mais rápida em alguns casos, mas **não garante otimalidade** e pode ser ineficiente.

3. **UCS (Uniform-Cost Search):**

   * Expande o nó com menor custo acumulado (`path_cost`).
   * Garante encontrar o caminho de **custo mínimo**, ideal quando o custo de mover varia.

4. **GBFS (Greedy Best-First Search):**

   * Expande o nó com menor valor heurístico (`h(n)`) em relação ao objetivo.
   * Rápido, mas **não garante a solução ótima**, pois ignora custo acumulado.

5. **A* Search:**

   * Combina custo acumulado (`g(n)`) + heurística (`h(n)`).
   * Garante encontrar **caminho ótimo** se a heurística for admissível.
   * Heurística utilizada: **distância de Manhattan até a cova mais próxima**, assumindo que o robô não carrega sementes.

```python
h(n) = |x_robo - x_cova| + |y_robo - y_cova|
```

> A heurística é admissível porque assume o cenário mais otimista, nunca superestimando o custo real.

---

<p align="center"> <strong>5. Teste e execução do agente</strong></p>

* O agente é inicializado com a posição inicial `(0,0)` e estoque de sementes.
* O ambiente fornece percepções ao agente, que executa seu programa passo a passo até plantar todas as árvores.
* Durante a execução, são registradas:

  * Histórico de ações
  * Total de replans
  * Passos e custo acumulado


**Execução no terminal**

Para rodar a simulação principal do robô no ambiente:

```bash
python main.py
````

Para executar os testes automáticos do agente (simulando cenários diferentes):

```bash
python -m tests.test1
```

> Esses comandos permitem validar tanto a funcionalidade do agente quanto o desempenho dos algoritmos de busca.



