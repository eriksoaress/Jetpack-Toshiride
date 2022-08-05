import pygame
import sys

def inicializar2():
    '''
    Inicializa o pygame e cria a tela e retorna um dicionário com as imagens e fontes.
    Arquivos txt para moedas e best score são criados se não existirem.
    '''
    pygame.init()
    screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Menu")
    default_font = pygame.font.get_default_font()

    assets = {}
    assets['font_16'] = pygame.font.Font(default_font, 16)
    assets['font_32'] = pygame.font.Font(default_font, 32)

    return screen, assets

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

def atualiza_estado(screen, assets, estado):
    '''
    Aqui é onde o menu é renderizado na tela
    '''
    screen.fill((0, 0, 0))
    render_text(screen, assets, "Help Menu", 250, 50)
    render_text(screen, assets, "seta para cima = Voar", 250, 150)
    render_text(screen, assets, "Barra de espaço = Atirar", 250, 200)
    render_text(screen, assets, "Retornar para o menu", 250, 250)
    pygame.display.flip()
    pygame.display.update()

def game_loop2(screen, assets):
    '''
    Aqui é onde o menu é renderizado na tela
    Ao clicar Retornar para o menu, o programa retorna para o menu principal
    '''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if colisao_ponto_retangulo(event.pos[0], event.pos[1], (200, 225, 100, 50)):
                    running = False
        atualiza_estado(screen, assets, "menu")
    pygame.quit()
    
    

