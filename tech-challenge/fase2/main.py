# Imports das funções dos algoritmos
from functions import algorithms

# Imports para o funcionamento do PyGame
import pygame
from pygame.locals import *
from functions import pygame_functions as pgf
import itertools

# Imports gerais
import random


# =========== INICIALIZADOR DE JANELA ===========
# Cria a janela do Pygame
window_size = (800, 400)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Loop de Gerações")
clock = pygame.time.Clock()

# =========== VARs GLOBAIS ===========
FPS = 20    # Velocidade de atualizaçao dos frames do PyGame
cor_fundo = [204, 204, 204]

params = {
    "_N_ORDERS" : 100,
    "_N_OPERATORS" : 15,
    "_POPULATION_SIZE" : 64,
    "_GENERATIONS" : 50,
    "_MUTATION_RATE" : 0.3,
    "_ELITISM_SIZE" : 5,
    "_REINITIALIZE_INTERVAL" : 10,
}

if __name__ == '__main__':
    """
        Seleçao de algoritmo a ser utilizado: 
        Args:   "genetic_algorithm"
                "linear_programming_algorithm"
                "greedy_algorithm"
    """
    # Escolha do algoritmo
    selected_algorithm = "genetic_algorithm"

    if selected_algorithm not in algorithms:
        raise ValueError(f"Algoritmo '{selected_algorithm}' não encontrado!")

    # Inicializa operadores e ordens iniciais.
    operators, orders = algorithms[selected_algorithm].create_sample_data(params["_N_ORDERS"], params["_N_OPERATORS"])
    
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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False  # Sai do jogo quando a tecla 'q' é apertada


        # Atualiza a geração
        i = next(generation_counter)

        # Limpa a tela
        screen.fill(cor_fundo)

        # Cálculo da aptidão de cada solução
        fitness_scores = [algorithms[selected_algorithm].calculate_fitness(solution, operators, orders) for solution in population]
        
        # Ajuste na taxa de mutação conforme o número da geração
        mutation_rate = params["_MUTATION_RATE"] - (i / params["_GENERATIONS"]) * 0.05  # Reduz a taxa de mutação
        if mutation_rate < 0.05:
            mutation_rate = 0.05  # Taxa mínima de mutação


        # Exibição da aptidão da melhor solução da geração
        best_fitness = max(fitness_scores)
        best_schedule = population[fitness_scores.index(best_fitness)]
        best_fitness_values.append(best_fitness)
        best_schedules.append(best_schedule)

        # print(f"\nGeneration {generation + 1}/{generations} - Best Fitness: {best_fitness:.2f} - Mutation Rate: {mutation_rate:.4f}")
        # time.sleep(0.1)  # Delay para animação

        # Seleção dos pais
        parents = []
        for _ in range(params["_POPULATION_SIZE"] // 2):
            tournament = random.sample(list(enumerate(fitness_scores)), 5)
            parent_idx = max(tournament, key=lambda x: x[1])[0]
            parents.append(population[parent_idx])

        # Implementação de elitismo: mantém as melhores 'elitism_size' soluções
        sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
        elite_population = [individual for individual, score in sorted_population[:params["_ELITISM_SIZE"]]]


        # Geração da nova população
        new_population = [population[0]] # Mantem o melhor indivíduo
        while len(new_population) < params["_POPULATION_SIZE"]:
            parent1, parent2 = random.sample(parents, 2)
            child = algorithms[selected_algorithm].crossover(parent1, parent2, operators=operators, orders=orders)
            child = algorithms[selected_algorithm].mutate(child, operators, orders, mutation_rate=params["_MUTATION_RATE"])
            new_population.append(child)
            
        # Reinicialização da população a cada 'reinitalize_interval' gerações
        if i % params["_REINITIALIZE_INTERVAL"] == 0:
            num_to_reinitialize = params["_POPULATION_SIZE"] // 2
            new_population[-num_to_reinitialize:] = [algorithms[selected_algorithm].create_initial_solution(operators, orders) for _ in range(num_to_reinitialize)]

        population = new_population


        # Atualiza o status das ordens para cada solução
        orders = algorithms[selected_algorithm].update_order_status(best_schedule, orders)

        # Desenha os quadrados para a melhor solução
        pgf.draw_squares(screen, best_schedule, operators, orders, 5)  # Exibe os quadrados para a solução atual
        
        # # Conversão dos dados de operadores e ordens em pandas dataframe
        # operators_df, orders_df = F.sample_to_dataframe(operators, orders)

        # # Execução do algoritmo com a geração de um dataset com a alocação das ordens aos operadores
        # final_df, unassigned_orders = F.run_genetic_algorithm(
        #     operators,
        #     orders,
        #     population_size=_POPULATION_SIZE,
        #     generations=_GENERATIONS,
        #     mutation_rate=_MUTATION_RATE,
        #     elitism_size=_ELITISM_SIZE,
        #     reinitalize_interval=_REINITIALIZE_INTERVAL
        #     )

        # # Exibe o DataFrame final
        # print("Dados dos operadores: \n")
        # print(operators_df)

        # print("Dados das ordens: \n")
        # print(orders_df)
        
        # print(f"\n Dados das ordens atribuídas aos operdores (shape = {final_df.shape}\n")
        # print(final_df.sort_values(["id_operador", "id_ordem", "dia"], ascending=[True, True, True]))
        
        # print(unassigned_orders)
        # if len(unassigned_orders) > 0:
        #     print("\n As ordens abaixo não puderam ser alocadas: ")
        #     print(orders_df.loc[orders_df["order_id"].isin(unassigned_orders)])
        
        # final_df.to_csv("resultado.csv", index=False)
        # final_df.to_excel("resultado.xlsx", index=False)

       

        # Desenha na tela    
        pgf.draw_plot(screen, list(range(len(best_fitness_values))), best_fitness_values)
        
        # Exibe informações de texto
        # pgf.draw_text(screen, f"Generation: {i}", 10, 10, font_size=15, font='Courier New')
        # pgf.draw_text(screen, f"Mutation Rate: {mutation_rate:.2f}", 10, 30, font_size=15, font='Courier New')
        pgf.draw_text(screen, f"Best Solution: {best_fitness}", 450, window_size[1]-50, font_size=15, font='Courier New')
        
        # Atualiza a tela
        pygame.display.flip()
        clock.tick(FPS)
        
        # Se encontrar uma % que esteja alocada como melhor solução, para o algoritmo.
        if best_fitness == 2300:
            running = False
            print('Otimização do melhor indivíduo encontrada!!!')

    pygame.quit()