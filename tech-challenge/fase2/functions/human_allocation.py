from common_functions import *

def human_allocation_execution(operators, orders, days=5):
    """
    Realiza a alocação de ordens de serviço separando-as em grupos de prioridade e atribuindo-as aos operadores.

    Args:
        operators (dict): Dicionário de operadores, contendo suas habilidades e horários.
        orders (dict): Dicionário de ordens de serviço, contendo as habilidades necessárias, horas estimadas, etc.
        days (int): Número de dias do planejamento.

    Returns:
        dict: Solução de alocação de ordens a operadores por dia.
    """
    # Inicializa a solução
    # solution = {day: {op: [] for op in operators.keys()} for day in range(days)}
    solution = {
        "orders": {},
        "fitness": 0
    }

    # Separa as ordens em grupos de prioridade
    priority_groups = {}
    for order_id, order in orders.items():
        priority = order['priority']
        if priority not in priority_groups:
            priority_groups[priority] = []
        priority_groups[priority].append((order_id, order))

    # Ordena as prioridades (do mais alto para o mais baixo)
    sorted_priorities = sorted(priority_groups.keys(), key=priority_to_number, reverse=True)

    # Atribui cada ordem ao operador mais adequado disponível, por grupo de prioridade
    for priority in sorted_priorities:
        for order_id, order in priority_groups[priority]:
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
