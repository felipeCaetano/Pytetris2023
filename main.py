import random

import pygame

from colors import (PRETO, BRANCO, VERMELHO, AZUL, VERDE, AMARELO, CIANO, ROXO,
                    LARANJA)
from configs import (
    LARG_TELA, ALTURA_TELA, TAM_BLOCO, LARG_TABULEIRO,
    ALTURA_TABULEIRO, POSICAO_INI, FPS
)


# Peças do Tetris
PECAS = [
    [[1, 1, 1, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
]

cores_blocos = [VERMELHO, AZUL, VERDE, AMARELO, CIANO, ROXO, LARANJA]


class Tetris:
    def __init__(self):
        pygame.init()
        self.posicao_y = None
        self.posicao_x = None
        self.cor_da_peca = None
        self.peca_atual = None
        self.temporizador = pygame.time.get_ticks()
        self.tela = pygame.display.set_mode((LARG_TELA, ALTURA_TELA))
        pygame.display.set_caption("PyTetris")
        self.clock = pygame.time.Clock()
        self.tabuleiro = [
            [PRETO] * (LARG_TABULEIRO) for _ in range(ALTURA_TABULEIRO)]
        self.novo_bloco()
        self.velocidade = 1
        self.game_over = False
        self.menu_ativo = True
        self.opcoes = ["Iniciar Jogo", "Configurações", "Créditos", "Sair"]
        self.opcao_selecionada = 0

    def novo_bloco(self):
        self.peca_atual = self.criar_peca()
        self.cor_da_peca = random.choice(cores_blocos)
        self.posicao_x = POSICAO_INI
        self.posicao_y = 0

    def criar_peca(self):
        return random.choice(PECAS)

    def esta_dentro(self, pos_x, pos_y, peca):
        for i, linha in enumerate(peca):
            for j, bloco in enumerate(linha):
                if bloco == 1:
                    if not (
                            0 <= pos_x + j < LARG_TABULEIRO
                            and 0 <= pos_y + i + 1 < ALTURA_TABULEIRO
                    ) or self.tabuleiro[pos_y + i][pos_x + j] != PRETO:
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
            self.tabuleiro.insert(0, [PRETO] * LARG_TABULEIRO)

    def desenhar_blocos(self):
        for i in range(ALTURA_TABULEIRO):
            for j in range(LARG_TABULEIRO):
                cor = self.tabuleiro[i][j]
                self.desenhar_bloco(j * TAM_BLOCO, i * TAM_BLOCO, cor)

    def desenhar_bloco(self, posx, posy, cor):
        pygame.draw.rect(self.tela, BRANCO, (posx, posy - TAM_BLOCO, TAM_BLOCO, TAM_BLOCO), 1)
        pygame.draw.rect(self.tela, cor, (posx, posy, TAM_BLOCO, TAM_BLOCO))

    def desenhar_menu(self):
        for i, opcao in enumerate(self.opcoes):
            if i == self.opcao_selecionada:
                cor = AMARELO
            else:
                cor = BRANCO
            texto = pygame.font.Font(None, 36).render(opcao, True, cor)
            pos_x = (LARG_TELA- texto.get_width()) // 2
            pos_y = (ALTURA_TELA // 2) + i * 50
            self.tela.blit(texto, (pos_x, pos_y))

    def desenhar_tela(self):
        self.desenhar_blocos()
        for i, linha in enumerate(self.peca_atual):
            for j, bloco in enumerate(linha):
                if bloco == 1:
                    pygame.draw.rect(
                        self.tela,
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
                        self.opcao_selecionada = (
                                                         self.opcao_selecionada - 1
                                                 ) % len(self.opcoes)
                    elif event.key == pygame.K_DOWN:
                        self.opcao_selecionada = (
                                                         self.opcao_selecionada + 1
                                                 ) % len(self.opcoes)
                    elif event.key == pygame.K_RETURN:
                        if self.opcoes[
                            self.opcao_selecionada] == "Iniciar Jogo":
                            self.menu_ativo = False
                        elif self.opcoes[self.opcao_selecionada] == "Sair":
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
        if self.esta_dentro(self.posicao_x, self.posicao_y + 1, self.peca_atual):
            self.posicao_y += 1

    def move_right(self):
        if self.posicao_x < LARG_TABULEIRO - len(self.peca_atual[0])\
                and self.esta_dentro(self.posicao_x + 1, self.posicao_y, self.peca_atual):
            self.posicao_x += 1

    def move_left(self):
        if self.posicao_x > 0 and self.esta_dentro(self.posicao_x - 1, self.posicao_y, self.peca_atual):
            self.posicao_x -= 1

    def atualizar(self):
        if pygame.time.get_ticks() - self.temporizador > 500 // self.velocidade:
            if self.esta_dentro(
                    self.posicao_x, self.posicao_y + 1, self.peca_atual):
                self.posicao_y += 1
            else:
                self.atualizar_matriz(self.posicao_x, self.posicao_y)
                self.novo_bloco()

                if not self.esta_dentro(
                        self.posicao_x, self.posicao_y, self.peca_atual):
                    self.game_over = True

            self.temporizador = pygame.time.get_ticks()

    def desenhar_tela(self):
        self.desenhar_blocos()
        for i, linha in enumerate(self.peca_atual):
            for j, bloco in enumerate(linha):
                if bloco == 1:
                    pygame.draw.rect(
                        self.tela, self.cor_da_peca,
                        (
                            (self.posicao_x + j) * TAM_BLOCO,
                            (self.posicao_y + i) * TAM_BLOCO,
                            TAM_BLOCO, TAM_BLOCO
                        )
                    )

    def rodar(self):
        while not self.game_over:
            self.limpar_tela()
            self.tratar_eventos()
            if self.menu_ativo:
                self.desenhar_menu()
            else:
                self.atualizar()
                self.desenhar_tela()

                self.remover_linhas()
                # self.desenhar_tela()
                # self.atualizar()
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()


Tetris().rodar()
