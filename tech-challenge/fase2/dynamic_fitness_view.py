import pygame
import sys

class DynamicFitnessView:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Evolução da Aptidão ao Longo das Gerações')
        self.clock = pygame.time.Clock()
        self.fitness_history = []

    def add_fitness(self, fitness):
        self.fitness_history.append(fitness)
        self.draw_plot()

    def draw_plot(self):
        self.screen.fill((255, 255, 255))
        max_fitness = 0
        min_fitness = 0
        margin = 50  # Margin for the axes
        if len(self.fitness_history) > 1:
            max_fitness = max(self.fitness_history)
            min_fitness = min(self.fitness_history)
            if max_fitness == min_fitness:
                max_fitness += 1  # Avoid division by zero
            for i in range(1, len(self.fitness_history)):
                x1 = margin + (i - 1) * ((self.width - 2 * margin) // (len(self.fitness_history) - 1))
                y1 = self.height - margin - int((self.fitness_history[i - 1] - min_fitness) / (max_fitness - min_fitness) * (self.height - 2 * margin))
                x2 = margin + i * ((self.width - 2 * margin) // (len(self.fitness_history) - 1))
                y2 = self.height - margin - int((self.fitness_history[i] - min_fitness) / (max_fitness - min_fitness) * (self.height - 2 * margin))
                pygame.draw.line(self.screen, (255, 0, 0), (x1, y1), (x2, y2), 2)
        
        # Draw scales
        font = pygame.font.SysFont(None, 24)
        max_fitness_text = font.render(f'Max: {max_fitness}', True, (0, 0, 0))
        min_fitness_text = font.render(f'Min: {min_fitness}', True, (0, 0, 0))
        self.screen.blit(max_fitness_text, (10, 10))
        self.screen.blit(min_fitness_text, (10, self.height - 30))
        
        # Draw X and Y axes
        pygame.draw.line(self.screen, (0, 0, 0), (margin, self.height - margin), (self.width - margin, self.height - margin), 2)  # X axis
        pygame.draw.line(self.screen, (0, 0, 0), (margin, margin), (margin, self.height - margin), 2)  # Y axis

        # Draw labels for X and Y axes
        font = pygame.font.SysFont(None, 24)
        x_label = font.render('Gerações', True, (0, 0, 0))
        y_label = pygame.transform.rotate(font.render('Aptidão', True, (0, 0, 0)), 90)
        self.screen.blit(x_label, (self.width // 2, self.height - 30))
        self.screen.blit(y_label, (10, self.height // 2))
        
        pygame.display.flip()

    def show(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clock.tick(60)
        pygame.quit()
        sys.exit()