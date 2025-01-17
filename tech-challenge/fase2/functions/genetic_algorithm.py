import os
import random
import pandas as pd
import copy

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

# Função para converter prioridade em valor numérico
def priority_to_number(priority):
    """
    Converte o nível de prioridade em um valor numérico.
    Args:
        priority (str): Nível de prioridade (baixa, média, alta, urgente).
    Returns:
        int: Valor numérico correspondente à prioridade.
    Detalhes:
    - A prioridade influencia o peso de penalidades e pontuações.
    """
    priorities = {"baixa": 1, "média": 2, "alta": 3, "urgente": 4}
    return priorities.get(priority, 0)

# Função para criar os dados de exemplo
def create_initial_data(n_orders=None, n_operators=None):
    """
    Inicializa dados simulados de operadores e ordens de serviço. Se 'n_operators' for fornecido, gera operadores e ordens automaticamente.

    Args:
        n_orders (int): Número de ordens de serviço a serem criadas.
        n_operators (int, opcional): Número de operadores a serem gerados automaticamente. Se não fornecido, usa operadores predefinidos.

    Returns:
        tuple: Um dicionário com operadores e suas habilidades e outro com ordens de serviço.

    Detalhes:
    - Se 'n_operators' for fornecido, serão gerados operadores aleatórios com habilidades e horários.
    - As ordens de serviço são geradas com habilidades, horas estimadas, prioridade e inicio_esperado de forma aleatória.
    """
    skills = ["pintura", "elétrica", "alvenaria", "hidráulica", "solda"]
    skills_level = ["júnior", "pleno", "sênior", "especialista"]
    priority_levels = ["baixa", "média", "alta", "urgente"]

    # Geração automática de operadores, se n_operators for fornecido.
    if n_operators:
        operators = {}
        for i in range(1, n_operators + 1):
            op_id = f"op{i}"
            num_skills = random.randint(2, 3)
            op_skills = random.sample(skills, num_skills)
            level = random.choice(skills_level)
            shift = random.choice(["manhã", "tarde", "noite"])
            hours_per_day = random.randint(7, 9)
            operators[op_id] = {"skills": op_skills, "level": level, "shift": shift, "hours_per_day": hours_per_day}
    # Opçao Default
    else:
        # Dados dos operadores predefinidos.
        operators = {
            "op1": {"skills": ["pintura", "elétrica"], "level": "sênior", "shift": "manhã", "hours_per_day": 8},
            "op2": {"skills": ["hidráulica", "alvenaria"], "level": "pleno", "shift": "tarde", "hours_per_day": 8},
            "op3": {"skills": ["solda", "pintura"], "level": "sênior", "shift": "noite", "hours_per_day": 9},
            "op4": {"skills": ["elétrica", "hidráulica"], "level": "júnior", "shift": "manhã", "hours_per_day": 7},
        }

    # Geração dinâmica de ordens de serviço.
    if n_orders:
        service_orders = {}
        for i in range(n_orders):
            required_skills = random.sample(skills, random.randint(1, 2))
            service_orders[f"os{i+1}"] = {
                "required_skills": required_skills,
                "estimated_hours": random.randint(2, 8),
                "priority": random.choice(priority_levels),
                "expected_start_day": random.randint(1, 5),
                "status": "não_atendida",
            }
    # Opçao Default.
    else:
        service_orders = {
            'os1': {'required_skills': ['solda', 'alvenaria'], 'estimated_hours': 2, 'priority': 'média', 'expected_start_day': 3, 'status':'não_atendida'},
            'os2': {'required_skills': ['pintura', 'hidráulica'], 'estimated_hours': 8, 'priority': 'alta', 'expected_start_day': 2, 'status':'não_atendida'},
            'os3': {'required_skills': ['hidráulica'], 'estimated_hours': 5, 'priority': 'urgente', 'expected_start_day': 5, 'status':'não_atendida'},
            'os4': {'required_skills': ['hidráulica', 'pintura'], 'estimated_hours': 2, 'priority': 'urgente', 'expected_start_day': 1, 'status':'não_atendida'},
            'os5': {'required_skills': ['alvenaria'], 'estimated_hours': 5, 'priority': 'alta', 'expected_start_day': 3, 'status':'não_atendida'},
            'os6': {'required_skills': ['alvenaria'], 'estimated_hours': 7, 'priority': 'baixa', 'expected_start_day': 5, 'status':'não_atendida'},
            'os7': {'required_skills': ['elétrica'], 'estimated_hours': 7, 'priority': 'baixa', 'expected_start_day': 4, 'status':'não_atendida'},
            'os8': {'required_skills': ['solda'], 'estimated_hours': 8, 'priority': 'baixa', 'expected_start_day': 5, 'status':'não_atendida'},
            'os9': {'required_skills': ['pintura'], 'estimated_hours': 3, 'priority': 'baixa', 'expected_start_day': 4, 'status':'não_atendida'},
            'os10': {'required_skills': ['alvenaria', 'solda'], 'estimated_hours': 2, 'priority': 'alta', 'expected_start_day': 5, 'status':'não_atendida'}
        }

    return operators, service_orders

