import random
import pandas as pd
from .common_functions import *

# Função para criação de uma solução inicial
def create_initial_solution(operators, orders, days=5):
    """
    Cria uma solução inicial aleatória, garantindo que apenas operadores com as habilidades necessárias
    sejam atribuídos às ordens.
    Args:
        operators (dict): Operadores disponíveis.
        orders (dict): Ordens de serviço a serem alocadas.
        days (int): Número de dias do planejamento.
    Returns:
        dict: Solução inicial com alocação de ordens por operador e dia.
    Detalhes:
    - Distribui ordens aleatoriamente para operadores e dias.
    - Garante que o operador alocado tenha as habilidades necessárias para atender a ordem.
    - A solução gerada será ajustada pelo algoritmo genético.
    """
    solution = {day: {op: [] for op in operators.keys()} for day in range(days)}
    unassigned_orders = list(orders.keys())

    for order_id in unassigned_orders:
        valid_operators = [
            op_id for op_id, operator in operators.items()
            if meets_minimum_skills(operator["skills"], orders[order_id]["required_skills"])
        ]
        if valid_operators:  # Apenas atribui se houver operadores válidos
            day = random.randint(0, days-1)  # Atribui a ordem aleatoriamente a um dia
            operator = random.choice(valid_operators)  # Atribui a ordem a um operador válido
            solution[day][operator].append(order_id)

    return solution

# TODO: Funçao aparentemente não utilizada
# Converte os dados de exemplo em dataframe para facilitar a visualização
def sample_to_dataframe(operators, service_orders):
    """
    Converte os dados simulados de operadores e ordens de serviço em DataFrames.

    Args:
        operators (dict): Dicionário com dados dos operadores, incluindo suas habilidades, turnos e horas de trabalho.
        service_orders (dict): Dicionário com ordens de serviço, incluindo habilidades exigidas, horas estimadas, prioridade e inicio_esperado.

    Returns:
        tuple: Um tuple contendo dois DataFrames:
            - operators_df: DataFrame com os dados dos operadores.
            - service_orders_df: DataFrame com os dados das ordens de serviço.

    Detalhes:
    - O DataFrame dos operadores inclui as colunas: 'operator_id', 'skills', 'level', 'shift', 'hours_per_day'.
    - O DataFrame das ordens de serviço inclui as colunas: 'order_id', 'required_skills', 'estimated_hours', 'priority', 'expected_start_day'.
    """

    # Converte os operadores em um DataFrame
    operators_data = []
    for operator_id, details in operators.items():
        operators_data.append({
            "operator_id": operator_id,
            "skills": " | ".join(details["skills"]),
            "level": details["level"],
            "shift": details["shift"],
            "hours_per_day": details["hours_per_day"]
        })

    operators_df = pd.DataFrame(operators_data)

    # Converte as ordens de serviço em um DataFrame
    service_orders_data = []
    for order_id, details in service_orders.items():
        service_orders_data.append({
            "order_id": order_id,
            "required_skills": " | ".join(details["required_skills"]),
            "estimated_hours": details["estimated_hours"],
            "priority": details["priority"],
            "expected_start_day": details["expected_start_day"]
        })

    service_orders_df = pd.DataFrame(service_orders_data)

    return operators_df, service_orders_df

# TODO: função aparece como não utilizada
# Função para converter nível de habilidade em valor numérico
def skill_level_to_number(level):
    """
    Converte o nível de habilidade em um valor numérico.
    Args:
        level (str): Nível de habilidade (júnior, pleno, sênior, especialista).
    Returns:
        int: Valor numérico correspondente ao nível.
    Detalhes:
    - Utilizado para comparar habilidades entre operador e ordem.
    """
    levels = {"júnior": 1, "pleno": 2, "sênior": 3, "especialista": 4}
    return levels.get(level, 0)

