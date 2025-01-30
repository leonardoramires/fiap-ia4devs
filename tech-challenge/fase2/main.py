# Imports das funções dos algoritmos
import functions.common_functions as cf
import functions.greedy_algorithm as ga
import functions.linear_programming_algorithm as lp
import functions.human_allocation as ha

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

algorithms = {
    "genetic_algorithm",
    "greedy_algorithm",
    "human_allocation",
    "linear_programming_algorithm",
}

def run_greedy_algorithm(operators, orders):
    print("="*35 + " Greedy Algorithm " + "="*35)
    solution = ga.greedy_allocation(operators, orders)
    greedy_fitness = cf.calculate_fitness(solution, operators, orders, params["_DAYS"])
    solution_df, unassigned_orders = cf.solution_to_dataframe(solution, operators, orders)
    print("Fitness (Greedy Algorithm):", greedy_fitness)
    cf.imprimir_resultados_alocacao(solution_df, unassigned_orders, orders, "greedy_algorithm")
    cf.salvar_arquivos(solution_df, 'greedy_algorithm')

def run_linear_algorithm(operators, orders):
    print("="*30 + " Linear Programming Algorithm " + "="*29)
    solution = lp.linear_programming_allocation(operators, orders)
    linear_fitness = cf.calculate_fitness(solution, operators, orders, params["_DAYS"])
    solution_df, unassigned_orders = cf.solution_to_dataframe(solution, operators, orders)
    print("Fitness (Linear Programming):", linear_fitness)
    cf.imprimir_resultados_alocacao(solution_df, unassigned_orders, orders, "linear_programming")
    cf.salvar_arquivos(solution_df, 'greedy_algorithm')

def run_human_allocation(operators, orders):
    print("="*35 + " Human Allocation " + "="*35)
    solution = ha.human_allocation_execution(operators, orders)
    human_allocation_fitness = cf.calculate_fitness(solution, operators, orders, params["_DAYS"])
    solution_df, unassigned_orders = cf.solution_to_dataframe(solution, operators, orders)
    print("Fitness (Alocação Humana):", human_allocation_fitness)
    cf.imprimir_resultados_alocacao(solution_df, unassigned_orders, orders, "human_allocation")
    cf.salvar_arquivos(solution_df, 'human_allocation')