# Função para validar se as habilidades do operador atendem pelo menos 50% das habilidades da ordem
def meets_minimum_skills(operator_skills, required_skills):
    """
    Verifica se o operador atende pelo menos 50% das habilidades necessárias para a ordem.

    Args:
        operator_skills (list): Habilidades do operador.
        required_skills (list): Habilidades exigidas pela ordem.

    Returns:
        meets_minimum (bool): True se o operador atender pelo menos 50% das habilidades, False caso contrário.
        match_percentage(float): a porcentagem de habilidades atendidas.
    """
    matching_skills = set(operator_skills).intersection(required_skills)
    
    # Verifica se a porcentagem de habilidades está acima da metade (valor minimo).
    match_percentage = len(matching_skills) / len(required_skills) if required_skills else 1
    
    # Verifica se o operador atende pelo menos 50% das habilidades necessárias
    meets_minimum = match_percentage >= 0.5
    
    return meets_minimum, match_percentage

# Função para criação de uma solução inicial
def create_initial_solution(operators, orders, days):
    """
    Cria uma solução inicial aleatória, garantindo que apenas operadores com as habilidades necessárias
    sejam atribuídos às ordens.
    Args:
        operators (dict): Operadores disponíveis.
        orders (dict): Ordens de serviço a serem alocadas.
        days (int): Número de dias do planejamento.
    Returns:
        dict: Solução inicial com as OSs organizadas por prioridade.
    Detalhes:
    - Distribui ordens aleatoriamente para operadores e dias.
    - Garante que o operador alocado tenha as habilidades necessárias para atender a ordem.
    - A solução gerada será ajustada pelo algoritmo genético.
    """
    # Inicializa a solução.
    solution = {
        order_id: {"day": None, "operator": None, "status": "não atendida"}
        for order_id in orders.keys()
    }
    
    for order_id, order_data in orders.items():
        # Identifica operadores válidos para a ordem com base nas habilidades.
        valid_operators = [
            op_id for op_id, operator in operators.items()
            if meets_minimum_skills(operator["skills"], order_data["required_skills"])
        ]

        if valid_operators:  # Apenas atribui se houver operadores válidos.
            # Atribui a ordem a um dia e operador aleatórios.
            assigned_day = random.randint(1, days)
            assigned_operator = random.choice(valid_operators)

            # Calcula a quantidade de dias em atraso, se late_order > 0 = atraso.. 
            late_order = assigned_day - order_data["expected_start_day"]

            # Atualiza a solução para a OS atual
            solution[order_id]["day"] = assigned_day
            solution[order_id]["operator"] = assigned_operator
            solution[order_id]["status"] = "atrasada" if late_order > 0 else "atendida"

    return solution

