import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]], # I shape
    [[1, 1, 1], [0, 1, 0]], # T shape
    [[1, 1], [1, 1]], # O shape
    [[1, 1, 0], [0, 1, 1]], # S shape
    [[0, 1, 1], [1, 1, 0]], # Z shape
    [[1, 1, 1], [1, 0, 0]], # L shape
    [[1, 1, 1], [0, 0, 1]]  # J shape
]

# Colors for shapes
SHAPE_COLORS = [CYAN, MAGENTA, YELLOW, GREEN, RED, BLUE, ORANGE]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.score = 0
        self.level = 1
        self.game_over = False
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.piece_pos = [0, 3]

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = SHAPE_COLORS[SHAPES.index(shape)]
        return {'shape': shape, 'color': color}

    def rotate_piece(self):
        shape = self.current_piece['shape']
        rotated_shape = [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]
        if not self.check_collision(rotated_shape, self.piece_pos):
            self.current_piece['shape'] = rotated_shape

    def check_collision(self, shape, pos):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell and (
                    x + pos[1] < 0 or
                    x + pos[1] >= len(self.grid[0]) or
                    y + pos[0] >= len(self.grid) or
                    self.grid[y + pos[0]][x + pos[1]] != BLACK
                ):
                    return True
        return False
