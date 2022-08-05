from random import randint
import sys
import pygame
import os.path
import sys

class Moedas:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vivo = True
    
    def atualiza_estado(self, delta_t, state):
        '''Atualiza a posição x da moeda com base na velocidade dos obstáculos e da variação de tempo,
        e se ela sair da tela, é retirada da lista de moedas'''
        delta_sx = state['velocidade_obst'] * (delta_t/1000)
        self.x = self.x - delta_sx
        if self.x <= -30:
            state['moedas'] = []

    def desenha(self, w, assets):
        w.blit(assets['moeda'], (self.x, self.y))
    
    def pegou_moeda(self, assets, state):
        '''Verifica se o jogador colidiu com a moeda, caso sim, ele retira a moeda e soma no total das coletadas'''
        rect_moeda = pygame.rect.Rect(self.x, self.y, 30,30)
        rect_player = pygame.rect.Rect(state['player_x'], state['player_y'], 50, 60)
        if rect_moeda.colliderect(rect_player):
            if state['perdeu'] == False:
                assets['coin_som'].play()
            state['moedas'] = []
            state['moedas_coletadas'] += 1

class Coxinhas:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vivo = True
         
    def atualiza_estado(self, delta_t):
        '''Atualiza a posição x da coxinha com base na sua própria velocidade ("1200") e da variação de tempo'''
        delta_sx =  1200 * (delta_t/1000)
        self.x = self.x + delta_sx
        if self.x >= 1280:
            self.vivo = False

    def desenha(self, w, assets):
        w.blit(assets['coxinha'], (self.x, self.y))
    

class Inimigos():
    def __init__(self, state, x, y):
        self.vivo = True
        self.velocidade_y = state['velocidade_y'][randint(0,5)]
        self.x = x
        self.y = y

    def atualiza_estado(self, delta_t, assets, state):
        '''Atualiza as posições x e y dos inimigos com base na velocidade dos obstaculos
        e na sua própria velocidade y, além de criar condições para ele quicar quando encostar
        nas bordas superior e inferior'''
        state['velocidade_obst'] += 1 * (delta_t/1000)
        delta_sx =  state['velocidade_obst'] * (delta_t/1000)
        delta_sy =  self.velocidade_y * (delta_t/1000)
        self.x = self.x - delta_sx
        self.y = self.y - delta_sy
        if self.y <= 0 and self.y != -1000:
            self.velocidade_y = - self.velocidade_y
            self.y = 1
        elif self.y >= 670:
            self.velocidade_y = - self.velocidade_y
            self.y = 669
        if self.x <= -30:
            self.vivo = False
        for coxinha in state['coxinhas']:
            rect_coxinha = pygame.rect.Rect(coxinha.x, coxinha.y, 25, 20)
            inimigo_rect = pygame.rect.Rect(self.x, self.y, 30, 50)
            if rect_coxinha.colliderect(inimigo_rect):
                if state['perdeu'] == False:
                    assets['coxinha_monstro_som'].play()
                state['coxinhas'] = []
                self.y = -1000
                self.velocidade_y = 0
                state['pontuacao'] += 30

            


    def desenha(self, w, assets):
        w.blit(assets['monstro'], (self.x, self.y))
    
    def perdeu(self, delta_t, assets, state):
        '''Verifica se o jogador colidiu com o inimigo'''
        player = pygame.rect.Rect(state['player_x'], state['player_y'], 50, 60)
        inimigo_rect = pygame.rect.Rect(self.x, self.y, 30, 50)
        if player.colliderect(inimigo_rect):
            if state['perdeu'] == False:
                assets['alien_som'].play()
            return True
        else:
            return False