# Função para realizar o crossover entre dois pais, garantindo que cada ordem seja atribuída apenas uma vez
def crossover(parent1, parent2, operators, orders):
    """
    Realiza o crossover entre dois pais, garantindo que cada ordem seja atribuída apenas uma vez e que operadores atendam a pelo menos 50% das habilidades necessárias.

    Args:
        parent1 (dict): A solução do primeiro pai, contendo a alocação de ordens a operadores por dia.
        parent2 (dict): A solução do segundo pai, contendo a alocação de ordens a operadores por dia.

    Returns:
        dict: A solução do filho gerada pelo crossover, com a alocação de ordens a operadores por dia.

    Detalhes:
    - A solução resultante do crossover é composta por dois segmentos:
      1. O primeiro segmento é copiado do pai 1 até o ponto de crossover.
      2. O segundo segmento é copiado do pai 2 após o ponto de crossover.
    - Durante o crossover, garante-se que uma ordem não seja atribuída mais de uma vez.
    - Se alguma ordem não for atribuída após o crossover, ela é atribuída aleatoriamente a um operador em um dia aleatório.
    """
    days = len(parent1)
    crossover_point = random.randint(1, days-1)

    # Inicializa o filho com alocações vazias
    child = {day: {op: [] for op in parent1[0].keys()} for day in range(days)}

    # Rastreia as ordens atribuídas
    assigned_orders = set()

    # Primeiro, copia as alocações do pai 1 até o ponto de crossover
    for day in range(crossover_point):
        for operator, s_orders in parent1[day].items():
            for order in s_orders:
                if order not in assigned_orders and meets_minimum_skills(operators[operator]["skills"], orders[order]["required_skills"]):
                    child[day][operator].append(order)
                    assigned_orders.add(order)

    # Depois, copia as alocações do pai 2 após o ponto de crossover
    for day in range(crossover_point, days):
        for operator, s_orders in parent2[day].items():
            for order in s_orders:
                if order not in assigned_orders and meets_minimum_skills(operators[operator]["skills"], orders[order]["required_skills"]):
                    child[day][operator].append(order)
                    assigned_orders.add(order)

    # Lida com as ordens não atribuídas do pai 1
    for day in range(days):
        for operator, s_orders in parent1[day].items():
            for order in s_orders:
                if order not in assigned_orders and meets_minimum_skills(operators[operator]["skills"], orders[order]["required_skills"]):
                    # Encontra um dia e um operador aleatório para atribuir a ordem
                    random_day = random.randint(0, days-1)
                    random_operator = random.choice(list(child[random_day].keys()))
                    child[random_day][random_operator].append(order)
                    assigned_orders.add(order)

    return child

# Função para realizar a mutação em um novo indivíduo
def mutate(solution, operators, orders, mutation_rate=0.1):
    """
    Realiza a mutação em uma solução, aceitando apenas mutações benéficas.

    Args:
        solution: A solução atual, contendo a alocação de ordens a operadores por dia.
        operators: Dicionário de operadores, contendo suas habilidades e horários.
        orders: Dicionário de ordens de serviço, contendo as habilidades necessárias, horas estimadas, etc.
        mutation_rate (float): Taxa de mutação, indicando a probabilidade de ocorrer uma mutação (entre 0 e 1).

    Returns:
        mutated: A solução mutada, se a mutação for benéfica, caso contrário, retorna a solução original.

    Detalhes:
    - A mutação é realizada trocando ordens aleatórias entre dois operadores no mesmo dia.
    - Verifica se na mutação realizada, as habilidades do operador atendem os requisitos da ordem.
    - A solução é validada antes e depois da mutação, e se a mutação não melhorar a aptidão, ela é desfeita.
    """
    mutated = solution.copy()

    for day in mutated:
        if random.random() < mutation_rate:
            # Troca ordens entre dois operadores aleatórios no mesmo dia
            operators_in_day = list(mutated[day].keys())
            if len(operators_in_day) >= 2:
                op1, op2 = random.sample(operators_in_day, 2)
                if mutated[day][op1] and mutated[day][op2]:
                    # Escolhe ordens aleatórias para trocar
                    idx1 = random.randint(0, len(mutated[day][op1]) - 1)
                    idx2 = random.randint(0, len(mutated[day][op2]) - 1)

                    # Troca as ordens entre os dois operadores
                    order1, order2 = mutated[day][op1][idx1], mutated[day][op2][idx2]
                    
                    # Verifica se as trocas realizadas atendem os requisitos das habilidades
                    if meets_minimum_skills(operators[op2]["skills"], orders[order1]["required_skills"]) and meets_minimum_skills(operators[op1]["skills"], orders[order2]["required_skills"]):
                        mutated[day][op1][idx1], mutated[day][op2][idx2] = order2, order1

                        # Verifica se a aptidão melhorou, e se não, desfaz a troca
                        original_fitness = calculate_fitness(solution, operators, orders)
                        new_fitness = calculate_fitness(mutated, operators, orders)

                        # Se a nova solução for pior, desfaz a mutação
                        if new_fitness < original_fitness:
                            mutated[day][op1][idx1], mutated[day][op2][idx2] = order1, order2

    return mutated

