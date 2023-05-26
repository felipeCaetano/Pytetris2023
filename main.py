import random

import pygame

from colors import (BLACK, WHITE, VERMELHO, AZUL, VERDE, YELLOW, CIANO, ROXO,
                    LARANJA)
from configs import (
    SCR_WIDTH, SCR_HEIGHT, LEN_BLOCK, BOARD_WIDTH,
    BOARD_HEIGHT, INIT_POS, FPS, WIDTH_TAB
)
from pecas import PIECES

cores_blocos = [VERMELHO, AZUL, VERDE, YELLOW, CIANO, ROXO, LARANJA]


class Tetris:
    def __init__(self):
        self.counter = 0
        pygame.init()
        self.pos_y = None
        self.pos_x = None
        self.color_piece = None
        self.cur_piece = None
        self.game_over = False
        self.menu_atv = True
        self.speed = 1
        self.option = 0
        self.score = 0
        self.high_score = 0
        self.options = ["Iniciar Jogo", "Configurações", "Créditos", "Sair"]
        self.timer = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
        self.area = pygame.Surface.subsurface(
            self.screen, [0, 0, WIDTH_TAB, SCR_HEIGHT - 2 * LEN_BLOCK])
        self.board = [[BLACK] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.new_block()
        pygame.display.set_caption("PyTetris")

    def new_block(self):
        self.cur_piece = self.create_piece()
        self.color_piece = random.choice(cores_blocos)
        self.pos_x = INIT_POS
        self.pos_y = 0

    @staticmethod
    def create_piece():
        return random.choice(PIECES)

    def in_bounds(self, pos_x, pos_y, piece):
        board = self.board
        for i, line in enumerate(piece):
            y = pos_y + i
            if y >= BOARD_HEIGHT:
                return False
            for j, block in enumerate(line):
                x = pos_x + j
                if not (0 <= x < BOARD_WIDTH):
                    return False
                if block == 1 and board[y][x] != BLACK:
                    return False
        return True

    def update_board(self, pos_x, pos_y):
        for i, line in enumerate(self.cur_piece):
            for j, block in enumerate(line):
                if block == 1 and pos_y + i >= 0:
                    self.board[pos_y + i][pos_x + j] = self.color_piece

    def rotate_piece(self):
        new_piece = list(zip(*reversed(self.cur_piece)))
        if not self.in_bounds(self.pos_x, self.pos_y, new_piece):
            return self.cur_piece
        return new_piece

    def remove_lines(self):
        lines_removed = []
        for index, line in enumerate(self.board):
            if all(clock_color != BLACK for clock_color in line):
                lines_removed.append(index)
        for line in lines_removed:
            self.score += len(self.board[line])
            del self.board[line]
            self.board.insert(0, [BLACK] * BOARD_WIDTH)

    def draw_blocks(self):
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                cor = self.board[i][j]
                self.draw_block(j * LEN_BLOCK, i * LEN_BLOCK, cor)

    def draw_block(self, posx, posy, cor):
        # self.draw_grid(posx, posy)
        pygame.draw.rect(
            self.area, cor, (posx, posy, LEN_BLOCK, LEN_BLOCK))

    def draw_grid(self):
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                pygame.draw.rect(
                    self.area,
                    WHITE,
                    (j * LEN_BLOCK, i * LEN_BLOCK, LEN_BLOCK, LEN_BLOCK), 1
                )

    def draw_menu(self):
        for i, op in enumerate(self.options):
            if i == self.option:
                cor = YELLOW
            else:
                cor = WHITE
            text = pygame.font.Font(None, 36).render(op, True, cor)
            pos_x = (SCR_WIDTH - text.get_width()) // 2
            pos_y = (SCR_HEIGHT // 2) + i * 50
            self.screen.blit(text, (pos_x, pos_y))

    def draw_screen(self):
        self.draw_blocks()
        # self.draw_grid()
        for i, line in enumerate(self.cur_piece):
            for j, block in enumerate(line):
                if block == 1:
                    pygame.draw.rect(
                        self.area,
                        self.color_piece,
                        (
                            (self.pos_x + j) * LEN_BLOCK,
                            (self.pos_y + i) * LEN_BLOCK,
                            LEN_BLOCK,
                            LEN_BLOCK),
                    )

    def clear_scr(self):
        self.screen.fill(BLACK)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if self.menu_atv:
                    if event.key == pygame.K_UP:
                        self.option = (self.option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.option = (self.option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.option] == "Iniciar Jogo":
                            self.menu_atv = False
                        elif self.options[self.option] == "Sair":
                            self.game_over = True
                else:
                    if event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_SPACE:
                        self.cur_piece = self.rotate_piece()

    def move_down(self):
        if self.in_bounds(self.pos_x, self.pos_y + 1, self.cur_piece):
            self.pos_y += 1

    def move_right(self):
        if self.pos_x < BOARD_WIDTH - len(self.cur_piece[0]) \
                and self.in_bounds(self.pos_x + 1, self.pos_y, self.cur_piece):
            self.pos_x += 1

    def move_left(self):
        if self.pos_x > 0 and self.in_bounds(
                self.pos_x - 1, self.pos_y, self.cur_piece):
            self.pos_x -= 1

    def atualizar(self):
        if pygame.time.get_ticks() - self.timer > 500 // self.speed:
            if self.in_bounds(self.pos_x, self.pos_y + 1, self.cur_piece):
                self.pos_y += 1
            else:
                self.update_board(self.pos_x, self.pos_y)
                self.new_block()
                if not self.in_bounds(self.pos_x, self.pos_y, self.cur_piece):
                    self.game_over = True
            self.timer = pygame.time.get_ticks()

    def run(self):
        while not self.game_over:
            self.clear_scr()
            self.event_handler()
            if self.menu_atv:
                self.draw_menu()
            else:
                self.atualizar()
                self.draw_screen()
                self.draw_grid()
                self.remove_lines()
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()


Tetris().run()
