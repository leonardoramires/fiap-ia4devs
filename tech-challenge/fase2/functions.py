import random
import time
import pandas as pd

# Função para criar os dados de exemplo
def create_sample_data(n_orders=None, n_operators=None):
    """
    Cria dados simulados de operadores e ordens de serviço. Se 'n_operators' for fornecido, gera operadores e ordens automaticamente.

    Args:
        n_orders (int): Número de ordens de serviço a serem criadas.
        n_operators (int, opcional): Número de operadores a serem gerados automaticamente. Se não fornecido, usa operadores predefinidos.

    Returns:
        tuple: Um dicionário com operadores e suas habilidades e outro com ordens de serviço.

    Detalhes:
    - Se 'n_operators' for fornecido, serão gerados operadores aleatórios com habilidades e horários.
    - As ordens de serviço são geradas com habilidades, horas estimadas, prioridade e prazo de forma aleatória.
    """
    skills = ["pintura", "elétrica", "alvenaria", "hidráulica", "solda"]
    skill_levels = ["júnior", "pleno", "sênior", "especialista"]
    priority_levels = ["baixa", "média", "alta", "urgente"]

    # Geração automática de operadores, se n_operators for fornecido
    if n_operators:
        operators = {}
        for i in range(1, n_operators + 1):
            op_id = f"op{i}"
            num_skills = random.randint(2, 3)
            op_skills = random.sample(skills, num_skills)
            level = random.choice(skill_levels)
            shift = random.choice(["manhã", "tarde", "noite"])
            hours_per_day = random.randint(7, 9)
            operators[op_id] = {"skills": op_skills, "level": level, "shift": shift, "hours_per_day": hours_per_day}
    else:
        # Dados dos operadores predefinidos
        operators = {
            "op1": {"skills": ["pintura", "elétrica"], "level": "sênior", "shift": "manhã", "hours_per_day": 8},
            "op2": {"skills": ["hidráulica", "alvenaria"], "level": "pleno", "shift": "tarde", "hours_per_day": 8},
            "op3": {"skills": ["solda", "pintura"], "level": "sênior", "shift": "noite", "hours_per_day": 9},
            "op4": {"skills": ["elétrica", "hidráulica"], "level": "júnior", "shift": "manhã", "hours_per_day": 7},
        }

    # Geração dinâmica de ordens de serviço
    if n_orders:
        service_orders = {}
        for i in range(n_orders):
            required_skills = random.sample(skills, random.randint(1, 2))
            service_orders[f"ordem{i+1}"] = {
                "required_skills": required_skills,
                "estimated_hours": random.randint(2, 8),
                "priority": random.choice(priority_levels),
                "deadline_days": random.randint(1, 5),
            }
    else:
        service_orders = {
            'ordem1': {'required_skills': ['solda', 'alvenaria'], 'estimated_hours': 2, 'priority': 'média', 'deadline_days': 3},
            'ordem2': {'required_skills': ['pintura', 'hidráulica'], 'estimated_hours': 8, 'priority': 'alta', 'deadline_days': 2},
            'ordem3': {'required_skills': ['hidráulica'], 'estimated_hours': 5, 'priority': 'urgente', 'deadline_days': 5},
            'ordem4': {'required_skills': ['hidráulica', 'pintura'], 'estimated_hours': 2, 'priority': 'urgente', 'deadline_days': 1},
            'ordem5': {'required_skills': ['alvenaria'], 'estimated_hours': 5, 'priority': 'alta', 'deadline_days': 3},
            'ordem6': {'required_skills': ['alvenaria'], 'estimated_hours': 7, 'priority': 'baixa', 'deadline_days': 5},
            'ordem7': {'required_skills': ['elétrica'], 'estimated_hours': 7, 'priority': 'baixa', 'deadline_days': 4},
            'ordem8': {'required_skills': ['solda'], 'estimated_hours': 8, 'priority': 'baixa', 'deadline_days': 5},
            'ordem9': {'required_skills': ['pintura'], 'estimated_hours': 3, 'priority': 'baixa', 'deadline_days': 4},
            'ordem10': {'required_skills': ['alvenaria', 'solda'], 'estimated_hours': 2, 'priority': 'alta', 'deadline_days': 5}
        }

    return operators, service_orders

