#Imports para o funcionamento do PyGame
import pygame
import pylab
import matplotlib.backends.backend_agg as agg
import math

# Função para desenhar o plot do matplotlib na tela.
def draw_plot(screen, x, y, x_label = 'Generation', y_label = 'Fitness', window_size=(1000, 600)):
    """
    Desenha um gráfico em um buffer e exibe na tela do Pygame.

    Args:
        screen: A superfície do Pygame onde o gráfico será desenhado.
        x: Lista de valores para o eixo x.
        y: Lista de valores para o eixo y.
        x_label: Rótulo do eixo x.
        y_label: Rótulo do eixo y.
        window_size: Tamanho da janela (largura, altura)
    """
    # Cria a figura com tamanho e resolução especificados.
    fig = pylab.figure(figsize=[4, 4], # Inches
                       dpi=100,        # 100 dots por inch, resultado do buffer = 400x400 pixels
                       )
    ax = fig.gca()
    ax.plot(x, y)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Renderiza a figura no buffer.
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    # Converte o buffer em uma superfície do Pygame.
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")

    # Calcula o deslocamento para centralizar o gráfico na metade esquerda da tela.
    x_offset = 50  # Fica na metade esquerda da tela.
    y_offset = (window_size[1] - size[1]) // 2  # Centraliza verticalmente.

    screen.blit(surf, (x_offset,y_offset))

    # Fecha a figura para liberar memória
    pylab.close(fig)
    
    
# Função para desenhar os quadrados com base no status das ordens
def draw_squares(screen, population, orders, n_orders, window_size=(1000, 600)):
    """
    Desenha uma matriz de quadrados na tela, representando o status das ordens.

    Args:
        screen: A superfície do Pygame onde os quadrados serão desenhados.
        population: A solução atual (alocação de ordens por operadores e dias).
        operators: Operadores disponíveis.
        orders: Ordens disponíveis.
        n_orders: Número total de ordens.
        window_size: Tamanho da janela (largura, altura)
    """
    
    # Define o tamanho de cada quadrado e a distância entre os quadrados.
    square_size = 40
    distance_between_squares = 5

    # Ajusta o tamanho da fonte para caber no quadrado
    font_size = square_size // 2  # Tamanho da fonte é metade do tamanho do quadrado
    font = pygame.font.Font(None, font_size)  # Cria a fonte com o tamanho ajustado
    
    # Calcula o tamanho da matriz.
    
    n_columns = math.floor(n_orders ** 0.5)
    n_rows = math.ceil(n_orders / n_columns)
    matrix_width = n_columns * (square_size + distance_between_squares) - distance_between_squares
    matrix_height = n_columns * (square_size + distance_between_squares) - distance_between_squares

    # Calcula os deslocamentos para centralizar a matriz na metade direita da tela.
    x_offset = window_size[0] // 2  # Começa no meio da tela, à direita.
    y_offset = (window_size[1] - matrix_height) // 2  # Centraliza verticalmente.

    # Índice para acessar as ordens.
    order_ids = list(orders.keys())  # Lista de IDs das ordens.
    total_orders = n_orders


    # Criar uma lista de superfícies para os quadrados.
    square_surfaces = []

    # Desenha a matriz de quadrados.
    for row in range(n_rows):
        for col in range(n_columns):
            x = col * (square_size + distance_between_squares) + x_offset
            y = row * (square_size + distance_between_squares) + y_offset
            
            # Calcula o índice da ordem correspondente.
            order_index = row * n_columns + col
            if order_index < total_orders:
                order_id = order_ids[order_index]
                order = population["orders"][order_id]
                
                # Determina o operador.
                operator_id = order["operator"]
                operator = operator_id if operator_id is not None else "N/A"
               
                # Define a cor com base no status da ordem.
                if order["status"] == "atendida":
                    color = (0, 255, 0)  # Verde para atendida.
                elif order["status"] == "atrasada":
                    color = (255, 255, 102)  # Amarelo para atrasada.
                else:
                    color = (255, 51, 0)  # Vermelha para não atendida.
            else:
                # Caso não haja ordem correspondente .
                color = (0, 0, 26)  # Azul Petroleto para erro de referência.

            # Cria a superfície para o quadrado.
            square_surface = pygame.Surface((square_size, square_size))
            square_surface.fill(color) 
            
            # Renderiza o texto do operador.
            operator_text = font.render(str(operator), True, (0, 0, 0))  # Texto em preto.
            
            # Verifica o texto gerado
            text_rect = operator_text.get_rect(center=(square_size // 2, square_size // 2))  # Centraliza o texto
            square_surface.blit(operator_text, text_rect)  

            # Adiciona a superfície à lista.
            square_surfaces.append((square_surface, x, y))

    # Agora desenha todos os quadrados de uma vez.
    for surface, x, y in square_surfaces:
        screen.blit(surface, (x, y))
           
# Função para renderizar texto na tela
def draw_text(screen, text, x_position, y_position, color=(0, 0, 0), font_size=30, font='Arial'):
    # Initialize Pygame font.
    pygame.font.init()
    
    # Set the font and size.
    font = pygame.font.SysFont(font, font_size)
    
    # Render the text
    text_surface = font.render(text, True, color)
    
    # Get the rectangle containing the text surface.
    text_rect = text_surface.get_rect()
    
    # Set the position of the text.
    text_rect.topleft = (x_position, y_position)
    
    # Blit the text onto the screen.
    screen.blit(text_surface, text_rect)