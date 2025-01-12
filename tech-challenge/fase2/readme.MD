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