class Obstaculos:
    def __init__(self, x1, y1):
        '''O obstáculo é composto por um cano superior, e um inferior
        que é criado a partir da posição do primeiro'''
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1 + 700 
        self.x = self.x1
        self.vivo = True
    
    def atualiza_estado(self, delta_t, assets, state):
        '''Atualiza a posição x do obstáculo de acordo com sua própria velocidade e do intervalo de tempo,
        além de parar de desenhar a coxinha caso colida com ela'''
        state['velocidade_obst'] += 1 * (delta_t/1000)
        delta_s =  state['velocidade_obst'] * (delta_t/1000)
        self.x = self.x - delta_s
        self.x1 = self.x
        if self.x1 <= -70:
            self.vivo = False
        self.x2 = self.x1
        rect1 = pygame.rect.Rect(self.x1, self.y1, 70, 500)
        rect2 = pygame.rect.Rect(self.x2, self.y2, 70, 500)
        for coxinha in state['coxinhas']:
            rect_coxinha = pygame.rect.Rect(coxinha.x, coxinha.y, 25, 20)
            if rect_coxinha.colliderect(rect1):
                state['coxinhas'] = []
                
            elif rect_coxinha.colliderect(rect2):
                state['coxinhas'] = []
    
    def desenha(self, w, assets):
        w.blit(assets['cano'], (self.x1, self.y1))
        w.blit(assets['cano'], (self.x2, self.y2))

    def perdeu(self, delta_t, assets, state):
        '''Verifica se o jogador colidiu com o obstáculo'''
        rect1 = pygame.rect.Rect(self.x1, self.y1, 70, 500)
        rect2 = pygame.rect.Rect(self.x2, self.y2, 70, 500)
        player = pygame.rect.Rect(state['player_x'], state['player_y'], 50, 60)
        if player.colliderect(rect1) or player.colliderect(rect2):
            if state['perdeu'] == False:
                assets['cano_som'].play()
            return True
        else:
            return False



def inicializa3():
    '''Cria a tela, os states, faz o carregamento das imagens e sons,
    verifica os arquivos utilizados para armazenamento do record e moedas
    totais, e também inicia a trilha sonora'''
    pygame.init()
    w = pygame.display.set_mode((1280,720))
    pygame.display.set_caption('Jetpack Toshiride')
    pygame.key.set_repeat(5)
    state = {'player_x': 400, 'player_y': 200, 'last_updated': pygame.time.get_ticks(), 'perdeu': False,
     'pontuacao': 0, 'velocidade_obst': 300, 'ultima_coxinha': pygame.time.get_ticks(), 'velocidade': 0, 'velocidade_y': [-200,-300,-400,200,300,400,500], 'record': 0, 'tela': False,
     'coxinhas': [], 'moedas':[Moedas(1280, randint(30,690))], 'moedas_coletadas': 0, 'moedas_total': 0, 'last_frame_updated': pygame.time.get_ticks(), 'index_correndo': 0, 'index_voando': 0,
     'index_passos': 0, 'personagem': randint(0,1), 'reinicio_validacao': False,
     'obstaculos': [   
        Obstaculos(1280, randint(-390,0)),
        Obstaculos(2200, randint(-390,0))
    ]

    }
    if os.path.exists('record.txt'):
        with open('record.txt', 'r') as f:
            state['record'] = float(f.read())
    if os.path.exists('moedas_total.txt'):
        with open('moedas_total.txt', 'r') as f:
            state['moedas_total'] = float(f.read())

    assets = {'fundo': pygame.image.load('fundo.png').convert_alpha(), 'coxinha': pygame.image.load('coxinha.png'), 'monstro': pygame.image.load('monstro.png'),
    'cano': pygame.image.load('cano.png'), 'moeda': pygame.image.load('moeda.png'), 'menu': pygame.image.load('menu.png'), 'toshi_voando': [pygame.image.load('toshi_voando1.png'), pygame.image.load('toshi_voando2.png'), pygame.image.load('toshi_voando3.png')],
    'toshi_correndo': [pygame.image.load('toshi_correndo1.png'), pygame.image.load('toshi_correndo2.png'), pygame.image.load('toshi_correndo3.png'), pygame.image.load('toshi_correndo4.png'), pygame.image.load('toshi_correndo5.png')],
    'passos': [pygame.mixer.Sound('passosom1.ogg'), pygame.mixer.Sound('passosom2.ogg'), pygame.mixer.Sound('passosom3.ogg'), pygame.mixer.Sound('passosom4.ogg'), pygame.mixer.Sound('passosom5.ogg'), pygame.mixer.Sound('passosom6.ogg')], 'alien_som': pygame.mixer.Sound('alien_som.ogg'),
     'cano_som': pygame.mixer.Sound('cano_som.ogg'),'coin_som': pygame.mixer.Sound('coin_som.ogg'), 'coxinha_monstro_som': pygame.mixer.Sound('coxinha_monstro_som.ogg'), 'coxinha_som': pygame.mixer.Sound('coxinha_som.ogg'),
     'trilha_som': pygame.mixer.music.load('trilha_som.ogg'), 'igor_correndo': [pygame.image.load('igor_correndo1.png'), pygame.image.load('igor_correndo2.png'), pygame.image.load('igor_correndo3.png'), pygame.image.load('igor_correndo4.png'), pygame.image.load('igor_correndo5.png')],
     'igor_voando': [pygame.image.load('igor_voando1.png'), pygame.image.load('igor_voando2.png'), pygame.image.load('igor_voando3.png')], 'personagem_correndo': [], 'personagem_voando': []
    }
    pygame.mixer.music.play(-1)
    return w, assets, state

