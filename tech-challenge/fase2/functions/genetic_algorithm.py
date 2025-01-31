import random
import pandas as pd
import copy

from common_functions import *

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

# Função para criação de uma solução inicial
def create_initial_solution(operators, orders, max_days):
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
        "orders": {
            order_id: {"day": None, "operator": None, "status": "não_atendida"}
            for order_id in orders.keys()
        },
        "fitness": 0,
    }
    
    for order_id, order_data in orders.items():
        # Identifica operadores válidos para a ordem com base nas habilidades.
        valid_operators = [
            op_id for op_id, operator in operators.items()
            if meets_minimum_skills(operator["skills"], order_data["required_skills"])[0]
        ]

        if valid_operators:  # Apenas atribui se houver operadores válidos.
            # Atribui a ordem a um dia e operador aleatórios.
            assigned_day = random.randint(1, max_days)
            assigned_operator = random.choice(valid_operators)

            # Calcula a quantidade de dias em atraso, se late_order > 0 = atraso.. 
            late_order = assigned_day - order_data["expected_start_day"]

            # Atualiza a solução para a OS atual
            solution["orders"][order_id]["day"] = assigned_day
            solution["orders"][order_id]["operator"] = assigned_operator
            solution["orders"][order_id]["status"] = "atrasada" if late_order > 0 else "atendida"

    return solution

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
    child = {"orders": {}, "fitness": 0}
    assigned_orders = set()  # Rastreia as ordens já atribuídas.

    # Obtém a lista de ordens para o ponto de crossover.
    orders_parent1 = list(parent1["orders"].keys())
    orders_parent2 = list(parent2["orders"].keys())
    crossover_point = random.randint(1, len(orders_parent1) - 1)

    # Primeiro segmento: Copia as ordens do pai 1 até o ponto de crossover.
    for order_id in orders_parent1[:crossover_point]:
        if order_id in parent1["orders"]:
            order_data = parent1["orders"][order_id]
            operator = order_data["operator"]
            day = order_data["day"]
            status = order_data["status"]

            # Verifica se o operador é compatível e a ordem não foi atribuída.
            if (order_id not in assigned_orders
                and meets_minimum_skills(operators[operator]["skills"], orders[order_id]["required_skills"])[0]
                ):
                child["orders"][order_id] = {"operator": operator, "day": day, "status": status}
                assigned_orders.add(order_id)

    # Segundo segmento: Copia as ordens do pai 2 após o ponto de crossover.
    for order_id in orders_parent2[crossover_point:]:
        if order_id in parent2["orders"]:
            order_data = parent2["orders"][order_id]
            operator = order_data["operator"]
            day = order_data["day"]
            status = order_data["status"]

            # Verifica se o operador é compatível e a ordem não foi atribuída.
            if (order_id not in assigned_orders
                and meets_minimum_skills(operators[operator]["skills"], orders[order_id]["required_skills"])[0]
            ):
                child["orders"][order_id] = {"operator": operator, "day": day, "status": status}
                assigned_orders.add(order_id)

    # Atribui ordens "não atribuídas", aleatoriamente.
    for order_id in orders.keys():
        if order_id not in assigned_orders:
            random_operator = random.choice(list(operators.keys()))
            random_day = random.randint(1, max_days)
            
            # Calcula a quantidade de dias em atraso, se late_order > 0 = atraso.. 
            late_order = random_day - order_data["expected_start_day"]
            new_status = "atrasada" if late_order > 0 else "atendida"

            # Garante que o operador é compatível.
            while not meets_minimum_skills(operators[random_operator]["skills"], orders[order_id]["required_skills"])[0]:
                random_operator = random.choice(list(operators.keys()))

            child["orders"][order_id] = {"day": random_day, "operator": random_operator, "status": new_status}
            assigned_orders.add(order_id)

    # Recalcula o fitness para o novo individuo sendo criado.
    child["fitness"] = calculate_fitness(child, operators, orders, max_days)

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

    # Garantir que o fitness original esteja definido.
    original_fitness = solution["fitness"]
    if original_fitness is None:
        raise ValueError("O fitness original não pode ser None. Verifique a função de cálculo de aptidão.")


    # Aplica mutações em ordens individuais com base na taxa de mutação.
    for order_id, allocation in solution["orders"].items():
        if random.random() < mutation_rate:
            current_day = allocation["day"]
            current_operator = allocation["operator"]
            current_status = allocation["status"]
            expected_start_day = orders[order_id]["expected_start_day"]

            # Seleciona um novo operador e um novo dia aleatoriamente.
            new_day = random.randint(1, max_days)
            new_operator = random.choice(list(operators.keys()))

            # Verifica se o novo operador atende às habilidades necessárias para a ordem.
            if meets_minimum_skills(operators[new_operator]["skills"], orders[order_id]["required_skills"])[0]:
                # Atualiza temporariamente a alocação para o novo operador e dia.
                mutated["orders"][order_id] = {"day": new_day, "operator": new_operator, "status": None}

                # Atualiza o status da ordem.
                mutated["orders"][order_id]["status"] = "atendida" if new_day <= expected_start_day else "atrasada"
                
                # Calcula a aptidão antes e depois da mutação.
                new_fitness = calculate_fitness(mutated, operators, orders, max_days)

                # Garantir que `new_fitness` seja válido.
                if new_fitness is None:
                    raise ValueError("O cálculo de aptidão retornou None. Verifique a função de cálculo de aptidão.")

                # Se a mutação não melhorar a aptidão, desfaz a alteração.
                if new_fitness < original_fitness:
                    mutated["orders"][order_id] = {
                        "day": current_day, 
                        "operator": current_operator, 
                        "status": current_status
                        }
                else:
                    # Atualiza o fitness da solução mutada.
                    mutated["fitness"] = new_fitness    
                    
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