# Função para calcular a aptidão de uma solução 
def calculate_fitness(solution, operators, orders):
    """
    Calcula a pontuação de aptidão de uma solução. A função avalia como uma solução de alocação de ordens a operadores
    é eficaz, levando em consideração a compatibilidade das habilidades, o cumprimento de prazo e o excesso de horas
    trabalhadas por cada operador.

    Args:
        solution (dict): Solução atual contendo as alocações de ordens por operador e dia.
                          Estrutura esperada: {day: {operator_id: [order_ids]}}.
        operators (dict): Dicionário com os dados dos operadores, incluindo suas habilidades e carga horária diária.
        orders (dict): Dicionário com as ordens de serviço, incluindo as habilidades necessárias e o tempo estimado para execução.

    Returns:
        int: A pontuação de aptidão da solução, onde valores mais altos indicam uma solução mais "apt" (ou mais eficiente).

    Detalhes:
    - A função leva em consideração três critérios principais para calcular a aptidão de uma solução:
        1. **Compatibilidade de habilidades**: A habilidade do operador deve ser compatível com a habilidade necessária para a ordem de serviço.
        2. **Cumprimento do inicio_esperado**: A solução penaliza ordens que não são completadas dentro do inicio_esperado estipulado pela ordem de serviço.
        3. **Excesso de horas**: Penaliza a alocação de mais horas do que a capacidade diária do operador.

    Penalidades:
    - **Compatibilidade de habilidades**: Quando a habilidade de um operador não é adequada à ordem, a pontuação é penalizada. A penalidade depende do nível de habilidade do operador em comparação com o nível necessário para a ordem.
    - **Cumprimento do inicio_esperado**: Se a ordem não for completada até o dia limite, é aplicada uma penalidade proporcional à quantidade de dias de atraso e à prioridade da ordem.
    - **Excesso de horas**: Se a soma das horas estimadas para a ordem ultrapassar as horas trabalhadas disponíveis para o operador em um dia, uma penalidade por excesso de horas será aplicada.
    
    A pontuação de aptidão final é a soma das pontuações de compatibilidade, penalidades de atraso e excesso de horas.
    """
    fitness = 0  # Inicia a pontuação de aptidão com zero.

    # Dicionário para rastrear as horas trabalhadas por operador por dia.
    operator_daily_hours = {op_id: {day: 0 for day in range(1, max(order["day"] for order in solution.values()) + 1)}
                            for op_id in operators.keys()}

    # Itera sobre cada ordem na solução.
    for order_id, allocation in solution.items():
        operator_id = allocation["operator"]
        day = allocation["day"]
        status = allocation["status"]

        # Obtém os dados da ordem e do operador.
        order = orders[order_id]
        operator = operators[operator_id]

        # Acumula as horas estimadas para a ordem no operador e dia correspondentes.
        operator_daily_hours[operator_id][day] += order["estimated_hours"]

        # Avaliação de compatibilidade de habilidades.
        skill_match_score = 0
        meets_mininum, match_percentage = meets_minimum_skills(operator["skills"], order["required_skills"])
        
        # Multiplica o skill_match_score de acordo com a porcentagem de skills possuidas pelo operador.
        if meets_mininum:
            skill_match_score += 10 * match_percentage
        else:
            skill_match_score -= 10

        # Avaliação da prioridade.
        priority_multiplier = priority_to_number(order["priority"])

        # Penaliza atrasos no início esperado.
        if status == "atrasada":  # Verifica se a ordem está atrasada.
            days_late =  max(0, day - order["expected_start_day"])
            fitness -= 5 * days_late * priority_multiplier

        # Aumenta a pontuação com base na compatibilidade de habilidades e prioridade.
        fitness += skill_match_score * priority_multiplier

    # Verifica o excesso de horas trabalhadas por operador por dia.
    for operator_id, daily_hours in operator_daily_hours.items():
        for day, hours_worked in daily_hours.items():
            excess_hours = max(0, hours_worked - operators[operator_id]["hours_per_day"])  # Garante que excess_hours não seja negativo.
            if excess_hours > 0:
                fitness -= 5 * excess_hours  # Penaliza o excesso de horas trabalhadas.

    return fitness  # Retorna a pontuação de aptidão final da solução.

