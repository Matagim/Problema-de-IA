<p align="center"> <strong>O problema: Robô de reflorestamento autônomo</strong></p>

**Conceito:** Um robô opera em um terreno 2D (matriz) com o objetivo e plantar mudas em covas pelo terreno.



<p align="center"> <strong>1. Especificação formal:</strong></p>


**Representação dos estados**: `Uma tupla (posicao_robo, sementes_no_inventario, covas_restantes).`. 
* ***posicao_robo:*** uma tupla (x,y)
* ***sementes_no_inventario:*** Um número inteiro que decresce a cada plantio.
* ***covas_restantes:*** um conjunto de coordenadas de covas que ainda precisam ser plantadas.

`--espaço para código--`


**Estado inicial:** O robô começa na posição ***(0,0)***, inventário com ***n*** sementes e ***m*** pontos de plantio distribuidos.

**Conjunto de ações:** `Mover (Cima, baixo, direita e esquerda)` , `Plantar` (se estiver sobre uma cova e tiver sementes) e `Recarregar` (se estiver na base de recarga e tiver menos sementes que a capacidade máxima).



**Modelo de transição (result(estado, acao)):** 

* ***Mover:*** Atualiza a posicao_robo no grid.
* ***Plantar:*** Retorna um estado com a quantidade de sementes atualizada e remove a posição atual de covas_restantes.
* ***Recarregar:*** Retorna um estado com sementes_no_inventario = MAX_CAPACIDADE.

`--espaço para código--`

**Teste de objetivo (goal_test):**  Verifica se *covas_restantes* está vazio.

**Custo de caminho (path_cost):**  
* ***Mover:*** 1 + (0.5 * sementes_no_inventario).
* ***Plantar:*** 2
* ***Recarregar:*** 1 

<p align="center"> <strong>2.Classificação do Ambiente</strong></p>


**Determinístico:** O resultado de cada ação de movimento ou plantio é fixo e previsível.

**Totalmente observável:** A posição do agente, quantidade de sementes e localização das covas são conhecidas.

**Estático:** O grid e as localizações das covas não mudam.

**Discreto:** O ambiente é composto por células e ações bem definidas por passo.

**Agente único:** Apenas o robô de reflorestamento opera no ambiente.

<p align="center"> <strong>3.Programa de agente e arquitetura.</strong></p>


**Ambiente:** Gerencia o estado do mundo, o atualizando a partir das ações tomadas pelo agente e mostra visualmente a partir da função ***render()***.

**Programa de agente:** Herda de ***SimpleProblemSolvingAgentProgram*** e para traçar um plano de ação e agir.

<p align="center"> <strong>4.Heurística.</strong></p>


A discussão para outros algoritmos será feita, porém o principal utilizado será o **A*** e a heurística será a distância de Manhattan até a cova mais próxima assumindo o cenário mais otimista, quando o robô não carrega semente alguma.

Essa heurística é admissível pois assume o cenário mais otimista possível dentro do contexto do problema, nunca superestimando o custo real de chegar à cova.
