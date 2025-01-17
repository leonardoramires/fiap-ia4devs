import random
import pandas as pd

# Função para criar os dados de exemplo
def create_sample_data(n_orders=None, n_operators=None):
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

    # Geração automática de operadores, se n_operators for fornecido
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
                "expected_start_day": random.randint(1, 5),
                "status": "não_atendida",
            }
    else:
        service_orders = {
            'ordem1': {'required_skills': ['solda', 'alvenaria'], 'estimated_hours': 2, 'priority': 'média', 'expected_start_day': 3, 'status':'não_atendida'},
            'ordem2': {'required_skills': ['pintura', 'hidráulica'], 'estimated_hours': 8, 'priority': 'alta', 'expected_start_day': 2, 'status':'não_atendida'},
            'ordem3': {'required_skills': ['hidráulica'], 'estimated_hours': 5, 'priority': 'urgente', 'expected_start_day': 5, 'status':'não_atendida'},
            'ordem4': {'required_skills': ['hidráulica', 'pintura'], 'estimated_hours': 2, 'priority': 'urgente', 'expected_start_day': 1, 'status':'não_atendida'},
            'ordem5': {'required_skills': ['alvenaria'], 'estimated_hours': 5, 'priority': 'alta', 'expected_start_day': 3, 'status':'não_atendida'},
            'ordem6': {'required_skills': ['alvenaria'], 'estimated_hours': 7, 'priority': 'baixa', 'expected_start_day': 5, 'status':'não_atendida'},
            'ordem7': {'required_skills': ['elétrica'], 'estimated_hours': 7, 'priority': 'baixa', 'expected_start_day': 4, 'status':'não_atendida'},
            'ordem8': {'required_skills': ['solda'], 'estimated_hours': 8, 'priority': 'baixa', 'expected_start_day': 5, 'status':'não_atendida'},
            'ordem9': {'required_skills': ['pintura'], 'estimated_hours': 3, 'priority': 'baixa', 'expected_start_day': 4, 'status':'não_atendida'},
            'ordem10': {'required_skills': ['alvenaria', 'solda'], 'estimated_hours': 2, 'priority': 'alta', 'expected_start_day': 5, 'status':'não_atendida'}
        }

    return operators, service_orders

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
    - **


    TODO:
    aplicar o percentual de match de habilidades no score

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

                # Avaliação da prioridade e do cumprimento do inicio_esperado:
                priority_multiplier = priority_to_number(order["priority"])  # Multiplicador de prioridade para penalidades e bônus.

                # Se a ordem foi concluída após o inicio_esperado, penaliza a solução:
                if day > order["expected_start_day"]:  # Se o dia atual ultrapassa o inicio_esperado da ordem.
                    days_late = day - order["expected_start_day"]  # Quantidade de dias de atraso.
                    fitness -= 5 * priority_multiplier * days_late  # Penaliza com base na prioridade e atraso.

                # Aumenta a pontuação de aptidão com base na compatibilidade de habilidades e na prioridade.
                fitness += skill_match_score * priority_multiplier

            # Verifica se o operador trabalhou mais horas do que sua capacidade diária.
            if daily_hours > operator["hours_per_day"]:  # Se o total de horas diárias for excedido.
                excess_hours = daily_hours - operator["hours_per_day"]  # Excesso de horas trabalhadas.
                fitness -= 5 * excess_hours  # Penaliza com base no excesso de horas trabalhadas.

    return fitness  # Retorna a pontuação de aptidão final da solução.

# Função para tranformar a solução encontrada em Dtaframe
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
      prioridade e inicio_esperado, além das novas colunas de compatibilidade e habilidades não atendidas.
    """
    data = []
    operator_daily_hours = {}

    for day, assignments in solution.items():
        if day not in operator_daily_hours:
            operator_daily_hours[day] = {}

        for operator_id, order_ids in assignments.items():
            if operator_id not in operator_daily_hours[day]:
                operator_daily_hours[day][operator_id] = 0

            for order_id in order_ids:
                order = orders[order_id]
                operator = operators[operator_id]

                # Calcular compatibilidade de habilidades
                required_skills = set(order["required_skills"])
                operator_skills = set(operator["skills"])

                matched_skills = required_skills & operator_skills
                missing_skills = required_skills - operator_skills

                skill_compatibility = len(matched_skills) / len(required_skills) if required_skills else 1.0

                # Verificar compatibilidade do nível com a prioridade
                priority_level_map = {
                    "alta": ["especialista", "sênior"],
                    "urgente": ["especialista", "sênior"],
                    "média": ["especialista", "sênior", "pleno"],
                    "baixa": ["especialista", "sênior", "pleno", "júnior"]
                }

                priority = order["priority"]
                operator_level = operator["level"]

                compatibility_level = (
                    "OK" if operator_level in priority_level_map.get(priority, []) else "NOK"
                )

                # Acumular horas do operador no dia
                operator_daily_hours[day][operator_id] += order["estimated_hours"]
                total_hours = operator_daily_hours[day][operator_id]
                extra_hours = "Sim" if total_hours > operator["hours_per_day"] else "Não"
                total_extra_hours = total_hours - operator["hours_per_day"]
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
                    "inicio_esperado": order["expected_start_day"],
                    "atraso": day + 1 - order["expected_start_day"],
                    "compatibilidade_habilidade": round(skill_compatibility * 100, 2),
                    "habilidades_nao_atendidas": " | ".join(missing_skills),
                    "compatibilidade_nivel_prioridade": compatibility_level,
                    "hora_extra": extra_hours,
                    "total_hora_extra": 0 if total_extra_hours <= 0 else total_extra_hours,
                    "status": order["status"],
                }

                data.append(row)

    df = pd.DataFrame(data)
    unassigned_orders = list(set(orders.keys()) - set(df["id_ordem"].unique()))
    return df, unassigned_orders

def orders_to_dataframe(service_orders):
    """
    Converte um dicionário de ordens de serviço em um DataFrame do pandas.

    Args:
        service_orders (dict): Dicionário contendo os detalhes das ordens de serviço.

    Returns:
        pd.DataFrame: DataFrame contendo os detalhes das ordens de serviço.
    """
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

    return service_orders_df