# Função para realizar o crossover entre dois pais, garantindo que cada ordem seja atribuída apenas uma vez
def crossover(parent1, parent2, operators, orders, max_days):
    """
    Realiza o crossover entre dois pais, garantindo que cada ordem seja atribuída apenas uma vez e que operadores atendam a pelo menos 50% das habilidades necessárias.

    Args:
        parent1 (dict): A solução do primeiro pai, contendo a alocação de ordens a operadores por dia.
        parent2 (dict): A solução do segundo pai, contendo a alocação de ordens a operadores por dia.
        operators (dict): Dicionário de operadores com habilidades e capacidade.
        orders (dict): Dicionário de ordens com habilidades necessárias e detalhes.

    Returns:
        dict: A solução do filho gerada pelo crossover, com a alocação de ordens a operadores por dia.

    Detalhes:
    - A solução resultante do crossover é composta por dois segmentos:
      1. O primeiro segmento é copiado do pai 1 até o ponto de crossover.
      2. O segundo segmento é copiado do pai 2 após o ponto de crossover.
    - Durante o crossover, garante-se que uma ordem não seja atribuída mais de uma vez.
    - Se alguma ordem não for atribuída após o crossover, ela é atribuída aleatoriamente a um operador em um dia aleatório.
    """
    # Inicializa o filho com uma estrutura vazia.
    child = {}
    assigned_orders = set()  # Rastreia as ordens já atribuídas.

    # Obtém a lista de ordens para o ponto de crossover.
    order_ids = list(parent1.keys())
    crossover_point = random.randint(1, len(order_ids) - 1)

    # Primeiro segmento: Copia as ordens do pai 1 até o ponto de crossover.
    for order_id in order_ids[:crossover_point]:
        if order_id in parent1:
            order_data = parent1[order_id]
            operator = order_data["operator"]
            day = order_data["day"]
            status = order_data["status"]

            # Verifica se o operador é compatível e a ordem não foi atribuída.
            if (order_id not in assigned_orders
                and meets_minimum_skills(operators[operator]["skills"], orders[order_id]["required_skills"])
                ):
                child[order_id] = {"operator": operator, "day": day, "status": status}
                assigned_orders.add(order_id)

    # Segundo segmento: Copia as ordens do pai 2 após o ponto de crossover.
    for order_id in order_ids[crossover_point:]:
        if order_id in parent2:
            order_data = parent2[order_id]
            operator = order_data["operator"]
            day = order_data["day"]
            status = order_data["status"]

            # Verifica se o operador é compatível e a ordem não foi atribuída.
            if (order_id not in assigned_orders
                and meets_minimum_skills(operators[operator]["skills"], orders[order_id]["required_skills"])
            ):
                child[order_id] = {"operator": operator, "day": day, "status": status}
                assigned_orders.add(order_id)

    # Atribui ordens "não atribuídas" aleatoriamente.
    for order_id in orders.keys():
        if order_id not in assigned_orders:
            random_operator = random.choice(list(operators.keys()))
            random_day = random.randint(1, max_days)

            # Garante que o operador é compatível
            while not meets_minimum_skills(operators[random_operator]["skills"], orders[order_id]["required_skills"]):
                random_operator = random.choice(list(operators.keys()))

            child[order_id] = {"operator": random_operator, "day": random_day, "status": "não atendida"}
            assigned_orders.add(order_id)

    return child

