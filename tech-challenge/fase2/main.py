import functions as F
import pandas as pd

if __name__ == '__main__':
    # Parâmetros
    _N_ORDERS = 100
    _N_OPERATORS = 15
    _POPULATION_SIZE=50
    _GENERATIONS = 50
    _MUTATION_RATE = 0.3
    _ELITISM_SIZE = 5
    _REINITIALIZE_INTERVAL = 5

    
    # Criação dos dados de operadores e ordens
    operators, orders = F.create_sample_data(n_orders=_N_ORDERS, n_operators=_N_OPERATORS)
    
    # Conversão dos dados de operadores e ordens em pandas dataframe
    operators_df, orders_df = F.sample_to_dataframe(operators, orders)

    # Execução do algoritmo com a geração de um dataset com a alocação das ordens aos operadores
    final_df, unassigned_orders = F.run_genetic_algorithm(
        operators,
        orders,
        population_size=_POPULATION_SIZE,
        generations=_GENERATIONS,
        mutation_rate=_MUTATION_RATE,
        elitism_size=_ELITISM_SIZE,
        reinitalize_interval=_REINITIALIZE_INTERVAL
        )

    # Exibe o DataFrame final
    print("Dados dos operadores: \n")
    print(operators_df)

    print("Dados das ordens: \n")
    print(orders_df)
    
    print(f"\n Dados das ordens atribuídas aos operdores (shape = {final_df.shape}\n")
    print(final_df.sort_values(["id_operador", "id_ordem", "dia"], ascending=[True, True, True]))
    
    print(unassigned_orders)
    if len(unassigned_orders) > 0:
        print("\n As ordens abaixo não puderam ser alocadas: ")
        print(orders_df.loc[orders_df["order_id"].isin(unassigned_orders)])
    
    final_df.to_csv("resultado.csv", index=False)
        