# Converte os dados de exemplo em dataframe para facilitar a visualização
def sample_to_dataframe(operators, service_orders):
    """
    Converte os dados simulados de operadores e ordens de serviço em DataFrames.

    Args:
        operators (dict): Dicionário com dados dos operadores, incluindo suas habilidades, turnos e horas de trabalho.
        service_orders (dict): Dicionário com ordens de serviço, incluindo habilidades exigidas, horas estimadas, prioridade e prazo.

    Returns:
        tuple: Um tuple contendo dois DataFrames:
            - operators_df: DataFrame com os dados dos operadores.
            - service_orders_df: DataFrame com os dados das ordens de serviço.

    Detalhes:
    - O DataFrame dos operadores inclui as colunas: 'operator_id', 'skills', 'level', 'shift', 'hours_per_day'.
    - O DataFrame das ordens de serviço inclui as colunas: 'order_id', 'required_skills', 'estimated_hours', 'priority', 'deadline_days'.
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
            "deadline_days": details["deadline_days"]
        })

    service_orders_df = pd.DataFrame(service_orders_data)

    return operators_df, service_orders_df

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

# Função para validar se as habilidades do operador atendem pelo menos 50% das habilidades da ordem
def meets_minimum_skills(operator_skills, required_skills):
    """
    Verifica se o operador atende pelo menos 50% das habilidades necessárias para a ordem.

    Args:
        operator_skills (list): Habilidades do operador.
        required_skills (list): Habilidades exigidas pela ordem.

    Returns:
        bool: True se o operador atender pelo menos 50% das habilidades, False caso contrário.
    """
    matching_skills = sum(1 for skill in required_skills if skill in operator_skills)
    return matching_skills / len(required_skills) >= 0.5

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

# Função para calcular a aptidão de uma solução
def calculate_fitness(solution, operators, orders):
    """
    Calcula a pontuação de aptidão de uma solução. A função avalia como uma solução de alocação de ordens a operadores
    é eficaz, levando em consideração a compatibilidade das habilidades, o cumprimento de prazos e o excesso de horas
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
        2. **Cumprimento do prazo**: A solução penaliza ordens que não são completadas dentro do prazo estipulado pela ordem de serviço.
        3. **Excesso de horas**: Penaliza a alocação de mais horas do que a capacidade diária do operador.

    Penalidades:
    - **Compatibilidade de habilidades**: Quando a habilidade de um operador não é adequada à ordem, a pontuação é penalizada. A penalidade depende do nível de habilidade do operador em comparação com o nível necessário para a ordem.
    - **Cumprimento do prazo**: Se a ordem não for completada até o dia limite, é aplicada uma penalidade proporcional à quantidade de dias de atraso e à prioridade da ordem.
    - **Excesso de horas**: Se a soma das horas estimadas para a ordem ultrapassar as horas trabalhadas disponíveis para o operador em um dia, uma penalidade por excesso de horas será aplicada.
    - **

    A pontuação de aptidão final é a soma das pontuações de compatibilidade, penalidades de atraso e excesso de horas.
    """
    fitness = 0  # Inicia a pontuação de aptidão com zero.

    # Itera sobre cada dia da solução (planejamento).
    for day, daily_assignments in solution.items():
        # Para cada operador e as ordens alocadas a ele nesse dia.
        for operator_id, assigned_orders in daily_assignments.items():
            operator = operators[operator_id]  # Obtém as informações do operador.
            daily_hours = 0  # Variável para acumular as horas trabalhadas nesse dia.

            # Avalia cada ordem alocada ao operador no dia atual.
            for order_id in assigned_orders:
                order = orders[order_id]  # Obtém as informações da ordem de serviço.
                daily_hours += order["estimated_hours"]  # Acumula as horas estimadas para as ordens.

                # Avaliação de compatibilidade de habilidades: Como as habilidades do operador atendem aos requisitos da ordem.
                skill_match_score = 0
                if meets_minimum_skills(operator["skills"], order["required_skills"]):
                    skill_match_score += 10
                else:
                    skill_match_score -= 10

                # Avaliação da prioridade e do cumprimento do prazo:
                priority_multiplier = priority_to_number(order["priority"])  # Multiplicador de prioridade para penalidades e bônus.

                # Se a ordem foi concluída após o prazo, penaliza a solução:
                if day > order["deadline_days"]:  # Se o dia atual ultrapassa o prazo da ordem.
                    days_late = day - order["deadline_days"]  # Quantidade de dias de atraso.
                    fitness -= 5 * priority_multiplier * days_late  # Penaliza com base na prioridade e atraso.

                # Aumenta a pontuação de aptidão com base na compatibilidade de habilidades e na prioridade.
                fitness += skill_match_score * priority_multiplier

            # Verifica se o operador trabalhou mais horas do que sua capacidade diária.
            if daily_hours > operator["hours_per_day"]:  # Se o total de horas diárias for excedido.
                excess_hours = daily_hours - operator["hours_per_day"]  # Excesso de horas trabalhadas.
                fitness -= 5 * excess_hours  # Penaliza com base no excesso de horas trabalhadas.

    return fitness  # Retorna a pontuação de aptidão final da solução.

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


def mutate(solution, operators, orders, mutation_rate=0.1):
    """
    Realiza a mutação em uma solução, aceitando apenas mutações benéficas.

    Args:
        solution (dict): A solução atual, contendo a alocação de ordens a operadores por dia.
        operators (dict): Dicionário de operadores, contendo suas habilidades e horários.
        orders (dict): Dicionário de ordens de serviço, contendo as habilidades necessárias, horas estimadas, etc.
        mutation_rate (float): Taxa de mutação, indicando a probabilidade de ocorrer uma mutação (entre 0 e 1).

    Returns:
        dict: A solução mutada, se a mutação for benéfica, caso contrário, retorna a solução original.

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

