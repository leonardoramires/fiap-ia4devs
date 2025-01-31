import os
import random
import pandas as pd

# Função para criar os dados de exemplo
def create_initial_data(n_operators=None, n_orders=None, max_days=5):
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
            num_skills = random.randint(1, 2)
            op_skills = random.sample(skills, num_skills)
            level = random.choice(skills_level)
            shift = random.choice(["manhã", "tarde", "noite"])
            hours_per_day = random.randint(7, 9)
            operators[op_id] = {
                "skills": op_skills, 
                "level": level, 
                "shift": shift, 
                "hours_per_day": hours_per_day
            }
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
        for i in range(1, n_orders + 1):
            required_skills = random.sample(skills, random.randint(1, 2))
            os_id = f"os{i}"
            service_orders[os_id] = {
                "required_skills": required_skills,
                "estimated_hours": random.randint(2, 8),
                "priority": random.choice(priority_levels),
                "expected_start_day": random.randint(1, max_days),
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
        meets_minimum (bool): True se o operador atender pelo menos 50% das habilidades, False caso contrário.
        match_percentage(float): a porcentagem de habilidades atendidas.
    """
    matching_skills = set(operator_skills) & set(required_skills)
    
    # Verifica se a porcentagem de habilidades está acima da metade (valor minimo).
    match_percentage = len(matching_skills) / len(required_skills) if required_skills else 1
    
    # Verifica se o operador atende pelo menos 50% das habilidades necessárias
    meets_minimum = match_percentage >= 0.5
    
    return meets_minimum, match_percentage

# Função para calcular a aptidão de uma solução 
def calculate_fitness(solution, operators, orders, max_days=5):
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
    operator_daily_hours = {op_id: {day: 0 for day in range(1, max_days+1)}
                            for op_id in operators.keys()}
    
    # Itera sobre cada ordem na solução.
    for order_id, allocation in solution["orders"].items():
        day = allocation["day"]
        operator_id = allocation["operator"]
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
            penalty = 5 * days_late * priority_multiplier
            fitness -= penalty
           
        # Aumenta a pontuação com base na compatibilidade de habilidades e prioridade.
        fitness += skill_match_score * priority_multiplier
       
    # Verifica o excesso de horas trabalhadas por operador por dia.
    for operator_id, daily_hours in operator_daily_hours.items():
        for day, hours_worked in daily_hours.items():
            excess_hours = max(0, hours_worked - operators[operator_id]["hours_per_day"])  # Garante que excess_hours não seja negativo.
            if excess_hours > 0:
                penalty = 5 * excess_hours
                fitness -= penalty
               
    solution["fitness"] = fitness
    return fitness  # Retorna a pontuação de aptidão final da solução.

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

    for order_id, allocation in solution["orders"].items():
        day = allocation["day"]
        operator_id = allocation["operator"]
        current_status = allocation["status"]

        # Verifica se a ordem foi atribuída a algum operador.
        if not operator_id:
            operator_id = "N/A"
        else:
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

# Converte os dados de exemplo em dataframe para facilitar a visualização
def orders_to_dataframe(orders):
    """
    Converte os dados simulados de ordens de serviço em um DataFrame.

    Args:
        orders (dict): Dicionário com ordens de serviço, incluindo habilidades exigidas, horas estimadas, prioridade, inicio_esperado e status.

    Returns:
        pd.DataFrame: DataFrame com os dados das ordens de serviço.

    Detalhes:
    - O DataFrame das ordens de serviço inclui as colunas: 'id_ordem', 'Serviços', 'horas_estimadas', 'prioridade', 
        'inicio_esperado', 'status'.
    """

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

    return service_orders_df

# Função para imprimir na tela o resultado do algoritmo
def imprimir_resultados_alocacao(df, unassigned_orders, orders, name):
    """
    Imprime um relatório detalhado da alocação de ordens de serviço.

    Args:
        df (pd.DataFrame): DataFrame com a solução de alocação
        unassigned_orders (list): Lista de ordens não alocadas
        operators (dict): Dicionário com informações dos operadores
        orders (dict): Dicionário com informações das ordens
    """
    # Configuração do arquivo de saída
    script_dir = os.path.dirname(os.path.abspath(__file__))
    result_dir = os.path.join(script_dir, "./../resultados")
    os.makedirs(result_dir, exist_ok=True)
    report_file_path = os.path.join(result_dir, f"relatorio_alocacao_{name}.txt")

    # Função auxiliar para escrever tanto no console quanto no arquivo
    def write_output(text):
        print(text)
        with open(report_file_path, 'a', encoding='utf-8') as f:
            f.write(text + '\n')

    # Limpa o arquivo se ja existir
    with open(report_file_path, 'w', encoding='utf-8') as f:
        f.write('')

    write_output("\n" + "=" * 80)
    write_output("RELATÓRIO DETALHADO DE ALOCAÇÃO".center(80))
    write_output("=" * 80)

    # 1. Estatísticas Gerais
    total_ordens = len(orders)
    ordens_alocadas = len(df['id_ordem'].unique())
    ordens_nao_alocadas = len(unassigned_orders)

    write_output("\n1. ESTATÍSTICAS GERAIS")
    write_output("-" * 40)
    write_output(f"Total de Ordens: {total_ordens}")
    write_output(
        f"Ordens Alocadas: {ordens_alocadas} ({(ordens_alocadas / total_ordens) * 100:.1f}%)")
    write_output(f"Ordens Não Alocadas: {ordens_nao_alocadas}")

    # 2. Análise por Prioridade
    write_output("\n2. ANÁLISE POR PRIORIDADE")
    write_output("-" * 40)
    for prioridade in ['urgente', 'alta', 'média', 'baixa']:
        count = len(df[df['prioridade'] == prioridade])
        if count > 0:
            write_output(
                f"Prioridade {prioridade:8s}: {count:3d} ordens ({(count / ordens_alocadas) * 100:5.1f}%)")

    # 3. Análise por Operador
    write_output("\n3. ANÁLISE POR OPERADOR")
    write_output("-" * 40)
    for operador in df['id_operador'].unique():
        df_op = df[df['id_operador'] == operador]
        horas_total = df_op['horas_estimadas'].sum()
        horas_disp = df_op['horas_disponiveis'].iloc[0]
        percentual = (horas_total / (horas_disp * 5)) * 100
        n_ordens = len(df_op)
        write_output(f"Operador {operador}:")
        write_output(f"  - Ordens alocadas: {n_ordens}")
        write_output(
            f"  - Horas alocadas: {horas_total:.1f}h de {horas_disp * 5:.1f}h ({percentual:.1f}%)")
    # 4. Análise de Prazos
    write_output("\n4. ANÁLISE DE PRAZOS")
    write_output("-" * 40)

    ordens_no_prazo = len(df[df['atraso'] <= 0])
    write_output(
        f"Ordens no Prazo: {ordens_no_prazo} ({(ordens_no_prazo / ordens_alocadas) * 100:.1f}%)")

    if len(df[df['atraso'] > 0]) > 0:
        write_output("\nDetalhamento dos Atrasos:")
        for _, row in df[df['atraso'] > 0].iterrows():
            write_output(
                f"  Ordem {row['id_ordem']}: {row['atraso']} dias de atraso (Prioridade: {row['prioridade']})")

    # 5. Análise de Atendimentos por Fitness
    write_output("\n5. ANÁLISE DE ATENDIMENTOS POR FITNESS")
    write_output("-" * 40)

    # Análise de atendimento baseada nos critérios do fitness
    atendimentos = {
        'total': [],
        'parcial': [],
        'inadequado': []
    }

    for _, row in df.iterrows():
        # Converte strings de habilidades em conjuntos para comparação
        required_skills = set(row['Serviços'].split(" | "))
        operator_skills = set(row['habilidades_operador'].split(" | "))

        # Calcula o percentual de match de habilidades
        matching_skills = len(required_skills.intersection(operator_skills))
        skill_match_percent = matching_skills / len(required_skills)

        # Verifica condições de atendimento
        dentro_prazo = row['atraso'] <= 0
        horas_ok = row['horas_estimadas'] <= row['horas_disponiveis']

        # Classifica o atendimento
        if skill_match_percent == 1 and dentro_prazo and horas_ok:
            atendimentos['total'].append(row['id_ordem'])
        elif skill_match_percent >= 0.5:
            atendimentos['parcial'].append(row['id_ordem'])
        else:
            atendimentos['inadequado'].append(row['id_ordem'])

    # Imprime estatísticas gerais
    total_atendidos = len(atendimentos['total'])
    parcial_atendidos = len(atendimentos['parcial'])
    inadequados = len(atendimentos['inadequado'])

    write_output("Estatísticas Gerais de Atendimento:")
    write_output(f"  - Atendimento Total:    {total_atendidos:3d} ordens ({(total_atendidos / ordens_alocadas) * 100:5.1f}%)")
    write_output(f"  - Atendimento Parcial:  {parcial_atendidos:3d} ordens ({(parcial_atendidos / ordens_alocadas) * 100:5.1f}%)")
    write_output(f"  - Atendimento Inadequado: {inadequados:3d} ordens ({(inadequados / ordens_alocadas) * 100:5.1f}%)")

    # Análise detalhada por tipo de atendimento
    write_output("\nDetalhamento dos Atendimentos:")

    if atendimentos['total']:
        write_output("\nOrdens com Atendimento Total:")
        for ordem_id in atendimentos['total']:
            ordem = df[df['id_ordem'] == ordem_id].iloc[0]
            write_output(f"  ✓ Ordem {ordem_id}: "
                         f"Skills={ordem['Serviços']}, "
                         f"Operador={ordem['id_operador']}, "
                         f"Inicio Esperado={ordem['inicio_esperado']}, "
                         f"Dia Alocado={ordem['dia']}")

    if atendimentos['parcial']:
        write_output("\nOrdens com Atendimento Parcial:")
        for ordem_id in atendimentos['parcial']:
            ordem = df[df['id_ordem'] == ordem_id].iloc[0]
            write_output(f"  ⚠ Ordem {ordem_id}: "
                         f"Skills={ordem['Serviços']}, "
                         f"Operador={ordem['id_operador']} ({ordem['habilidades_operador']}), "
                         f"Inicio Esperado={ordem['inicio_esperado']}, "
                         f"Dia Alocado={ordem['dia']}")

    if atendimentos['inadequado']:
        write_output("\nOrdens com Atendimento Inadequado:")
        for ordem_id in atendimentos['inadequado']:
            ordem = df[df['id_ordem'] == ordem_id].iloc[0]
            write_output(f"  ✗ Ordem {ordem_id}: "
                         f"Skills={ordem['Serviços']}, "
                         f"Operador={ordem['id_operador']} ({ordem['habilidades_operador']}), "
                         f"Inicio Esperado={ordem['inicio_esperado']}, "
                         f"Dia Alocado={ordem['dia']}")

    # 6. Análise por Dia
    write_output("\n6. DISTRIBUIÇÃO POR DIA")
    write_output("-" * 40)
    for dia in sorted(df['dia'].unique()):
        df_dia = df[df['dia'] == dia]
        write_output(f"\nDia {dia}:")
        write_output(f"  - Total de Ordens: {len(df_dia)}")
        write_output(
            f"  - Horas Alocadas: {df_dia['horas_estimadas'].sum():.1f}h")
        write_output(f"  - Distribuição de Prioridades:")
        for prioridade in ['urgente', 'alta', 'média', 'baixa']:
            count = len(df_dia[df_dia['prioridade'] == prioridade])
            if count > 0:
                write_output(f"    * {prioridade:8s}: {count:3d}")

    # 7. Ordens Não Alocadas
    if unassigned_orders:
        write_output("\n7. ORDENS NÃO ALOCADAS")
        write_output("-" * 40)
        write_output(f"Total de ordens não alocadas: {len(unassigned_orders)}")

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
                write_output(
                    f"\nPrioridade {priority}: {len(orders_list)} ordens")
                for order_id in orders_list:
                    order = orders[order_id]
                    write_output(f"  - {order_id}: "
                                 f"Skills={', '.join(order['required_skills'])}, "
                                 f"Horas={order['estimated_hours']}, "
                                 f"Prazo={order['expected_start_day']}")

    write_output("\n" + "=" * 80)
    write_output("FIM DO RELATÓRIO".center(80))
    write_output("=" * 80)

    # Retorna métricas principais para uso no algoritmo genético
    return {
        'total_ordens': total_ordens,
        'ordens_alocadas': ordens_alocadas,
        'ordens_nao_alocadas': ordens_nao_alocadas,
        'taxa_alocacao': (ordens_alocadas/total_ordens)*100,
        'matches_perfeitos': total_atendidos,
        'taxa_matches_perfeitos': (total_atendidos/ordens_alocadas)*100 if ordens_alocadas > 0 else 0,
        'compatibilidade_media': df['compatibilidade_os_op'].mean()*100 if not df.empty else 0,
        'ordens_no_prazo': ordens_no_prazo,
        'taxa_cumprimento_prazo': (ordens_no_prazo/ordens_alocadas)*100 if ordens_alocadas > 0 else 0,
        'atendimento_total': total_atendidos,
        'atendimento_parcial': parcial_atendidos,
        'atendimento_inadequado': inadequados,
        'taxa_atendimento_total': (total_atendidos/ordens_alocadas)*100 if ordens_alocadas > 0 else 0,
        'taxa_atendimento_parcial': (parcial_atendidos/ordens_alocadas)*100 if ordens_alocadas > 0 else 0,
        'taxa_atendimento_inadequado': (inadequados/ordens_alocadas)*100 if ordens_alocadas > 0 else 0
    }

def salvar_arquivos(dataframe, algorithm_name = 'genetic_algorithm'):
    # Diretório do script em execução
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Defina o diretório onde os arquivos serão salvos
    result_dir = os.path.join(script_dir, f"./../resultados_{algorithm_name}")

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