# Função para realizar a mutação em um novo indivíduo
def mutate(solution, operators, orders, mutation_rate, max_days):
    """
    Realiza a mutação em uma solução, aceitando apenas mutações benéficas.

    Args:
        solution (dict): A solução atual, contendo a alocação de ordens a operadores por dia.
        operators (dict): Dicionário de operadores, contendo suas habilidades e horários.
        orders (dict): Dicionário de ordens de serviço, contendo as habilidades necessárias, horas estimadas, etc.
        mutation_rate (float): Taxa de mutação, indicando a probabilidade de ocorrer uma mutação (entre 0 e 1).

    Returns:
        mutated: A solução mutada, se a mutação for benéfica, caso contrário, retorna a solução original.

    Detalhes:
    - A mutação é realizada trocando ordens aleatórias entre dois operadores no mesmo dia.
    - Verifica se na mutação realizada, as habilidades do operador atendem os requisitos da ordem.
    - A solução é validada antes e depois da mutação, e se a mutação não melhorar a aptidão, ela é desfeita.
    """
    # Faz uma cópia profunda da solução para evitar alterações na original.
    mutated = copy.deepcopy(solution)

    # Aplica mutações em ordens individuais com base na taxa de mutação.
    for order_id, allocation in solution.items():
        if random.random() < mutation_rate:
            current_day = allocation["day"]
            current_operator = allocation["operator"]
            current_status = allocation["status"]
            expected_start_day = orders[order_id]["expected_start_day"]

            # Seleciona um novo operador e um novo dia aleatoriamente.
            new_day = random.randint(1, max_days)
            new_operator = random.choice(list(operators.keys()))

            # Verifica se o novo operador atende às habilidades necessárias para a ordem.
            if meets_minimum_skills(operators[new_operator]["skills"], orders[order_id]["required_skills"]):
                # Atualiza temporariamente a alocação para o novo operador e dia.
                mutated[order_id] = {"day": new_day, "operator": new_operator, "status": None}

                # Atualiza o status da ordem.
                mutated[order_id]["status"] = "atendida" if new_day <= expected_start_day else "atrasada"
                
                # Calcula a aptidão antes e depois da mutação.
                original_fitness = calculate_fitness(solution, operators, orders)
                new_fitness = calculate_fitness(mutated, operators, orders)

                # Se a mutação não melhorar a aptidão, desfaz a alteração.
                if new_fitness < original_fitness:
                    mutated[order_id] = {
                        "day": current_day, 
                        "operator": current_operator, 
                        "status": current_status
                        }
                    
    return mutated

# Converte os dados de exemplo em dataframe para facilitar a visualização
def op_orders_to_dataframe(operators, orders):
    """
    Converte os dados simulados de operadores e ordens de serviço em DataFrames.

    Args:
        operators (dict): Dicionário com dados dos operadores, incluindo suas habilidades, turnos e horas de trabalho.
        service_orders (dict): Dicionário com ordens de serviço, incluindo habilidades exigidas, horas estimadas, prioridade, inicio_esperado e status.

    Returns:
        tuple: Um tuple contendo dois DataFrames:
            - operators_df: DataFrame com os dados dos operadores.
            - service_orders_df: DataFrame com os dados das ordens de serviço.

    Detalhes:
    - O DataFrame dos operadores inclui as colunas: 'operator_id', 'skills', 'level', 'shift', 'hours_per_day'.
    - O DataFrame das ordens de serviço inclui as colunas: 'order_id', 'required_skills', 'estimated_hours', 'priority', 
        'expected_start_day', 'status'.
    """

    # Converte os operadores em um DataFrame
    operators_data = []
    for operator_id, details in operators.items():
        operators_data.append({
            "id_operador": operator_id,
            "habilidades_operador": " | ".join(details["skills"]),
            "nivel_operador": details["level"],
            "turno": details["shift"],
            "horas_disponiveis": details["hours_per_day"]
        })

    operators_df = pd.DataFrame(operators_data)

    # Converte as ordens de serviço em um DataFrame
    service_orders_data = []
    for order_id, details in orders.items():
        service_orders_data.append({
            "id_ordem": order_id,
            "Serviços": " | ".join(details["required_skills"]),
            "horas_estimadas": details["estimated_hours"],
            "prioridade": details["priority"],
            "inicio_esperado": details["expected_start_day"],
            "status": details["status"],
        })

    service_orders_df = pd.DataFrame(service_orders_data)

    return operators_df, service_orders_df

