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
        self.font = pygame.font.SysFont('Arial', 24)  # Font for rendering text

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

    def place_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.piece_pos[0]][x + self.piece_pos[1]] = self.current_piece['color']
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.piece_pos = [0, 3]
        if self.check_collision(self.current_piece['shape'], self.piece_pos):
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]
        if lines_to_clear:
            for i in lines_to_clear:
                del self.grid[i]
                self.grid.insert(0, [BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])
            lines_cleared = len(lines_to_clear)
            
            if lines_cleared == 1:
                self.score += 100
            elif lines_cleared == 2:
                self.score += 300
            elif lines_cleared == 3:
                self.score += 500
            elif lines_cleared == 4:
                self.score += 800
            self.level = self.score // 1000 + 1

    def move_piece(self, dx):
        new_pos = [self.piece_pos[0], self.piece_pos[1] + dx]
        if not self.check_collision(self.current_piece['shape'], new_pos):
            self.piece_pos = new_pos

    def drop_piece(self):
        new_pos = [self.piece_pos[0] + 1, self.piece_pos[1]]
        if self.check_collision(self.current_piece['shape'], new_pos):
            self.place_piece()
        else:
            self.piece_pos = new_pos

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                pygame.draw.rect(self.screen, cell, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.current_piece['color'], pygame.Rect((self.piece_pos[1] + x) * BLOCK_SIZE, (self.piece_pos[0] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_piece(self):
        for y, row in enumerate(self.next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece['color'], pygame.Rect((SCREEN_WIDTH // BLOCK_SIZE + 1 + x) * BLOCK_SIZE, (1 + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1)
                    elif event.key == pygame.K_DOWN:
                        self.drop_piece()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()

            self.drop_piece()
            self.draw_grid()
            self.draw_piece()
            self.draw_next_piece()
            self.draw_score()
            pygame.display.flip()
            self.clock.tick(5+ self.level)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