# TODO: possível código deprecated
# Função para converter a solução final em um DataFrame
def solution_to_dataframe_actual(solution, operators, orders):
    """
    Converte a solução final de alocação de ordens a operadores em um DataFrame.

    Args:
        solution (dict): A solução final, contendo a alocação de ordens a operadores por dia.
        operators (dict): Dicionário de operadores, contendo suas habilidades e horários.
        orders (dict): Dicionário de ordens de serviço, contendo as habilidades necessárias, horas estimadas, etc.

    Returns:
        pd.DataFrame: Um DataFrame contendo a solução de alocação de ordens com informações detalhadas.

    Detalhes:
    - O DataFrame contém as colunas: dia, id do operador, id da ordem, habilidades da ordem, horas estimadas,
      prioridade e inicio_esperado.
    """
    data = []

    for day, assignments in solution.items():
        for operator_id, order_ids in assignments.items():
            for order_id in order_ids:
                order = orders[order_id]
                operator = operators[operator_id]

                row = {
                    "dia": day + 1,  # Dias começam de 1
                    "id_operador": operator_id,
                    "id_ordem": order_id,
                    "habilidades_ordem": " | ".join(order["required_skills"]),  # Formatação das habilidades
                    "habilidades_operador": " | ".join(operator["skills"]),
                    "nivel_operador": operator["level"],
                    "horas_estimadas": order["estimated_hours"],
                    "horas_disponiveis": operator["hours_per_day"],
                    "prioridade": order["priority"],
                    "prazo": order["expected_start_day"]
                }
                data.append(row)

    df = pd.DataFrame(data)
    unassigned_orders = list(set(orders.keys() - set(df["id_ordem"].unique())))
    return df, unassigned_orders

