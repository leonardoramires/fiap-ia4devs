import pandas as pd
import pulp
import functions as F

def linear_programming_allocation(operators, orders, days=5):
    """
    Realiza a alocação de ordens de serviço usando Programação Linear.

    Args:
        operators (dict): Dicionário de operadores, contendo suas habilidades e horários.
        orders (dict): Dicionário de ordens de serviço, contendo as habilidades necessárias, horas estimadas, etc.
        days (int): Número de dias do planejamento.

    Returns:
        dict: Solução de alocação de ordens a operadores por dia.
    """
    # Cria o problema de otimização
    prob = pulp.LpProblem("Order_Allocation", pulp.LpMaximize)

    # Cria as variáveis de decisão
    x = pulp.LpVariable.dicts("x", ((day, op, order) for day in range(days) for op in operators for order in orders), cat='Binary')

    # Função objetivo: maximizar a aptidão total
    prob += pulp.lpSum(F.priority_to_number(orders[order]["priority"]) * x[day, op, order] for day in range(days) for op in operators for order in orders)

    # Restrição: cada ordem deve ser atribuída a exatamente um operador em um dia
    for order in orders:
        prob += pulp.lpSum(x[day, op, order] for day in range(days) for op in operators) == 1

    # Restrição: as habilidades do operador devem atender às habilidades necessárias para a ordem
    for day in range(days):
        for op in operators:
            for order in orders:
                if not F.meets_minimum_skills(operators[op]["skills"], orders[order]["required_skills"]):
                    prob += x[day, op, order] == 0

    # Restrição: as horas de trabalho do operador não devem exceder as horas disponíveis
    for day in range(days):
        for op in operators:
            prob += pulp.lpSum(orders[order]["estimated_hours"] * x[day, op, order] for order in orders) <= operators[op]["hours_per_day"]

    # Resolve o problema sem exibir mensagens no terminal
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Cria a solução a partir das variáveis de decisão
    solution = {day: {op: [] for op in operators} for day in range(days)}
    for day in range(days):
        for op in operators:
            for order in orders:
                if pulp.value(x[day, op, order]) == 1:
                    solution[day][op].append(order)

    return solution