def finaliza():
    pygame.quit()
    sys.exit()

def desenha(w: pygame.Surface, assets, state):
    '''Desenha o personagem, a coxinha, os obstáculos, o score, as moedas
    coletadas e os inimigos, além de atualizar o state dos indíces do
    personagem para criar sua animação'''
    if state['perdeu'] == False:
        pygame.mixer.music.play
    w.fill((0,0,0))
    w.blit(assets['fundo'], (0,0))
    for moeda in state['moedas']:
        moeda.pegou_moeda(assets, state)
        moeda.desenha(w, assets)
    for coxinha in state['coxinhas']:
        coxinha.desenha(w, assets)
    for obstac in state['obstaculos']:
        obstac.desenha(w, assets)

    if state['player_y'] >= 660:
        if pygame.time.get_ticks() - state['last_frame_updated'] >= 100:
            state['last_frame_updated'] = pygame.time.get_ticks()
            state['index_correndo'] += 1
            if state['index_correndo'] >= 5:
                state['index_correndo'] = 0

            if state['index_passos'] < 5:
                state['index_passos'] += 1
            else:
                state['index_passos'] = 0
            assets['passos'][state['index_passos']].play()
        w.blit(assets['personagem_correndo'][state['index_correndo']], (state['player_x'], state['player_y']))
        
    else:
        if pygame.time.get_ticks() - state['last_frame_updated'] >= 100:
            state['last_frame_updated'] = pygame.time.get_ticks()
            state['index_voando'] += 1
            if state['index_voando'] >= 3:
                state['index_voando'] = 0
        w.blit(assets['personagem_voando'][state['index_voando']], (state['player_x'], state['player_y']))
    font = pygame.font.match_font('bauhaus93')
    def_font = pygame.font.Font(font, 22)
    text = def_font.render(f"{state['pontuacao']:.0f}", True, (255,255,255))
    w.blit(text, (1220,20))
    w.blit(assets['moeda'], (30,30))
    text = def_font.render(f"{state['moedas_coletadas']}", True, (255,255,255))
    w.blit(text, (70,35))
    pygame.display.update()


def reiniciar_state(state):
    '''Reseta os valores do dicionario state quando o jogo reiniciar'''
    state['player_x'] = 400
    state['player_y'] = 200
    state['last_updated'] =  pygame.time.get_ticks()
    state['perdeu'] = False
    state['pontuacao'] = 0
    state['velocidade_obst'] = 300
    state['ultima_coxinha'] = pygame.time.get_ticks()
    state['velocidade'] = 0 
    state['velocidade_y'] = [-200,-300,-400,200,300,400,500]
    state['tela'] = False
    state['coxinhas'] = []
    state['moedas'] = [Moedas(1280, randint(30,690))]
    state['moedas_coletadas'] = 0
    state['last_frame_updated'] = pygame.time.get_ticks()
    state['index_correndo'] = 0
    state['index_voando'] = 0
    state['index_passos'] = 0
    state['personagem'] = randint(0,1)
    state['reinicio_validacao'] = False,
    state['obstaculos'] = [   
    Obstaculos(1280, randint(-390,0)),
    Obstaculos(2200, randint(-390,0))
    ]
    pygame.mixer.music.play(-1)