# Função para tranformar a solução encontrada em Dataframe
def solution_to_dataframe(solution, operators, orders):
    """
    Converte a solução final de alocação de ordens a operadores em um DataFrame.

    Args:
        solution (dict): A solução final, contendo a alocação de ordens a operadores por dia.
        operators (dict): Dicionário de operadores, contendo suas habilidades e horários.
        orders (dict): Dicionário de ordens de serviço, contendo as habilidades necessárias, horas estimadas, etc.

    Returns:
        df (pd.DataFrame): Um DataFrame contendo a solução de alocação de ordens com informações detalhadas.
        unassigned_orders (list): Lista de ordens que não foram alocadas.

    Detalhes:
    - O DataFrame contém as colunas: dia, id do operador, id da ordem, habilidades da ordem, horas estimadas,
      prioridade e inicio_esperado, além das novas colunas de compatibilidade e habilidades não atendidas.
    """
    data = []
    operator_daily_hours = {}

    for order_id, allocation in solution.items():
        day = allocation["day"]
        operator_ids = allocation["operator"]
        current_status = allocation["status"]

        # Verifica se a ordem foi atribuída a algum operador.
        if not operator_ids:
            operator_id = "N/A"
            operator = {"skills": [], "level": "N/A", "hours_per_day": 0}
        else:
            operator_id = operator_ids[0]  # Considera o primeiro operador da lista.
            operator = operators[operator_id]

        # Inicializa horas trabalhadas por operador no dia, se necessário.
        if day not in operator_daily_hours:
            operator_daily_hours[day] = {}
        if operator_id not in operator_daily_hours[day]:
            operator_daily_hours[day][operator_id] = 0

        # Dados da ordem.
        order = orders[order_id]
        required_skills = set(order["required_skills"])
        operator_skills = set(operator["skills"])

        matched_skills = required_skills & operator_skills
        missing_skills = required_skills - operator_skills

        skill_compatibility = len(matched_skills) / len(required_skills) if required_skills else 1.0

        # Verificar compatibilidade do nível com a prioridade.
        priority_level_map = {
            "alta": ["especialista", "sênior"],
            "urgente": ["especialista", "sênior"],
            "média": ["especialista", "sênior", "pleno"],
            "baixa": ["especialista", "sênior", "pleno", "júnior"]
        }

        priority = order["priority"]
        operator_level = operator["level"]
        compatibility_level = "OK" if operator_level in priority_level_map.get(priority, []) else "NOK"

        # Acumular horas do operador no dia.
        operator_daily_hours[day][operator_id] += order["estimated_hours"]
        total_hours = operator_daily_hours[day][operator_id]
        extra_hours = "Sim" if total_hours > operator["hours_per_day"] else "Não"
        total_extra_hours = total_hours - operator["hours_per_day"]

        # Montar os dados da linha.
        row = {
            "dia": day,  # Dias começam de 1.
            "id_ordem": order_id,
            "id_operador": operator_id,
            "Serviços": " | ".join(order["required_skills"]),  # Formatação das habilidades.
            "habilidades_operador": " | ".join(operator["skills"]),
            "nivel_operador": operator["level"],
            "horas_estimadas": order["estimated_hours"],
            "horas_disponiveis": operator["hours_per_day"],
            "prioridade": order["priority"],
            "inicio_esperado": order["expected_start_day"],
            "atraso": max(0, day - order["expected_start_day"]),
            "compatibilidade_os_op": round(skill_compatibility * 100, 2),
            "habilidades_nao_atendidas": " | ".join(missing_skills),
            "compatibilidade_prioridade": compatibility_level,
            "hora_extra": extra_hours,
            "total_hora_extra": total_extra_hours,
            "status": current_status,
        }

        data.append(row)

    # Converte os dados em um DataFrame.
    df = pd.DataFrame(data)

    # Identifica ordens não alocadas.
    unassigned_orders = list(set(orders.keys()) - set(df["id_ordem"].unique()))

    return df, unassigned_orders

