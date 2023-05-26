import pygame

pygame.init()

# Obter informações sobre a tela atual
info = pygame.display.Info()

# Obter largura e altura da tela
scr_width = info.current_w
scr_height = info.current_h
LEN_BLOCK = 30
SCR_WIDTH = 840
WIDTH_TAB = 600
FPS = 60
SCR_HEIGHT = scr_height - (scr_height % LEN_BLOCK)
BOARD_WIDTH = WIDTH_TAB // LEN_BLOCK
BOARD_HEIGHT = SCR_HEIGHT // LEN_BLOCK - 2
INIT_POS = WIDTH_TAB // LEN_BLOCK // 2 - 1