# Função para imprimir na tela o resultado do algoritmo.
def imprimir_resultados_alocacao(df, unassigned_orders, operators, orders):
    """
    Imprime um relatório detalhado da alocação de ordens de serviço.
    
    Args:
        df (pd.DataFrame): DataFrame com a solução de alocação
        unassigned_orders (list): Lista de ordens não alocadas
        operators (dict): Dicionário com informações dos operadores
        orders (dict): Dicionário com informações das ordens
    """
    print("\n" + "="*80)
    print("RELATÓRIO DETALHADO DE ALOCAÇÃO".center(80))
    print("="*80)

    # 1. Estatísticas Gerais
    total_ordens = len(orders)
    ordens_alocadas = len(df['id_ordem'].unique())
    ordens_nao_alocadas = len(unassigned_orders)

    print("\n1. ESTATÍSTICAS GERAIS")
    print("-"*40)
    print(f"Total de Ordens: {total_ordens}")
    print(f"Ordens Alocadas: {ordens_alocadas} ({(ordens_alocadas/total_ordens)*100:.1f}%)")
    print(f"Ordens Não Alocadas: {ordens_nao_alocadas}")

    # 2. Análise por Prioridade
    print("\n2. ANÁLISE POR PRIORIDADE")
    print("-"*40)
    for prioridade in ['urgente', 'alta', 'média', 'baixa']:
        count = len(df[df['prioridade'] == prioridade])
        if count > 0:
            print(f"Prioridade {prioridade:8s}: {count:3d} ordens ({(count/ordens_alocadas)*100:5.1f}%)")

    # 3. Análise por Operador
    print("\n3. ANÁLISE POR OPERADOR")
    print("-"*40)
    for operador in df['id_operador'].unique():
        df_op = df[df['id_operador'] == operador]
        horas_total = df_op['horas_estimadas'].sum()
        horas_disp = df_op['horas_disponiveis'].iloc[0]
        n_ordens = len(df_op)
        print(f"Operador {operador}:")
        print(f"  - Ordens alocadas: {n_ordens}")
        print(f"  - Horas alocadas: {horas_total:.1f}h de {horas_disp:.1f}h ({(horas_total/horas_disp)*100:.1f}%)")

    # 4. Análise de Prazos
    print("\n4. ANÁLISE DE PRAZOS")
    print("-"*40)
    
    ordens_no_prazo = len(df[df['atraso'] <= 0])
    print(f"Ordens no Prazo: {ordens_no_prazo} ({(ordens_no_prazo/ordens_alocadas)*100:.1f}%)")
    
    if len(df[df['atraso'] > 0]) > 0:
        print("\nDetalhamento dos Atrasos:")
        for _, row in df[df['atraso'] > 0].iterrows():
            print(f"  Ordem {row['id_ordem']}: {row['atraso']} dias de atraso (Prioridade: {row['prioridade']})")

    # 5. Análise de Habilidades
    print("\n5. ANÁLISE DE COMPATIBILIDADE")
    print("-"*40)
    
    def verificar_compatibilidade(row):
        req_skills = set(row['habilidades_ordem'].split(" | "))
        op_skills = set(row['habilidades_operador'].split(" | "))
        return len(req_skills.intersection(op_skills)) / len(req_skills)

    # df['compatibilidade_habilidade'] = df.apply(verificar_compatibilidade, axis=1)
    matches_perfeitos = len(df[df['compatibilidade_habilidade'] == 1])
    
    print(f"Matches Perfeitos: {matches_perfeitos} ({(matches_perfeitos/ordens_alocadas)*100:.1f}%)")
    print(f"Compatibilidade Média: {df['compatibilidade_habilidade'].mean()*100:.1f}%")

    # 6. Análise por Dia
    print("\n6. DISTRIBUIÇÃO POR DIA")
    print("-"*40)
    for dia in sorted(df['dia'].unique()):
        df_dia = df[df['dia'] == dia]
        print(f"\nDia {dia}:")
        print(f"  - Total de Ordens: {len(df_dia)}")
        print(f"  - Horas Alocadas: {df_dia['horas_estimadas'].sum():.1f}h")
        print(f"  - Distribuição de Prioridades:")
        for prioridade in ['urgente', 'alta', 'média', 'baixa']:
            count = len(df_dia[df_dia['prioridade'] == prioridade])
            if count > 0:
                print(f"    * {prioridade:8s}: {count:3d}")

    # 7. Ordens Não Alocadas
    if unassigned_orders:
        print("\n7. ORDENS NÃO ALOCADAS")
        print("-"*40)
        print(f"Total de ordens não alocadas: {len(unassigned_orders)}")
        
        # Agrupa por prioridade
        unassigned_by_priority = {}
        for order_id in unassigned_orders:
            priority = orders[order_id]['priority']
            if priority not in unassigned_by_priority:
                unassigned_by_priority[priority] = []
            unassigned_by_priority[priority].append(order_id)
        
        for priority in ['urgente', 'alta', 'média', 'baixa']:
            if priority in unassigned_by_priority:
                orders_list = unassigned_by_priority[priority]
                print(f"\nPrioridade {priority}: {len(orders_list)} ordens")
                for order_id in orders_list:
                    order = orders[order_id]
                    print(f"  - {order_id}: "
                          f"Skills={', '.join(order['required_skills'])}, "
                          f"Horas={order['estimated_hours']}, "
                          f"Prazo={order['expected_start_day']}")

    print("\n" + "="*80)
    print("FIM DO RELATÓRIO".center(80))
    print("="*80)

    # Retorna métricas principais para uso no algoritmo genético
    return {
        'total_ordens': total_ordens,
        'ordens_alocadas': ordens_alocadas,
        'ordens_nao_alocadas': ordens_nao_alocadas,
        'taxa_alocacao': (ordens_alocadas/total_ordens)*100,
        'matches_perfeitos': matches_perfeitos,
        'taxa_matches_perfeitos': (matches_perfeitos/ordens_alocadas)*100 if ordens_alocadas > 0 else 0,
        'compatibilidade_media': df['compatibilidade_habilidade'].mean()*100 if not df.empty else 0,
        'ordens_no_prazo': ordens_no_prazo,
        'taxa_cumprimento_prazo': (ordens_no_prazo/ordens_alocadas)*100 if ordens_alocadas > 0 else 0
    }