# Função para executar o algoritmo genético no proprio arquivo
def run_genetic_algorithm(operators, orders, population_size=50, generations=100, 
                          mutation_rate=0.4, elitism_size=5, reinitalize_interval=10, max_days=5):
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
    operators, orders = create_initial_data(operators, orders, max_days)
    
    # Gera populaçao inicial com base nos operadores e ordens iniciais.
    population = [create_initial_solution(operators, orders, max_days) 
                  for _ in range(population_size)]

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
                            calculate_fitness(individual, operators, orders, max_days))

        # Exibição da aptidão da melhor solução da geração.
        best_fitness = calculate_fitness(population[0], operators, orders)
        best_schedule = population[0]
        best_fitness_values.append(best_fitness)
        best_schedules.append(best_schedule)
        
        # Geração da nova população.
        new_population = [population[0]]    # Preserva o melhor indivíduo (elitismo)
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:elitism_size], k=2)
            child = crossover(parent1, parent2, operators, orders, max_days)
            child = mutate(child, operators, orders, mutation_rate, max_days)
            new_population.append(child)

        # Reinicialização da população a cada 'reinitalize_interval' gerações.
        # Esta função aumenta a variabilidade na população, trocando a metade da populaçao com menor fit.
        if generation % reinitalize_interval == 0:
            num_to_reinitialize = population_size // 2
            new_population[-num_to_reinitialize:] = [
                create_initial_solution(operators, orders, max_days) 
                for _ in range(num_to_reinitialize)]

        population = new_population

    # Após as gerações, mostra a melhor solução.
    best_solution = max(best_schedules, key=lambda solution: 
                            calculate_fitness(solution, operators, orders))
    
    print(f"\nBest solution fitness: {calculate_fitness(best_solution, operators, orders):.2f}")

    # Conversão dos dados da melhor solução encontrada em Dataframe.
    final_df, unassigned_orders = solution_to_dataframe(best_solution, operators, orders)
    imprimir_resultados_alocacao(final_df, unassigned_orders, orders, "Genetic Algorithm")
    
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
                           params["_MUTATION_RATE"], params["_ELITISM_SIZE"], params["_REINITIALIZE_INTERVAL"], params["_DAYS"])
    
    # Salva os resultados em arquivo.
    salvar_arquivos(best_solution_df)