import functions as F
import greedy_algorithm as Greedy
import linear_programming_algorithm as Linear
import pandas as pd
import argparse

ENABLE_LOGGING = False

def run_linear_algorithm(_N_ORDERS, _N_OPERATORS):
    operators, orders = F.create_sample_data(_N_ORDERS, _N_OPERATORS)
    solution = Linear.linear_programming_allocation(operators, orders)
    linear_fitness = F.calculate_fitness(solution, operators, orders)
    df, unassigned_orders = F.solution_to_dataframe(solution, operators, orders)
    print("Fitness (Algoritmo Linear):", linear_fitness)
    if unassigned_orders:
        print("Ordens não atribuídas:", unassigned_orders)
    df.to_csv("resultado_linear_programming.csv", index=False)


def run_greedy_algorithm(_N_ORDERS, _N_OPERATORS):
    operators, orders = F.create_sample_data(_N_ORDERS, _N_OPERATORS)
    solution = Greedy.greedy_allocation(operators, orders)
    greedy_fitness = F.calculate_fitness(solution, operators, orders)
    df, unassigned_orders = F.solution_to_dataframe(solution, operators, orders)
    print("Fitness (Algoritmo Guloso):", greedy_fitness)
    if unassigned_orders:
        print("Ordens não atribuídas:", unassigned_orders)
    df.to_csv("resultado_greedy_programming.csv", index=False)


def run_genetic_algorithm(_N_ORDERS, _N_OPERATORS):
    _POPULATION_SIZE = 50
    _GENERATIONS = 50
    _MUTATION_RATE = 0.3
    _ELITISM_SIZE = 5
    _REINITIALIZE_INTERVAL = 5

    operators, orders = F.create_sample_data(n_orders=_N_ORDERS, n_operators=_N_OPERATORS)
    operators_df, orders_df = F.sample_to_dataframe(operators, orders)
    final_df, unassigned_orders = F.run_genetic_algorithm(
        operators,
        orders,
        population_size=_POPULATION_SIZE,
        generations=_GENERATIONS,
        mutation_rate=_MUTATION_RATE,
        elitism_size=_ELITISM_SIZE,
        reinitalize_interval=_REINITIALIZE_INTERVAL
    )

    if ENABLE_LOGGING:
        print("Dados dos operadores: \n")
        print(operators_df)
        print("Dados das ordens: \n")
        print(orders_df)
        print(f"\n Dados das ordens atribuídas aos operadores (shape = {final_df.shape}\n")
        print(final_df.sort_values(["id_operador", "id_ordem", "dia"], ascending=[True, True, True]))
        print(unassigned_orders)
    if len(unassigned_orders) > 0:
        print("\n As ordens abaixo não puderam ser alocadas: ")
        print(orders_df.loc[orders_df["order_id"].isin(unassigned_orders)])
    final_df.to_csv("resultado_genetic.csv", index=False)

def main():
    parser = argparse.ArgumentParser(description="Escolha o algoritmo de alocação a ser utilizado.")
    parser.add_argument('--algorithm', choices=['linear', 'greedy', 'genetic'], help="Algoritmo de alocação a ser utilizado: 'linear', 'greedy' ou 'genetic'")
    args = parser.parse_args()

    # Parâmetros
    _N_ORDERS = 100
    _N_OPERATORS = 15

    algorithms = ['linear', 'greedy', 'genetic'] if args.algorithm is None else [args.algorithm]

    for algorithm in algorithms:
        if algorithm == 'linear':
            run_linear_algorithm(_N_ORDERS, _N_OPERATORS)
        elif algorithm == 'greedy':
            run_greedy_algorithm(_N_ORDERS, _N_OPERATORS)
        elif algorithm == 'genetic':
            run_genetic_algorithm(_N_ORDERS, _N_OPERATORS)

if __name__ == "__main__":
    main()
