import pygame

pygame.init()

# Obter informações sobre a tela atual
info = pygame.display.Info()

# Obter largura e altura da tela
largura_tela = info.current_w
altura_tela = info.current_h

LARG_TELA = 600
ALTURA_TELA = info.current_h - 20
TAM_BLOCO = 30
FPS = 60
LARG_TABULEIRO = LARG_TELA // TAM_BLOCO
ALTURA_TABULEIRO = ALTURA_TELA // TAM_BLOCO
POSICAO_INI = LARG_TELA // TAM_BLOCO // 2 - 1