# Função para converter a solução final em um DataFrame
def solution_to_dataframe(solution, operators, orders):
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
      prioridade e prazo.
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
                    "prazo": order["deadline_days"]
                }
                data.append(row)

    df = pd.DataFrame(data)
    unassigned_orders = list(set(orders.keys() - set(df["id_ordem"].unique())))
    return df, unassigned_orders

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
    df['atraso'] = df['dia'] - df['prazo']
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

    df['compatibilidade'] = df.apply(verificar_compatibilidade, axis=1)
    matches_perfeitos = len(df[df['compatibilidade'] == 1])
    
    print(f"Matches Perfeitos: {matches_perfeitos} ({(matches_perfeitos/ordens_alocadas)*100:.1f}%)")
    print(f"Compatibilidade Média: {df['compatibilidade'].mean()*100:.1f}%")

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
                          f"Prazo={order['deadline_days']}")

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
        'compatibilidade_media': df['compatibilidade'].mean()*100 if not df.empty else 0,
        'ordens_no_prazo': ordens_no_prazo,
        'taxa_cumprimento_prazo': (ordens_no_prazo/ordens_alocadas)*100 if ordens_alocadas > 0 else 0
    }

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

        # Exibição da aptidão da melhor solução da geração
        best_fitness = max(fitness_scores)
        print(f"\nGeneration {generation + 1}/{generations} - Best Fitness: {best_fitness:.2f} - Mutation Rate: {mutation_rate:.4f}")
        time.sleep(0.1)  # Delay para animação

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
    # imprimir_resultados_alocacao(df, unassigned_orders, operators, orders)
    
    return df, unassigned_orders