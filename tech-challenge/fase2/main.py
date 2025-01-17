# Imports das funções dos algoritmos
from functions import algorithms
from functions import common_functions as cf
from functions import greedy_algorithm as ga
from functions import linear_programming_algorithm as lp
from functions import human_allocation as ha

# Imports para o funcionamento do PyGame
import pygame
from pygame.locals import *
from functions import pygame_functions as pgf
import itertools

# Imports gerais
import random
import argparse

# TODO Colocar no streamlit, executar e print o DF (pandas) no final.
# colocar disponivel para que uma pessoa possa colocar um arquivo de texto e que ela consiga colocar as orders e operadores pra rodar.
# Tentar colocar no pygame uma "agenda" aparecendo as OS's alocadas para cada operador.

# =========== INICIALIZADOR DE JANELA ===========
# Cria a janela do Pygame
window_size = (1000, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Loop de Gerações")
clock = pygame.time.Clock()

# =========== VARs GLOBAIS ===========
FPS = 10    # Velocidade de atualizaçao dos frames do PyGame
cor_fundo = [204, 204, 204]

params = {
    "_N_ORDERS" : 100,
    "_N_OPERATORS" : 10,
    "_POPULATION_SIZE" : 50,
    "_GENERATIONS" : 50,
    "_MUTATION_RATE" : 0.3,
    "_ELITISM_SIZE" : 5,
    "_REINITIALIZE_INTERVAL" : 10,
    "_DAYS": 5,  
}

def run_greedy_algorithm(_N_ORDERS, _N_OPERATORS):
    print("="*35 + " Greedy Algorithm " + "="*35)
    operators, orders = cf.create_sample_data(_N_ORDERS, _N_OPERATORS)
    solution = ga.greedy_allocation(operators, orders)
    greedy_fitness = cf.calculate_fitness(solution, operators, orders)
    solution_df, unassigned_orders = cf.solution_to_dataframe(solution, operators, orders)
    print("Fitness (Greedy Algorithm):", greedy_fitness)
    if len(unassigned_orders) > 0:
        orders_df = cf.orders_to_dataframe(orders)
        print(f"\n As ordens abaixo não puderam ser alocadas ({len(unassigned_orders)}): ")
        print(orders_df.loc[orders_df["order_id"].isin(unassigned_orders)])
    solution_df.to_csv("result_greedy_algorithm.csv", index=False)
    orders_df.to_csv("unassigned_orders_greedy_algorithm.csv", index=False)
    print("\n")

def run_linear_algorithm(_N_ORDERS, _N_OPERATORS):
    print("="*30 + " Linear Programming Algorithm " + "="*29)
    operators, orders = cf.create_sample_data(_N_ORDERS, _N_OPERATORS)
    solution = lp.linear_programming_allocation(operators, orders)
    linear_fitness = cf.calculate_fitness(solution, operators, orders)
    solution_df, unassigned_orders = cf.solution_to_dataframe(solution, operators, orders)
    print("Fitness (Linear Programming):", linear_fitness)
    if len(unassigned_orders) > 0:
        orders_df = cf.orders_to_dataframe(orders)
        print(f"\n As ordens abaixo não puderam ser alocadas ({len(unassigned_orders)}): ")
        print(orders_df.loc[orders_df["order_id"].isin(unassigned_orders)])
    solution_df.to_csv("result_linear_programming.csv", index=False)
    orders_df.to_csv("unassigned_orders_linear_programming.csv", index=False)
    print("\n")

def run_human_allocation(_N_ORDERS, _N_OPERATORS):
    print("="*35 + " Human Allocation " + "="*35)
    operators, orders = cf.create_sample_data(_N_ORDERS, _N_OPERATORS)
    solution = ha.human_allocation(operators, orders)
    linear_fitness = cf.calculate_fitness(solution, operators, orders)
    solution_df, unassigned_orders = cf.solution_to_dataframe(solution, operators, orders)
    print("Fitness (Alocação Humana):", linear_fitness)
    if len(unassigned_orders) > 0:
        orders_df = cf.orders_to_dataframe(orders)
        print(f"\n As ordens abaixo não puderam ser alocadas ({len(unassigned_orders)}): ")
        print(orders_df.loc[orders_df["order_id"].isin(unassigned_orders)])
    solution_df.to_csv("result_human_allocation.csv", index=False)
    orders_df.to_csv("unassigned_orders_humman_allocation.csv", index=False)
    print("\n")

def run_comparison_algorithms():
    if "greedy_algorithm" in algorithms_to_perform:
        run_greedy_algorithm(params["_N_ORDERS"], params["_N_OPERATORS"])
    
    if "linear_programming_algorithm" in algorithms_to_perform:
        run_linear_algorithm(params["_N_ORDERS"], params["_N_OPERATORS"])

    if "human_allocation" in algorithms_to_perform:
        run_human_allocation(params["_N_ORDERS"], params["_N_OPERATORS"])

if __name__ == '__main__':
    """
        Seleçao de algoritmo a ser utilizado: 
        Args:   "genetic_algorithm"
                "linear_programming_algorithm"
                "greedy_algorithm"
                "human_allocation"
    """
    # parser para escolha do algoritmo
    algorithm_keys = list(algorithms.keys())
    parser = argparse.ArgumentParser(description="Escolha o algoritmo de alocação a ser utilizado.")
    parser.add_argument('--algorithm', choices=algorithm_keys, help="Algoritmo de alocação a ser utilizado: 'genetic_algorithm', 'greedy_algorithm', 'linear_programming_algorithm' ou 'human_allocation'")
    args = parser.parse_args()

    # Escolha do algoritmo
    algorithms_to_perform = algorithm_keys if args.algorithm is None else [args.algorithm]

    # Inicializa operadores e ordens iniciais.
    operators, orders = cf.create_sample_data(params["_N_ORDERS"], params["_N_OPERATORS"])

    # Executa os algoritmos de comparação
    run_comparison_algorithms()    

    if "genetic_algorithm" not in algorithms_to_perform:
        exit()

    selected_algorithm = "genetic_algorithm"

    # Gera populaçao inicial
    population = [algorithms[selected_algorithm].create_initial_solution(operators, orders) for _ in range(params["_POPULATION_SIZE"])]


    # =========== LOOP DO PYGAME ===========
    pygame.init()

    # Inicia o contador de geraçoes em 1
    generation_counter = itertools.count(start=1) 

    # Salva os melhores fitness e geraçoes para plottar
    best_fitness_values = []
    best_schedules = []
        

    # Main game loop
    running = True
    pause = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                elif event.key == pygame.K_q:
                    running = False  # Sai do jogo quando a tecla 'q' é apertada

        if not pause:
            # Atualiza a geração
            i = next(generation_counter)

            # Limpa a tela
            screen.fill(cor_fundo)
            
            # population = sorted(population, key=calculate_fitness)
            population = sorted(population, reverse=True, key=lambda individual: algorithms[selected_algorithm].calculate_fitness(individual, operators, orders ))

            # Exibição da aptidão da melhor solução da geração
            best_fitness = algorithms[selected_algorithm].calculate_fitness(population[0], operators, orders)
            best_schedule = population[0]
            best_fitness_values.append(best_fitness)
            best_schedules.append(best_schedule)
            
            # Geração da nova população
            new_population = [population[0]]
            while len(new_population) < params["_POPULATION_SIZE"]:
                parent1, parent2 = random.choices(population[:params["_ELITISM_SIZE"]], k=2)
                child = algorithms[selected_algorithm].crossover(parent1, parent2, operators=operators, orders=orders)
                child = algorithms[selected_algorithm].mutate(child, operators, orders, mutation_rate=params["_MUTATION_RATE"])
                new_population.append(child)

            # Reinicialização da população a cada 'reinitalize_interval' gerações
            if i % params["_REINITIALIZE_INTERVAL"] == 0:
                # print(f"\n ------ Reinitializing population at generation {generation} ------")
                num_to_reinitialize = params["_POPULATION_SIZE"] // 2
                new_population[-num_to_reinitialize:] = [algorithms[selected_algorithm].create_initial_solution(operators, orders) for _ in range(num_to_reinitialize)]

            population = new_population

            # Após as gerações, mostra a melhor solução
            best_solution = max(best_schedules, key=lambda sol: algorithms[selected_algorithm].calculate_fitness(sol, operators, orders))
            
            # Atualiza o status das ordens com base na melhor solução
            orders_status = algorithms[selected_algorithm].update_order_status(best_solution, orders)

            # Métodos de desenho
            pgf.draw_plot(screen, list(range(len(best_fitness_values))), best_fitness_values, window_size=window_size)

            pgf.draw_squares(screen, best_solution, operators, orders_status, n_orders=params["_N_ORDERS"], window_size=window_size)
            
            # print(f"\nBest solution fitness: {algorithms[selected_algorithm].calculate_fitness(best_solution, operators, orders):.2f}")
            pgf.draw_text(screen, f"Best Fitness: {best_fitness:.2f}", 450, window_size[1] - 20, font_size=15, font="Courier New")
            # Atualiza a tela
            pygame.display.flip()
            clock.tick(FPS)
            
            # TODO IF todas as ordens forem alocadas ou BEST FITNESS
            # fazer tambem pelo numero de geraçoes em que nao teve melhora
            if (i > params["_GENERATIONS"] ):
                pause = not pause
                print('Otimização do melhor indivíduo encontrada!!!')
                # Conversão dos dados de operadores e ordens em pandas dataframe
                operators_df, orders_df = algorithms[selected_algorithm].sample_to_dataframe(operators, orders_status)

                # Execução do algoritmo com a geração de um dataset com a alocação das ordens aos operadores
                final_df, unassigned_orders = algorithms[selected_algorithm].solution_to_dataframe(best_solution, operators, orders_status)

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
                
                final_df.to_csv("./resultado.csv", index=False)
                final_df.to_excel("./resultado.xlsx", index=False)
                
        if pause:
            pgf.draw_text(screen, "PAUSADO", screen.get_width() // 2, screen.get_height() // 2, font_size=30, font='Courier New')


    pygame.quit()