# Função para imprimir na tela o resultado do algoritmo
def imprimir_resultados_alocacao(df, unassigned_orders, orders):
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

    # 1. Estatísticas Gerais.
    total_ordens = len(orders)
    ordens_alocadas = len(df['id_ordem'].unique())
    ordens_nao_alocadas = len(unassigned_orders)

    print("\n1. ESTATÍSTICAS GERAIS")
    print("-"*40)
    print(f"Total de Ordens: {total_ordens}")
    print(f"Ordens Alocadas: {ordens_alocadas} ({(ordens_alocadas/total_ordens)*100:.1f}%)")
    print(f"Ordens Não Alocadas: {ordens_nao_alocadas}")

    # 2. Análise por Prioridade.
    print("\n2. ANÁLISE POR PRIORIDADE")
    print("-"*40)
    for prioridade in ['urgente', 'alta', 'média', 'baixa']:
        count = len(df[df['prioridade'] == prioridade])
        if count > 0:
            print(f"Prioridade {prioridade:8s}: {count:3d} ordens ({(count/ordens_alocadas)*100:5.1f}%)")

    # 3. Análise por Operador.
    print("\n3. ANÁLISE POR OPERADOR")
    print("-"*40)
    for operador in df['id_operador'].unique():
        df_op = df[df['id_operador'] == operador]
        horas_total = df_op['horas_estimadas'].sum()
        horas_disp = df_op['horas_disponiveis'].iloc[0] if not df_op.empty else 0
        n_ordens = len(df_op)
        print(f"Operador {operador}:")
        print(f"  - Ordens alocadas: {n_ordens}")
        print(f"  - Horas alocadas: {horas_total:.1f}h de {horas_disp:.1f}h ({(horas_total/horas_disp)*100:.1f}%)")

    # 4. Análise de Prazos.
    print("\n4. ANÁLISE DE PRAZOS")
    print("-"*40)
    
    ordens_no_prazo = len(df[df['atraso'] <= 0])
    print(f"Ordens no Prazo: {ordens_no_prazo} ({(ordens_no_prazo/ordens_alocadas)*100:.1f}%)")
    
    atrasos = df[df['atraso'] > 0]
    if not atrasos.empty:
        print("\nDetalhamento dos Atrasos:")
        for _, row in atrasos.iterrows():
            print(f"  Ordem {row['id_ordem']}: {row['atraso']} dias de atraso (Prioridade: {row['prioridade']})")

    # 5. Análise de Habilidades.
    print("\n5. ANÁLISE DE COMPATIBILIDADE")
    print("-"*40)

    matches_perfeitos = len(df[df['compatibilidade_os_op'] == 1])
    compatibilidade_media = df['compatibilidade_os_op'].mean() if not df.empty else 0
    print(f"Matches Perfeitos: {matches_perfeitos} ({(matches_perfeitos/ordens_alocadas)*100:.1f}%)")
    print(f"Compatibilidade Média: {compatibilidade_media:.1f}%")

    # 6. Análise por Dia.
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

    # 7. Ordens Não Alocadas.
    if unassigned_orders:
        print("\n7. ORDENS NÃO ALOCADAS")
        print("-"*40)
        print(f"Total de ordens não alocadas: {len(unassigned_orders)}")
        
        # Agrupa por prioridade.
        unassigned_by_priority = {}
        for order_id in unassigned_orders:
            priority = orders[order_id]['priority']
            if priority not in unassigned_by_priority:
                unassigned_by_priority[priority] = []
            unassigned_by_priority[priority].append(order_id)
        
        for priority, order_list in unassigned_by_priority.items():
            print(f"\nPrioridade {priority}: {len(order_list)} ordens")
            for order_id in order_list:
                order = orders[order_id]
                print(f"  - {order_id}: Skills={', '.join(order['required_skills'])}, "
                      f"Horas={order['estimated_hours']}, Prazo={order['expected_start_day']}")

    print("\n" + "="*80)
    print("FIM DO RELATÓRIO".center(80))
    print("="*80)

    # Retorna métricas principais para uso no algoritmo genético.
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
    
def salvar_arquivos(dataframe):
    # Diretório do script em execução
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Defina o diretório onde os arquivos serão salvos
    result_dir = os.path.join(script_dir, "resultados")

    # Cria o diretório se não existir
    os.makedirs(result_dir, exist_ok=True)

    # Caminhos completos para os arquivos
    csv_file_path = os.path.join(result_dir, "best_solution.csv")
    xlsx_file_path = os.path.join(result_dir, "best_solution.xlsx")

    try:
        # Salva os resultados em arquivo CSV.
        dataframe.to_csv(csv_file_path, index=False)
        print(f"Arquivo CSV salvo com sucesso em: {csv_file_path}")

        # Salva os resultados em arquivo Excel.
        dataframe.to_excel(xlsx_file_path, index=False)
        print(f"Arquivo Excel salvo com sucesso em: {xlsx_file_path}")
    except Exception as e:
        print(f"Erro ao salvar os arquivos: {e}")

