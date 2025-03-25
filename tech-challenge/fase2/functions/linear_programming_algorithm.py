import pulp
from common_functions import *

def linear_programming_allocation(operators, orders, days=5):
    """
    Realiza a alocação de ordens de serviço usando Programacao Linear.

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
    prob += pulp.lpSum(priority_to_number(orders[order]["priority"]) * x[day, op, order] for day in range(days) for op in operators for order in orders)

    # Restrição: cada ordem deve ser atribuída a exatamente um operador em um dia
    for order_id in orders:
        prob += pulp.lpSum(x[day, op, order_id] for day in range(days) for op in operators) == 1

    # Restrição: as habilidades do operador devem atender às habilidades necessárias para a ordem
    for day in range(days):
        for operator_id in operators:
            for order_id in orders:
                if not meets_minimum_skills(operators[operator_id]["skills"], orders[order_id]["required_skills"]):
                    prob += x[day, operator_id, order_id] == 0

    # Restrição: as horas de trabalho do operador não devem exceder as horas disponíveis
    for day in range(days):
        for operator_id in operators:
            prob += pulp.lpSum(orders[order]["estimated_hours"] * x[day, operator_id, order] for order in orders) <= operators[operator_id]["hours_per_day"]

    # Resolve o problema sem exibir mensagens no terminal
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Inicializa a solução
    solution = {
        "orders": {},
        "fitness": 0
    }

    # Cria a solução a partir das variáveis de decisão
    for day in range(days):
        for operator_id in operators:
            for order_id in orders:
                if pulp.value(x[day, operator_id, order_id]) == 1:
                    # Calcula a quantidade de dias em atraso, se late_order > 0 = atraso.. 
                    late_order = day - orders[order_id]["expected_start_day"]

                    order_status = "atendida"
                    if late_order > 0:
                        order_status = "atrasada"

                    # Atualiza a solução para a OS atual
                    solution["orders"][order_id] = {"day": day+1, "operator": operator_id, "status": order_status}

    return solution