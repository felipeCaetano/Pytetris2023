import pygame

pygame.init()

# Obter informações sobre a tela atual
info = pygame.display.Info()

# Obter largura e altura da tela
largura_tela = info.current_w
altura_tela = info.current_h
TAM_BLOCO = 30
LARG_TELA = 840
LARG_TAB = 600
FPS = 60
ALTURA_TELA = altura_tela - (altura_tela % TAM_BLOCO)
LARG_TABULEIRO = LARG_TAB // TAM_BLOCO
ALTURA_TABULEIRO = ALTURA_TELA // TAM_BLOCO - 2
print(ALTURA_TABULEIRO)
POSICAO_INI = LARG_TAB // TAM_BLOCO // 2 - 1