# TODO: possível código deprecated
# Função para determinar o status das ordens
def update_order_status(solution, orders):
    """
    Atualiza o status das ordens com base na solução fornecida.

    Args:
        solution: Solução atual contendo dias, operadores e ordens atribuídas.
        orders: Dicionário de ordens com informações como `expected_start_day`.

    Returns:
        orders: Dicionário de ordens atualizado com os novos status.
    """
    # Atualiza o status com base na solução
    for day, operators in solution.items():
        for assigned_orders in operators.values():
            # Verifica se assigned_orders é uma lista
            if not isinstance(assigned_orders, list):
                raise TypeError(f"Esperado uma lista de ordens, mas recebeu: {type(assigned_orders)}")
            for order_id in assigned_orders:
                # Verifica se order_id é válido e se existe em orders
                if not isinstance(order_id, (int, str)):
                    raise TypeError(f"Esperado um identificador de ordem (int ou str), mas recebeu: {type(order_id)}")
                if order_id in orders:
                    order = orders[order_id]
                    if day <= order["expected_start_day"]:
                        order["status"] = "atendida"
                    elif day > order["expected_start_day"]:
                        order["status"] = "atrasada"
    return orders
    
# TODO: possível código deprecated
# Função para executar o algoritmo genético
def run_genetic_algorithm(operators, orders, population_size=50, generations=100, mutation_rate=0.4, elitism_size=5, reinitalize_interval=10):
    """
    Executa o algoritmo genético, evoluindo uma população de soluções ao longo de várias gerações.

    Args:
        operators (dict): Dicionário de operadores disponíveis.
        orders (dict): Dicionário de ordens de serviço a serem alocadas.
        population_size (int): Tamanho da população de soluções.
        generations (int): Número de gerações a serem executadas.
        mutation_rate (float): Taxa de mutação.
        elitism_size (int): Tamanho da elite, ou seja, o número de melhores soluções que são mantidas.
        reinitalize_interval (int): Intervalo de gerações para reinicializar parte da população.

    Returns:
        pd.DataFrame: DataFrame contendo a melhor solução após as gerações.

    Detalhes:
    - A população inicial é gerada aleatoriamente.
    - Em cada geração, os melhores pais são selecionados para realizar o crossover e gerar novos filhos.
    - O algoritmo utiliza a mutação, elitismo e re-inicialização periódica da população.
    """
    # Criação da população inicial
    population = [create_initial_solution(operators, orders) for _ in range(population_size)]

    for generation in range(generations):
        # Cálculo da aptidão de cada solução
        fitness_scores = [calculate_fitness(solution, operators, orders) for solution in population]
        
        # Ajuste na taxa de mutação conforme o número da geração
        mutation_rate = mutation_rate - (generation / generations) * 0.05  # Reduz a taxa de mutação
        if mutation_rate < 0.05:
            mutation_rate = 0.05  # Taxa mínima de mutação


        # Exibição da aptidão da melhor solução da geração
        best_fitness = max(fitness_scores)
        print(f"\nGeneration {generation + 1}/{generations} - Best Fitness: {best_fitness:.2f} - Mutation Rate: {mutation_rate:.4f}")
        # time.sleep(0.1)  # Delay para animação

        # Seleção dos pais
        parents = []
        for _ in range(population_size // 2):
            tournament = random.sample(list(enumerate(fitness_scores)), 5)
            parent_idx = max(tournament, key=lambda x: x[1])[0]
            parents.append(population[parent_idx])

        # Implementação de elitismo: mantém as melhores 'elitism_size' soluções
        sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
        elite_population = [individual for individual, score in sorted_population[:elitism_size]]

        # Geração da nova população
        new_population = elite_population.copy()
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2, operators=operators, orders=orders)
            child = mutate(child, operators, orders, mutation_rate=mutation_rate)
            new_population.append(child)

        # Reinicialização da população a cada 'reinitalize_interval' gerações
        if generation % reinitalize_interval == 0:
            print(f"\n ------ Reinitializing population at generation {generation} ------")
            num_to_reinitialize = population_size // 2
            new_population[-num_to_reinitialize:] = [create_initial_solution(operators, orders) for _ in range(num_to_reinitialize)]

        population = new_population

    # Após as gerações, mostra a melhor solução
    best_solution = max(population, key=lambda sol: calculate_fitness(sol, operators, orders))
    print(f"\nBest solution fitness: {calculate_fitness(best_solution, operators, orders):.2f}")

    # Converte a melhor solução para DataFrame e imprime os resultados
    df, unassigned_orders = solution_to_dataframe(best_solution, operators, orders)
    imprimir_resultados_alocacao(df, unassigned_orders, operators, orders)
    
    return df, unassigned_orders