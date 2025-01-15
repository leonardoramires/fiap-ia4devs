import pandas as pd
import functions as F

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
    sorted_orders = sorted(orders.items(), key=lambda x: (-F.priority_to_number(x[1]['priority']), x[1]['expected_start_day']))

    # Inicializa a solução
    solution = {day: {op: [] for op in operators.keys()} for day in range(days)}

    # Atribui cada ordem ao operador mais adequado disponível
    for order_id, order in sorted_orders:
        assigned = False
        for day in range(days):
            for operator_id, operator in operators.items():
                if F.meets_minimum_skills(operator["skills"], order["required_skills"]):
                    # Verifica se o operador tem horas disponíveis no dia
                    total_hours = sum(orders[order_id]["estimated_hours"] for order_id in solution[day][operator_id])
                    if total_hours + order["estimated_hours"] <= operator["hours_per_day"]:
                        solution[day][operator_id].append(order_id)
                        assigned = True
                        break
            if assigned:
                break

    return solution