def run_algorithm_comparison(operators, orders):
    if "greedy_algorithm" in algorithms_to_perform:
        run_greedy_algorithm(operators, orders)
    
    if "linear_programming_algorithm" in algorithms_to_perform:
        run_linear_algorithm(operators, orders)

    if "human_allocation" in algorithms_to_perform:
        run_human_allocation(operators, orders)

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
    operators, orders = cf.create_initial_data(params["_N_OPERATORS"], params["_N_ORDERS"], params["_DAYS"])

    # Executa os algoritmos de comparação
    run_algorithm_comparison(operators, orders)    

    if "genetic_algorithm" not in algorithms_to_perform:
        exit()

    selected_algorithm = "genetic_algorithm"
    
    # Gera populaçao inicial com base nos operadores e ordens iniciais.
    population = [algorithms[selected_algorithm].create_initial_solution(operators, orders, params["_DAYS"]) 
                  for _ in range(params["_POPULATION_SIZE"])]

    # =========== LOOP DO PYGAME ===========
    pygame.init()

    # Inicia o contador de geraçoes em 1.
    generation_counter = itertools.count(start=1) 

    # Salva os melhores fitness e geraçoes para plottar.
    best_fitness_values = []
    best_schedules = []

    # Contador para imprimir FPS a cada 20 quadros
    fps_counter = 0
    fps_print_interval = 10
        
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
                    running = False  # Sai do jogo quando a tecla 'q' é apertada.

        if not pause:
            # Atualiza a geração.
            generation = next(generation_counter)

            # Limpa a tela.
            screen.fill(cor_fundo)
            
            # population = sorted(population, key=calculate_fitness).
            population = sorted(population, reverse=True, key=lambda individual: 
                                algorithms[selected_algorithm].calculate_fitness(individual, operators, orders, params["_DAYS"]))
            
            # Exibição da aptidão da melhor solução da geração.
            best_fitness = population[0]["fitness"]
            best_schedule = population[0] 
            best_fitness_values.append(best_fitness)
            best_schedules.append(best_schedule)
            
            # Geração da nova população.
            new_population = [population[0]]    # Preserva o melhor indivíduo (elitismo)
            while len(new_population) < params["_POPULATION_SIZE"]:
                parent1, parent2 = random.choices(population[:params["_ELITISM_SIZE"]], k=2)
                child = algorithms[selected_algorithm].crossover(parent1, parent2, operators, orders, params["_DAYS"])
                child = algorithms[selected_algorithm].mutate(child, operators, orders, params["_MUTATION_RATE"], params["_DAYS"])
                new_population.append(child)

            # Reinicialização da população a cada 'reinitalize_interval' gerações.
            # Esta função aumenta a variabilidade na população, trocando a metade da populaçao com menor fit.
            new_population = sorted(new_population, reverse=True, key=lambda individual: 
                                individual["fitness"])
            if generation % params["_REINITIALIZE_INTERVAL"] == 0:
                num_to_reinitialize = params["_POPULATION_SIZE"] // 2
                new_population[-num_to_reinitialize:] = [
                    algorithms[selected_algorithm].create_initial_solution(operators, orders, params["_DAYS"]) 
                    for _ in range(num_to_reinitialize)]
                
                # Recalcula o fitness da nova populaçao
                for individual in new_population[-num_to_reinitialize:]:
                    individual["fitness"] = algorithms[selected_algorithm].calculate_fitness(individual, operators, orders, params["_DAYS"])

            population = new_population

            # Encontrando a melhor solução com base no fitness
            best_solution = max(best_schedules, key=lambda individual: individual["fitness"])
            
            # Desenha as informações na tela.
            pgf.draw_plot(screen, list(range(len(best_fitness_values))), best_fitness_values, window_size)
            pgf.draw_squares(screen, best_solution, orders, params["_N_ORDERS"], window_size)  
            pgf.draw_text(screen, f"Best Fitness: {best_fitness:.2f}", 450, window_size[1] - 20, font_size=15, font="Courier New")
            
            # Atualiza a tela.
            pygame.display.flip()
            # Controla o FPS do jogo
            clock.tick(FPS) 
            
            # TODO IF todas as ordens forem alocadas ou BEST FITNESS
            # fazer tambem pelo numero de geraçoes em que nao teve melhora
            if (generation > params["_GENERATIONS"] ):
                pause = True
                print('Otimização do melhor indivíduo encontrada!!!')

                # Conversão dos dados de operadores e ordens em Dataframe.
                operators_df, orders_df = algorithms[selected_algorithm].op_orders_to_dataframe(operators, orders)

                # Conversão dos dados da melhor solução encontrada em Dataframe.
                best_solution_df, unassigned_orders = algorithms[selected_algorithm].solution_to_dataframe(best_solution, operators, orders)

                # Imprime relatorio
                cf.imprimir_resultados_alocacao(best_solution_df, unassigned_orders, orders, selected_algorithm)

                # Exibe os resultados.
                print("Dados dos operadores: \n", operators_df)
                print("Dados das ordens: \n", orders_df)
                print(f"\nSolução final (shape = {best_solution_df.shape}):\n", 
                      best_solution_df.sort_values(["id_operador", "id_ordem", "dia"]))
            
                if unassigned_orders:
                    print("\nOrdens não alocadas:\n", orders_df.loc[orders_df["order_id"].isin(unassigned_orders)])

                # Salva os resultados em arquivo.
                cf.salvar_arquivos(best_solution_df)
              
        if pause:
            pgf.draw_text(screen, "PAUSADO", screen.get_width() // 2, screen.get_height() // 2, font_size=30, font='Courier New')

        
    pygame.quit()