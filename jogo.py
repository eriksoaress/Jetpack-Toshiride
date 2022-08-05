import pygame
from menu_help import *
from Jetpack_Toshiride import *
import os.path
import sys

def inicializar():
    '''
    Inicializa o pygame e cria a tela. Retorna um dicionário com as imagens e fontes. 
    Arquivos txt para moedas e best score são criados se não existirem.
    '''
    pygame.init()
    screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Menu")
    default_font = pygame.font.get_default_font()

    assets = {}
    assets['font_16'] = pygame.font.Font(default_font, 16)
    assets['font_32'] = pygame.font.Font(default_font, 32)

    state = {}
    if os.path.exists('record.txt'):
        with open('record.txt', 'r') as f:
            state['best_score'] = float(f.read())
    if os.path.exists('moedas_total.txt'):
        with open('moedas_total.txt', 'r') as f:
            state['moedas_total'] = float(f.read())
    state['pagina'] = 0

    return screen, assets, state

def finaliza():
    pygame.quit()
    sys.exit()

def render_text(screen, assets, text, x, y):
    '''
    aqui é onde o texto é renderizado na tela
    '''
    font = assets['font_16']
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def colisao_ponto_retangulo(x, y, rect):
    if x >= rect[0] and x <= rect[0] + rect[2] and y >= rect[1] and y <= rect[1] + rect[3]:
        return True
    return False

def atualiza_estado(screen, assets, state):
    '''
    Aqui é onde o menu é renderizado na tela
    '''
    screen.fill((0, 0, 0))
    render_text(screen, assets, "Menu", 250, 50)
    try:
        render_text(screen, assets, f"best score: {state['best_score']:.0f}", 250, 75)
    except:
        render_text(screen, assets, "best score: 0", 250, 75)
    try:
        render_text(screen, assets, f"moedas total: {state['moedas_total']:.0f}", 250, 100)
    except:
        render_text(screen, assets, "moedas total: 0", 250, 100)
    render_text(screen, assets, "|JOGAR|", 250, 150)
    render_text(screen, assets, "|HELP|", 250, 200)
    render_text(screen, assets, "|SAIR|", 250, 250)
    pygame.display.flip()
    pygame.display.update()

def game_loop(screen, assets, state):
    '''
    Aqui é onde o jogo é executado, conferindo se o jogador clicou em alguma das opções do menu
    '''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if colisao_ponto_retangulo(event.pos[0], event.pos[1], (200, 125, 100, 50)):
                    running = False
                    state['pagina'] = 2
                elif colisao_ponto_retangulo(event.pos[0], event.pos[1], (200, 175, 100, 50)):
                    running = False
                    state['pagina'] = 1
                elif colisao_ponto_retangulo(event.pos[0], event.pos[1], (200, 225, 100, 50)):
                    running = False
                    finaliza()
            if event.type == pygame.QUIT:
                running = False
                finaliza()
        atualiza_estado(screen, assets, state)

screen, assets, state = inicializar()
game_loop(screen, assets, state)
while True:
    '''
    Aqui é onde o jogo é executado, conferindo se o jogador clicou em alguma das opções do menu para poder trocar de tela
    '''
    if state['pagina'] == 0:
        pygame.quit()
        screen, assets, state = inicializar()
        game_loop(screen, assets, state)
    elif state['pagina'] == 1:
        pygame.quit()
        screen, assets = inicializar2()
        game_loop2(screen, assets)
        state['pagina'] = 0
    elif state['pagina'] == 2:
        pygame.quit()
        window, assets, state = inicializa3()
        gameloop3(window, assets, state)
        state['pagina'] = 0