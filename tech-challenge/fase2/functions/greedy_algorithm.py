from common_functions import *

def greedy_allocation(operators, orders, days=5):
    """
    Realiza a alocação de ordens de serviço usando o algoritmo guloso.

    Args:
        operators (dict): Dicionário de operadores, contendo suas habilidades e horários.
        orders (dict): Dicionário de ordens de serviço, contendo as habilidades necessárias, horas estimadas, etc.
        days (int): Número de dias do planejamento.

    Returns:
        dict: Solução de alocação de ordens a operadores por dia.
    """
    # Ordena as ordens de serviço por prioridade (decrescente) e prazo (crescente)
    sorted_orders = sorted(orders.items(), key=lambda x: (-priority_to_number(x[1]['priority']), x[1]['expected_start_day']))

    # Inicializa a solução
    solution = {
        "orders": {},
        "fitness": 0
    }

    # Atribui cada ordem ao operador mais adequado disponível
    for order_id, order in sorted_orders:
        assigned = False
        for day in range(1, days+1):
            for operator_id, operator in operators.items():
                if meets_minimum_skills(operator["skills"], order["required_skills"]):
                    # Verifica se o operador tem horas disponíveis no dia
                    total_hours = sum(
                        order["estimated_hours"]
                        for assigned_order_id, order in orders.items()
                        if assigned_order_id in solution["orders"] and
                           solution["orders"][assigned_order_id]["operator"] == operator_id and
                           solution["orders"][assigned_order_id]["day"] == day
                    )
                    if total_hours + order["estimated_hours"] <= operator["hours_per_day"]:
                        solution["orders"][order_id] = {"day": day, "operator": operator_id, "status": "atendida"}
                        assigned = True
                        break
            if assigned:
                break

    return solution
