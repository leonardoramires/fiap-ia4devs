#Imports para o funcionamento do PyGame
import pygame
import pylab
import matplotlib
import matplotlib.backends.backend_agg as agg
matplotlib.use("Agg")

# =========== FUNÇOES DE DESENHO ===========
def draw_plot(screen, x, y, x_label = 'Generation', y_label = 'Fitness'):
    

    fig = pylab.figure(figsize=[4, 4], # Inches
                       dpi=100,        # 100 dots por inch, resultado do buffer = 400x400 pixels
                       )
    ax = fig.gca()
    # ax.plot(random_integers[:i])
    ax.plot(x, y)


    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0,0))
    
    
# Função para desenhar os quadrados com base no status das ordens
def draw_squares(screen, population, operators, orders, days):
    """
    Desenha uma matriz 8x8 de quadrados na tela.

    Args:
        screen: A superfície do Pygame onde os quadrados serão desenhados.
        solution: A solução atual.
        operators: Operadores disponíveis. 
        orders: Ordens disponíveis. 
        days: Número de dias. 
    """
    # Define o número de linhas e colunas na matriz
    n = 8  # Altere esse valor para ajustar o tamanho da matriz (por exemplo, 5x5)
    
    # Define o tamanho de cada quadrado e a distância entre os quadrados
    square_size = 30
    distance_between_squares = 5
    x_offset = 450
    y_offset = 50

    # Inicializa o índice de iteração
    i = 0

    # Garante que o número total de quadrados seja limitado a 8x8
    total_squares = n * n

    # Desenha a matriz de quadrados
    for day in range(days):
        for operator in operators.keys():
            if i >= total_squares:
                break  # Para o loop se o número total de quadrados for alcançado

            x = i % n * (square_size + distance_between_squares) + x_offset
            y = i // n * (square_size + distance_between_squares) + y_offset

            # Verifica as ordens atribuídas ao operador e dia
            orders_for_day_operator = population[day].get(operator, [])

            if orders_for_day_operator:
                # Verifica o status da ordem e desenha a cor correspondente
                for order_id in orders_for_day_operator:
                    order = orders.get(order_id)
                    if order:
                        if order["status"] == "atendida":
                            color = (0, 255, 0)  # Verde para atendida
                        elif order["status"] == "atrasada":
                            color = (255, 0, 0)  # Vermelho para atrasada
                        else:
                            color = (169, 169, 169)  # Cinza para não atendida
                    else:
                        # Ordem não encontrada
                        color = (255, 255, 0)  # Amarelo para erro de referência
                        print(f"Ordem com ID {order_id} não encontrada no dicionário de ordens.")
                    pygame.draw.rect(screen, color, (x, y, square_size, square_size))
            else:
                # Se não houver ordens para esse operador e dia, desenha um quadrado cinza
                pygame.draw.rect(screen, (169, 169, 169), (x, y, square_size, square_size))

            # Incrementa o índice para avançar na matriz
            i += 1

            # Para o loop interno se o número total de quadrados for alcançado
            if i >= total_squares:
                break
        
    

def draw_text(screen, text, x_position, y_position, color=(255, 255, 255), font_size=30, font='Arial'):
    # Initialize Pygame font
    pygame.font.init()
    
    # Set the font and size
    font = pygame.font.SysFont(font, font_size)
    
    # Render the text
    text_surface = font.render(text, True, color)
    
    # Get the rectangle containing the text surface
    text_rect = text_surface.get_rect()
    
    # Set the position of the text
    text_rect.topleft = (x_position, y_position)
    
    # Blit the text onto the screen
    screen.blit(text_surface, text_rect)