# Função para executar o algoritmo genético no proprio arquivo
def run_genetic_algorithm(operators, orders, population_size=50, generations=100, 
                          mutation_rate=0.4, elitism_size=5, reinitalize_interval=10, days=5):
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
    # Inicializa operadores e ordens iniciais.
    operators, orders = create_initial_data(params["_N_ORDERS"], params["_N_OPERATORS"])
    
    # Gera populaçao inicial com base nos operadores e ordens iniciais.
    population = [create_initial_solution(operators, orders, params["_DAYS"]) 
                  for _ in range(params["_POPULATION_SIZE"])]

    # Salva os melhores fitness e geraçoes para plottar.
    best_fitness_values = []
    best_schedules = []

    for generation in range(generations):
                
        # Ajuste na taxa de mutação conforme o número da geração
        mutation_rate = mutation_rate - (generation / generations) * 0.05  # Reduz a taxa de mutação
        if mutation_rate < 0.05:
            mutation_rate = 0.05  # Taxa mínima de mutação

        # population = sorted(population, key=calculate_fitness).
        population = sorted(population, reverse=True, key=lambda individual: 
                            calculate_fitness(individual, operators, orders))

        # Exibição da aptidão da melhor solução da geração.
        best_fitness = calculate_fitness(population[0], operators, orders)
        best_schedule = population[0]
        best_fitness_values.append(best_fitness)
        best_schedules.append(best_schedule)
        
        # Geração da nova população.
        new_population = [population[0]]    # Preserva o melhor indivíduo (elitismo)
        while len(new_population) < params["_POPULATION_SIZE"]:
            parent1, parent2 = random.choices(population[:params["_ELITISM_SIZE"]], k=2)
            child = crossover(parent1, parent2, operators, orders, params["_DAYS"])
            child = mutate(child, operators, orders, params["_MUTATION_RATE"], params["_DAYS"])
            new_population.append(child)

        # Reinicialização da população a cada 'reinitalize_interval' gerações.
        # Esta função aumenta a variabilidade na população, trocando a metade da populaçao com menor fit.
        if generation % params["_REINITIALIZE_INTERVAL"] == 0:
            num_to_reinitialize = params["_POPULATION_SIZE"] // 2
            new_population[-num_to_reinitialize:] = [
                create_initial_solution(operators, orders, params["_DAYS"]) 
                for _ in range(num_to_reinitialize)]

        population = new_population

    # Após as gerações, mostra a melhor solução.
    best_solution = max(best_schedules, key=lambda solution: 
                            calculate_fitness(solution, operators, orders))
    
    print(f"\nBest solution fitness: {calculate_fitness(best_solution, operators, orders):.2f}")

    # Conversão dos dados da melhor solução encontrada em Dataframe.
    final_df, unassigned_orders = solution_to_dataframe(best_solution, operators, orders)
    imprimir_resultados_alocacao(final_df, unassigned_orders, operators, orders)
    
    return final_df, unassigned_orders
 
# Para rodar o algoritmo diretamente sem importar para outros arquivos
if __name__ == '__main__':
    params = {
        "_N_ORDERS" : 100,
        "_N_OPERATORS" : 10,
        "_POPULATION_SIZE" : 50,
        "_GENERATIONS" : 50,
        "_MUTATION_RATE" : 0.3,
        "_ELITISM_SIZE" : 5,
        "_REINITIALIZE_INTERVAL" : 10,
        "_DAYS": 5,   # Dias a serem organizados pelo algoritmo.
    }
    best_solution_df, unassigned_orders = run_genetic_algorithm(params["_N_OPERATORS"], params["_N_ORDERS"], params["_POPULATION_SIZE"], params["_GENERATIONS"],
                           params["_MUTATION_RATE"], params["_ELITISM_SIZE"], params["_REINITIALIZE_INTERVAL"],params["_DAYS"])
    
    # Salva os resultados em arquivo.
    salvar_arquivos(best_solution_df)