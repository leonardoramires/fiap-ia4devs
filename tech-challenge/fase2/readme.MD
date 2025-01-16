# Tech Challenge - Pós-Tech SOAT - FIAP - Fase 2

Alunos:

* André Mattos - RM358905
* Aurelio Thomasi Jr - RM358104
* Leonardo Ramires - RM358190
* Lucas Arruda - RM358628
* Pedro Marins - RM356883

## Evidências do projeto
- [Link para o repositório](https://github.com/leonardoramires/fiap-ia4devs)
- [Link para o vídeo do projeto]()

## Definição do Problema
O problema consiste em alocar ordens de serviço (OS) de manutenção para operadores de forma otimizada, considerando as habilidades necessárias para cada ordem e as habilidades dos operadores disponíveis. O objetivo é minimizar o tempo de execução das ordens, evitar horas extras desnecessárias e garantir que as ordens sejam atendidas dentro do prazo estipulado.


## Objetivos
Alocar ordens de serviço de forma eficiente, maximizando a compatibilidade entre as habilidades dos operadores e as habilidades necessárias para as ordens.
Minimizar o número de horas extras trabalhadas pelos operadores.
Garantir que as ordens de maior prioridade sejam atendidas dentro do prazo.


## Melhorias implementadas durante a execução dos testes

1. Reajuste nas funções de aptidão:
    - Adição de pesos considerando a prioridade da OS para tornar proporcional o impacto das penalidades.
    - Inclusão de penalização por horas extras realizadas, ajustando a penalização com base na prioridade da ordem.

2. Melhorias na função de crossover:
    - Garantia de que cada ordem seja atribuída apenas uma vez, reduzindo a possibilidade de soluções inviáveis.

3. Processo de mutação:
    - Verificação da qualidade da mutação. Se uma mutação leva a uma solução pior, a mutação é desfeita.

4. Inclusão do Elitismo:
    - Implementação de uma estratégia de elitismo, onde os melhores indivíduos da população são mantidos entre as gerações.

5. Reinicialização da população:
    - Reinicialização parcial da população a cada certo número de gerações para evitar convergência precoce para uma solução subótima.

6. Regra de habilidades mínimas:
    - Inclusão de uma regra para que os operadores atendam ao menos 50% das habilidades necessárias para evitar que uma pessoa desqualificada atenda a ordem.


## Detalhamento do Algoritmo Genético

### Geração da População Inicial
A população inicial é composta por um conjunto de soluções (indivíduos) geradas aleatoriamente. Cada solução representa uma possível alocação de ordens de serviço para operadores ao longo de um período de dias.

#### Passos para a Geração da População Inicial:
1. **Criação de Soluções Iniciais**:
   - Para cada solução, distribuímos as ordens de serviço aleatoriamente entre os operadores e dias.
   - Garantimos que cada operador alocado tenha as habilidades necessárias para atender a ordem de serviço.
   - Utilizamos a função `create_initial_solution` para gerar essas soluções iniciais.

2. **Estrutura da Solução**:
   - Cada solução é representada por um dicionário aninhado, onde as chaves são os dias e os valores são dicionários de operadores e suas respectivas ordens de serviço.
   - Exemplo de estrutura: `{dia: {operador_id: [ordem_ids]}}`.

### Processo de Seleção
A seleção é o processo de escolher quais soluções (pais) serão utilizadas para gerar novas soluções (filhos) na próxima geração. Utilizamos um método de torneio para a seleção.

#### Passos para a Seleção:
1. **Torneio**:
   - Selecionamos aleatoriamente um grupo de soluções (torneio) da população.
   - Avaliamos a aptidão de cada solução no torneio.
   - Escolhemos a solução com a melhor aptidão como um dos pais.

2. **Repetição**:
   - Repetimos o processo de torneio até selecionar o número necessário de pais para gerar a nova população.

### Processo de Crossover
O crossover é o processo de combinar duas soluções (pais) para gerar uma nova solução (filho). Utilizamos um ponto de crossover para dividir as soluções dos pais e combiná-las.

#### Passos para o Crossover:
1. **Ponto de Crossover**:
   - Escolhemos aleatoriamente um ponto de crossover que divide os dias da solução.
   - Exemplo: Se temos 5 dias, o ponto de crossover pode ser 2, dividindo a solução em dois segmentos (dias 1-2 e dias 3-5).

2. **Combinação de Segmentos**:
   - O primeiro segmento da solução do filho é copiado do primeiro pai até o ponto de crossover.
   - O segundo segmento da solução do filho é copiado do segundo pai após o ponto de crossover.

3. **Garantia de Viabilidade**:
   - Garantimos que cada ordem de serviço seja atribuída apenas uma vez.
   - Se alguma ordem não for atribuída após o crossover, ela é atribuída aleatoriamente a um operador em um dia aleatório.

### Processo de Mutação
A mutação é o processo de introduzir pequenas alterações em uma solução para promover a diversidade genética. Realizamos a mutação trocando ordens aleatórias entre dois operadores no mesmo dia.

#### Passos para a Mutação:
1. **Probabilidade de Mutação**:
   - Para cada dia na solução, verificamos se a mutação deve ocorrer com base em uma taxa de mutação predefinida.

2. **Troca de Ordens**:
   - Selecionamos aleatoriamente dois operadores no mesmo dia.
   - Trocamos ordens aleatórias entre esses operadores.

3. **Verificação de Qualidade**:
   - Avaliamos a aptidão da solução antes e depois da mutação.
   - Se a mutação não melhorar a aptidão, desfazemos a mutação.

### Construção da Função de Aptidão
A função de aptidão avalia a qualidade de uma solução com base em critérios específicos. No nosso caso, consideramos a compatibilidade das habilidades, o cumprimento de prazos e o excesso de horas trabalhadas.

#### Critérios da Função de Aptidão:
1. **Compatibilidade de Habilidades**:
   - Avaliamos se as habilidades do operador atendem aos requisitos da ordem de serviço.
   - Atribuímos uma pontuação positiva se as habilidades forem compatíveis e uma penalidade se não forem.

2. **Cumprimento de Prazos**:
   - Verificamos se as ordens de serviço são concluídas dentro do prazo estipulado.
   - Aplicamos penalidades para ordens que não são completadas dentro do prazo, proporcionalmente à prioridade da ordem e ao número de dias de atraso.

3. **Excesso de Horas Trabalhadas**:
   - Calculamos o total de horas trabalhadas por cada operador em um dia.
   - Aplicamos penalidades para horas trabalhadas que excedem a capacidade diária do operador.

#### Cálculo da Aptidão:
- A aptidão final de uma solução é a soma das pontuações de compatibilidade, penalidades de atraso e penalidades por excesso de horas.
- Utilizamos a função `calculate_fitness` para realizar esse cálculo.

### Resumo do Algoritmo Genético
1. **Inicialização**:
   - Geramos uma população inicial de soluções aleatórias.

2. **Evolução**:
   - Para cada geração, calculamos a aptidão de cada solução.
   - Selecionamos os melhores pais utilizando o método de torneio.
   - Realizamos o crossover para gerar novos filhos.
   - Aplicamos mutações para introduzir diversidade genética.
   - Implementamos elitismo para manter as melhores soluções entre as gerações.
   - Periodicamente reinicializamos parte da população para evitar convergência precoce.

3. **Resultado Final**:
   - Após um número predefinido de gerações, a melhor solução encontrada é selecionada como a solução final.
   - A solução final é convertida em um DataFrame para facilitar a visualização e análise.

Este detalhamento fornece uma visão abrangente das técnicas e regras utilizadas na implementação do algoritmo genético para otimização da alocação de ordens de manutenção.

## Informações gerais sobre o resultado do algoritmo

A análise dos resultados do algoritmo genético para alocação de ordens de serviço de manutenção revela aspectos importantes sobre sua performance e limitações. O algoritmo foi desenvolvido para otimizar a distribuição de 100 ordens de serviço entre 15 operadores ao longo de 5 dias, considerando múltiplas variáveis como habilidades técnicas, prioridades e prazos.

### Resultados Principais

1. **Capacidade de Alocação**
   - O algoritmo conseguiu alocar 100% das ordens de serviço (100 ordens)
   - A distribuição contemplou todos os 15 operadores disponíveis
   - Houve cobertura dos 5 dias do período analisado

2. **Distribuição Temporal**
   - **Concentração nos Primeiros Dias**:
     * Dia 1: 29 ordens (142 horas) - 28,3% do total de horas
     * Dia 2: 23 ordens (104 horas) - 20,7% do total de horas
     * Dia 3: 23 ordens (128 horas) - 25,5% do total de horas
     * Dia 4: 11 ordens (62 horas) - 12,4% do total de horas
     * Dia 5: 14 ordens (66 horas) - 13,1% do total de horas

3. **Gestão de Prioridades**
   - **Distribuição por Nível de Prioridade**:
     * Urgente: 26 ordens (26%)
     * Alta: 28 ordens (28%)
     * Média: 27 ordens (27%)
     * Baixa: 19 ordens (19%)

4. **Compatibilidade de Habilidades**
   - A compatibilidade média ficou em 82%
   - Foram necessárias adaptações para cobrir todas as ordens

### Desafios e Limitações Identificadas

1. **Capacidade Operacional**
   - O volume de trabalho excede significativamente a capacidade da equipe
   - A média de horas extras por operador está muito acima do aceitável
   - Possível necessidade de redimensionamento da equipe

2. **Distribuição Temporal**
   - Concentração excessiva nos primeiros três dias
   - Subutilização da capacidade nos últimos dois dias
   - Necessidade de melhor balanceamento da carga de trabalho

3. **Gestão de Prioridades**
   - Atrasos em ordens urgentes indicam necessidade de ajustes no algoritmo
   - O sistema de priorização atual pode não estar sendo suficientemente considerado

4. **Compatibilidade Técnica**
   - Ausência de matches perfeitos sugere possível necessidade de:
     * Treinamento adicional para a equipe
     * Revisão dos critérios de matching
     * Possível contratação de especialistas em áreas específicas

### Recomendações para Melhorias

1. **Ajustes no Algoritmo**:
   - Implementar pesos mais significativos para prioridades urgentes
   - Melhorar a distribuição temporal das ordens
   - Refinar os critérios de matching de habilidades

2. **Recursos Humanos**:
   - Avaliar a necessidade de contratações adicionais
   - Identificar gaps de habilidades para treinamento
   - Considerar a redistribuição de operadores entre turnos

3. **Processos**:
   - Revisar os critérios de classificação de prioridades
   - Estabelecer limites mais rígidos para horas extras
   - Implementar mecanismos de balanceamento de carga

Esta análise demonstra que, embora o algoritmo tenha conseguido alocar todas as ordens, existem oportunidades significativas de melhoria para otimizar a distribuição do trabalho e garantir uma operação mais sustentável e eficiente.

### 1. Estatísticas gerais

| Métrica | Valor |
|---------|-------|
| Total de Ordens | 100 |
| Ordens Alocadas | 100 (100.0%) |
| Ordens Não Alocadas | 0 |

### 2. Análise por prioridade

| Prioridade | Quantidade | Percentual |
|------------|------------|------------|
| Urgente | 26 | 26.0% |
| Alta | 28 | 28.0% |
| Média | 27 | 27.0% |
| Baixa | 19 | 19.0% |

### 3. Análise por operador

| Operador | Ordens Alocadas | Horas Alocadas | Capacidade | % Utilização |
|----------|-----------------|----------------|------------|--------------|
| op1 | 10 | 57.0h | 7.0h | 814.3% |
| op2 | 6 | 32.0h | 8.0h | 400.0% |
| op3 | 5 | 28.0h | 7.0h | 400.0% |
| op4 | 7 | 28.0h | 9.0h | 311.1% |
| op5 | 9 | 37.0h | 9.0h | 411.1% |
| op6 | 9 | 43.0h | 8.0h | 537.5% |
| op7 | 5 | 26.0h | 7.0h | 371.4% |
| op8 | 6 | 29.0h | 7.0h | 414.3% |
| op9 | 10 | 43.0h | 7.0h | 614.3% |
| op10 | 10 | 50.0h | 7.0h | 714.3% |
| op11 | 5 | 32.0h | 8.0h | 400.0% |
| op13 | 6 | 34.0h | 7.0h | 485.7% |
| op14 | 5 | 23.0h | 7.0h | 328.6% |
| op15 | 4 | 22.0h | 7.0h | 314.3% |
| op12 | 3 | 18.0h | 8.0h | 225.0% |

### 4. Análise de prazos

| Métrica | Valor |
|---------|-------|
| Ordens no Prazo | 65 (65.0%) |

## Detalhamento dos Atrasos

| Ordem | Dias de Atraso | Prioridade |
|-------|----------------|------------|
| ordem40 | 1 | urgente |
| ordem63 | 1 | alta |
| ordem92 | 1 | urgente |
| ordem62 | 1 | urgente |
| ordem12 | 1 | alta |
| ordem70 | 1 | urgente |
| ordem48 | 1 | média |
| ordem38 | 1 | urgente |
| ordem95 | 2 | média |
| ordem24 | 2 | média |
| ordem44 | 1 | baixa |
| ordem90 | 2 | baixa |
| ordem61 | 2 | alta |
| ordem46 | 2 | urgente |
| ordem67 | 2 | média |
| ordem49 | 1 | alta |
| ordem78 | 3 | alta |
| ordem29 | 2 | média |
| ordem1 | 1 | média |
| ordem80 | 1 | urgente |
| ordem5 | 3 | alta |
| ordem39 | 2 | média |
| ordem59 | 3 | baixa |
| ordem42 | 3 | baixa |
| ordem76 | 2 | baixa |
| ordem65 | 1 | alta |
| ordem15 | 2 | baixa |
| ordem57 | 1 | alta |
| ordem100 | 1 | baixa |
| ordem21 | 2 | urgente |
| ordem3 | 1 | urgente |
| ordem81 | 4 | média |
| ordem51 | 4 | alta |
| ordem9 | 2 | média |
| ordem79 | 2 | alta |

### 5. Análise de compatibilidade

| Métrica | Valor |
|---------|-------|
| Matches Perfeitos | 0 (0.0%) |
| Compatibilidade Média | 8200.0% |

### 6. Distribuição por dia

#### Dia 1
| Métrica | Valor |
|---------|-------|
| Total de Ordens | 29 |
| Horas Alocadas | 142.0h |

**Distribuição de Prioridades:**
- Urgente: 8
- Alta: 7
- Média: 7
- Baixa: 7

#### Dia 2
| Métrica | Valor |
|---------|-------|
| Total de Ordens | 23 |
| Horas Alocadas | 104.0h |

**Distribuição de Prioridades:**
- Urgente: 9
- Alta: 8
- Média: 5
- Baixa: 1

#### Dia 3
| Métrica | Valor |
|---------|-------|
| Total de Ordens | 23 |
| Horas Alocadas | 128.0h |

**Distribuição de Prioridades:**
- Urgente: 5
- Alta: 5
- Média: 8
- Baixa: 5

#### Dia 4
| Métrica | Valor |
|---------|-------|
| Total de Ordens | 11 |
| Horas Alocadas | 62.0h |

**Distribuição de Prioridades:**
- Urgente: 2
- Alta: 3
- Média: 4
- Baixa: 2

#### Dia 5
| Métrica | Valor |
|---------|-------|
| Total de Ordens | 14 |
| Horas Alocadas | 66.0h |

**Distribuição de Prioridades:**
- Urgente: 2
- Alta: 5
- Média: 3
- Baixa: 4

---

### Dados dos operadores

---

| operator_id | skills | level | shift | hours_per_day |
|------------|--------|-------|-------|---------------|
| op1 | alvenaria \| pintura | sênior | manhã | 7 |
| op2 | solda \| alvenaria | pleno | noite | 8 |
| op3 | solda \| pintura | sênior | noite | 7 |
| op4 | pintura \| alvenaria | sênior | tarde | 9 |
| op5 | alvenaria \| elétrica \| solda | júnior | noite | 9 |
| op6 | hidráulica \| pintura \| alvenaria | júnior | noite | 8 |
| op7 | alvenaria \| hidráulica \| solda | sênior | manhã | 7 |
| op8 | alvenaria \| pintura | sênior | tarde | 7 |
| op9 | solda \| elétrica | sênior | manhã | 7 |
| op10 | hidráulica \| elétrica \| alvenaria | pleno | manhã | 7 |
| op11 | alvenaria \| pintura | júnior | noite | 8 |
| op12 | alvenaria \| hidráulica | júnior | tarde | 8 |
| op13 | elétrica \| pintura | especialista | manhã | 7 |
| op14 | alvenaria \| solda \| pintura | sênior | tarde | 7 |
| op15 | alvenaria \| pintura | júnior | noite | 7 |

### Dados das ordens

| order_id | required_skills | estimated_hours | priority | expected_start_day |
|----------|----------------|-----------------|----------|-------------------|
| ordem1 | alvenaria | 2 | média | 3 |
| ordem2 | solda \| pintura | 7 | urgente | 4 |
| ordem3 | solda | 6 | urgente | 4 |
| ordem4 | elétrica | 2 | média | 4 |
| ordem5 | elétrica | 2 | alta | 1 |
| ... | ... | ... | ... | ... |
| ordem96 | pintura \| solda | 8 | alta | 4 |
| ordem97 | pintura \| alvenaria | 6 | urgente | 4 |
| ordem98 | alvenaria \| solda | 4 | alta | 2 |
| ordem99 | pintura \| alvenaria | 4 | baixa | 5 |
| ordem100 | hidráulica | 7 | baixa | 4 |

[100 rows x 5 columns]

### Dados das ordens atribuídas aos operdores (shape = (100, 16))

| dia | id_operador | id_ordem | habilidades_ordem | habilidades_nao_atendidas | compatibilidade_nivel_prioridade | hora_extra | total_hora_extra |
|-----|-------------|----------|-------------------|---------------------------|----------------------------------|------------|------------------|
| 3 | op1 | ordem2 | solda \| pintura | solda | OK | Não | 0 |
| 2 | op1 | ordem26 | pintura \| alvenaria | | OK | Sim | 1 |
| 5 | op1 | ordem42 | pintura | | OK | Não | 0 |
| 2 | op1 | ordem47 | alvenaria \| hidráulica | hidráulica | OK | Sim | 5 |
| 3 | op1 | ordem48 | alvenaria | | OK | Sim | 7 |
| ... | ... | ... | ... | ... | ... | ... | ... |
| 5 | op9 | ordem3 | solda | | OK | Não | 0 |
| 3 | op9 | ordem58 | elétrica | | OK | Sim | 2 |
| 5 | op9 | ordem81 | alvenaria \| solda | alvenaria | OK | Sim | 1 |
| 3 | op9 | ordem88 | elétrica | | OK | Sim | 6 |
| 4 | op9 | ordem93 | solda | | OK | Não | 0 |

## Possíveis melhorias
Esta seção apresenta possíveis melhorias para o algoritmo genético, considerando os resultados obtidos e as limitações identificadas durante a execução dos testes.
