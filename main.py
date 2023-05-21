import random

import pygame

from colors import (PRETO, BRANCO, VERMELHO, AZUL, VERDE, AMARELO, CIANO, ROXO,
                    LARANJA)
from configs import (
    LARG_TELA, ALTURA_TELA, TAM_BLOCO, LARG_TABULEIRO,
    ALTURA_TABULEIRO, POSICAO_INI, FPS, LARG_TAB
)
from pecas import PECAS

cores_blocos = [VERMELHO, AZUL, VERDE, AMARELO, CIANO, ROXO, LARANJA]


class Tetris:
    def __init__(self):
        self.counter = 0
        pygame.init()
        self.posicao_y = None
        self.posicao_x = None
        self.cor_da_peca = None
        self.peca_atual = None
        self.game_over = False
        self.menu_ativo = True
        self.velocidade = 1
        self.opcao = 0
        self.score = 0
        self.high_score = 0
        self.opcoes = ["Iniciar Jogo", "Configurações", "Créditos", "Sair"]
        self.temporizador = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.tela = pygame.display.set_mode((LARG_TELA, ALTURA_TELA))
        self.area_jogo = pygame.Surface.subsurface(
            self.tela, [0, 0, LARG_TAB, ALTURA_TELA - 2 * TAM_BLOCO])
        self.tabuleiro = [[PRETO] * LARG_TABULEIRO for _ in range(ALTURA_TABULEIRO)]
        self.novo_bloco()
        pygame.display.set_caption("PyTetris")

    def novo_bloco(self):
        self.peca_atual = self.criar_peca()
        self.cor_da_peca = random.choice(cores_blocos)
        self.posicao_x = POSICAO_INI
        self.posicao_y = 0

    @staticmethod
    def criar_peca():
        return random.choice(PECAS)

    def esta_dentro(self, pos_x, pos_y, peca):
        tabuleiro = self.tabuleiro
        for i, linha in enumerate(peca):
            y = pos_y + i
            if y >= ALTURA_TABULEIRO:
                return False
            for j, bloco in enumerate(linha):
                x = pos_x + j
                if not (0 <= x < LARG_TABULEIRO):
                    return False
                if bloco == 1 and tabuleiro[y][x] != PRETO:
                    return False
        return True

    def atualizar_matriz(self, pos_x, pos_y):
        for i, linha in enumerate(self.peca_atual):
            for j, bloco in enumerate(linha):
                if bloco == 1 and pos_y + i >= 0:
                    self.tabuleiro[pos_y + i][pos_x + j] = self.cor_da_peca

    def rotacionar_peca(self):
        nova_peca = list(zip(*reversed(self.peca_atual)))
        if not self.esta_dentro(self.posicao_x, self.posicao_y, nova_peca):
            return self.peca_atual
        return nova_peca

    def remover_linhas(self):
        linhas_removidas = []
        for index, linha in enumerate(self.tabuleiro):
            if all(cor_bloco != PRETO for cor_bloco in linha):
                linhas_removidas.append(index)
        for linha in linhas_removidas:
            del self.tabuleiro[linha]
            self.score += len(self.tabuleiro[linha])
            self.tabuleiro.insert(0, [PRETO] * LARG_TABULEIRO)

    def desenhar_blocos(self):
        for i in range(ALTURA_TABULEIRO):
            for j in range(LARG_TABULEIRO):
                cor = self.tabuleiro[i][j]
                self.desenhar_bloco(j * TAM_BLOCO, i * TAM_BLOCO, cor)

    def desenhar_bloco(self, posx, posy, cor):
        # self.draw_grid(posx, posy)
        pygame.draw.rect(
            self.area_jogo, cor, (posx, posy, TAM_BLOCO, TAM_BLOCO))

    def draw_grid(self):
        for i in range(ALTURA_TABULEIRO):
            for j in range(LARG_TABULEIRO):
                pygame.draw.rect(
                    self.area_jogo, BRANCO,
                    (j*TAM_BLOCO, i*TAM_BLOCO, TAM_BLOCO, TAM_BLOCO), 1)

    def desenhar_menu(self):
        for i, opcao in enumerate(self.opcoes):
            if i == self.opcao:
                cor = AMARELO
            else:
                cor = BRANCO
            texto = pygame.font.Font(None, 36).render(opcao, True, cor)
            pos_x = (LARG_TELA - texto.get_width()) // 2
            pos_y = (ALTURA_TELA // 2) + i * 50
            self.tela.blit(texto, (pos_x, pos_y))

    def desenhar_tela(self):
        self.desenhar_blocos()
        # self.draw_grid()
        for i, linha in enumerate(self.peca_atual):
            for j, bloco in enumerate(linha):
                if bloco == 1:
                    pygame.draw.rect(
                        self.area_jogo,
                        self.cor_da_peca,
                        (
                            (self.posicao_x + j) * TAM_BLOCO,
                            (self.posicao_y + i) * TAM_BLOCO,
                            TAM_BLOCO,
                            TAM_BLOCO,
                        ),
                    )

    def limpar_tela(self):
        self.tela.fill(PRETO)

    def tratar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if self.menu_ativo:
                    if event.key == pygame.K_UP:
                        self.opcao = (self.opcao - 1) % len(self.opcoes)
                    elif event.key == pygame.K_DOWN:
                        self.opcao = (self.opcao + 1) % len(self.opcoes)
                    elif event.key == pygame.K_RETURN:
                        if self.opcoes[self.opcao] == "Iniciar Jogo":
                            self.menu_ativo = False
                        elif self.opcoes[self.opcao] == "Sair":
                            self.game_over = True
                else:
                    if event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_SPACE:
                        self.peca_atual = self.rotacionar_peca()

    def move_down(self):
        if self.esta_dentro(self.posicao_x, self.posicao_y + 1,
                            self.peca_atual):
            self.posicao_y += 1

    def move_right(self):
        if self.posicao_x < LARG_TABULEIRO - len(self.peca_atual[0]) \
                and self.esta_dentro(self.posicao_x + 1, self.posicao_y,
                                     self.peca_atual):
            self.posicao_x += 1

    def move_left(self):
        if self.posicao_x > 0 and self.esta_dentro(self.posicao_x - 1,
                                                   self.posicao_y,
                                                   self.peca_atual):
            self.posicao_x -= 1

    def atualizar(self):
        if pygame.time.get_ticks() - self.temporizador > 500 // self.velocidade:
            if self.esta_dentro(
                    self.posicao_x, self.posicao_y + 1, self.peca_atual):
                self.posicao_y += 1
            else:
                self.atualizar_matriz(self.posicao_x, self.posicao_y)
                self.novo_bloco()
                # self.draw_grid()
                if not self.esta_dentro(
                        self.posicao_x, self.posicao_y, self.peca_atual):
                    self.game_over = True
            self.temporizador = pygame.time.get_ticks()

    def rodar(self):
        while not self.game_over:
            self.limpar_tela()
            self.tratar_eventos()
            if self.menu_ativo:
                self.desenhar_menu()
            else:
                self.atualizar()
                self.desenhar_tela()
                self.draw_grid()
                self.remover_linhas()
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()


Tetris().rodar()