def recebe_eventos(w, assets, state):
    '''Recebe as ações do jogador (atirar, voar, e demais interações), e define as condições
    para cada uma delas,como por exemplo, impedir que ele suba mais do que o tamanho da tela,
    cria novos obstáculos, moedas e inimigos quando o anterior sumir, e define também com qual
    personagem o jogador irá jogar (de forma aleatória) '''
    tempo = pygame.time.get_ticks()
    delta_t = tempo - state['last_updated']
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP:
                if state['velocidade'] < 0 and state['player_y'] > 0:
                        state['velocidade'] -= 5
                else: 
                    if state['player_y'] > 0:
                        state['velocidade'] = -100
                state['player_y'] = state['player_y'] + state['velocidade'] * (delta_t/1000)
            if ev.key == pygame.K_SPACE and state['perdeu'] == False and (tempo - state['ultima_coxinha']) > 1000:
                if state['perdeu'] == False:
                    assets['coxinha_som'].play()
                state['coxinhas'].append(Coxinhas(state['player_x'] + 30, state['player_y'] + 20 ))
                state['ultima_coxinha'] = tempo
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                (590, 410, 115, 52)
                if ev.pos[0] >= 590 and ev.pos[0] <= 705 and ev.pos[1] >= 410 and ev.pos[1] <= 460 and state['reinicio_validacao'] == True:
                    reiniciar_state(state)

    state['velocidade'] = state['velocidade'] + 400 * (delta_t/1000)
    if state['player_y'] >= 660:
        state['player_y'] = 660
    elif state['player_y'] <= 0:
        state['player_y'] = 0
        state['velocidade'] = 10
        state['velocidade'] = state['velocidade'] + 600 * (delta_t/1000)
        state['player_y'] = state['player_y'] + state['velocidade'] * (delta_t/1000)
    else:
        state['player_y'] = state['player_y'] + state['velocidade'] * (delta_t/1000)
    for obstac in state['obstaculos']:
        obstac.atualiza_estado(delta_t, assets, state)
        if obstac.perdeu(delta_t, assets, state):
            state['perdeu'] = True
    for coxinha in state['coxinhas']:
        coxinha.atualiza_estado(delta_t)
    for moeda in state['moedas']:
        moeda.atualiza_estado(delta_t, state)
    if not state['perdeu']:
        v = 300 + 1 * (delta_t/1000)
        state['pontuacao'] = state['pontuacao'] + v * (delta_t/1000) / 100
    if state['pontuacao'] > state['record']:
        state['record'] = state['pontuacao']

    novos_obstaculos = []
    for obstac in state['obstaculos']:
        if obstac.vivo == True:
            novos_obstaculos.append(obstac)
        else:
            aleatorio = randint(0,1)
            # 0 = inimigo
            # 1 = obstaculo
            if aleatorio == 0:
                novos_obstaculos.append(Inimigos(state, 1500, randint(0,650)))
                
            else:
                novos_obstaculos.append(Obstaculos(1500, randint(-390,0)))
                
    state['obstaculos'] = novos_obstaculos

    if state['moedas'] == []:
        state['moedas'].append(Moedas(1280, randint(30,690)))
                
    if state['personagem'] == 0:
        assets['personagem_correndo'] = assets['toshi_correndo']
        assets['personagem_voando'] = assets['toshi_voando']
    else:
        assets['personagem_correndo'] = assets['igor_correndo']
        assets['personagem_voando'] = assets['igor_voando']

    state['last_updated'] = tempo
    return True


def tela(w, assets, state):
    '''Cria a tela de fim de jogo'''
    w.blit(assets['menu'], (390,210))
    font = pygame.font.match_font('bauhaus93')
    def_font = pygame.font.Font(font, 16)
    try:    
        text_record = def_font.render(f"{state['record']:.0f}", True, (255,100,120))
    except:
        text_record = def_font.render(f"{state['pontuacao']:.0f}", True, (255,100,120))
    text_pontuacao = def_font.render(f"{state['pontuacao']:.0f}", True, (255,100,120))
    w.blit(text_record, (653,269))
    w.blit(text_pontuacao, (665,389))
    state['reinicio_validacao'] = True
    pygame.display.update()
    return True


def gameloop3(w, assets, state):
    '''
    Aqui eh criado os arquivos txt para salvar os dados do jogo apos o fim do jogo
    '''
    verificador = True
    while recebe_eventos(w, assets, state):
        if not state['perdeu']:
            desenha(w, assets, state)
        else: 
            pygame.mixer.music.stop()
            tela(w, assets, state)
            if os.path.exists('record.txt'):
                with open('record.txt', 'r') as f:
                    valor = float(f.read())
                if state['record'] > valor:
                    with open('record.txt', 'w') as f:
                        f.write(str(state['record']))
            else:
                with open('record.txt', 'w') as f:
                    f.write(str(state['record']))
            if os.path.exists('moedas_total.txt'):
                with open('moedas_total.txt', 'r') as f:
                    valor = float(f.read())
                if verificador == True:
                    with open('moedas_total.txt', 'w') as f:
                        f.write(str(state['moedas_coletadas'] + valor))
                    verificador = False
            else:
                with open('moedas_total.txt', 'w') as f:
                    f.write(str(state['moedas_coletadas']))
                verificador = False
    finaliza()


if __name__ == '__main__':
    window, assets, state = inicializa3()
    gameloop3(window, assets, state)
    finaliza()