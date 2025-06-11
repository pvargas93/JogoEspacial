import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from Recursos.funcoes import escreverDados, desenhar_sol, tela_historia
import json
import datetime

# Configuração para compatibilidade no MacOS
# MacOS: corrige Bug
if os.name == "posix":
    root = tk.Tk()
    root.update()
    root.destroy()

# Inicializações
pygame.init()

# Tela principal
largura_tela, altura_tela = 1000, 700
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo Espacial")
relogio = pygame.time.Clock()

# Ícone
icone = pygame.image.load("Recursos/imagens/icone.png")
pygame.display.set_icon(icone)

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Fontes
fonteMenu = pygame.font.SysFont("comicsans", 18)
fonteMorte = pygame.font.SysFont("arial", 60)
fontePequena = pygame.font.SysFont("arial", 20)
fonteHistoria = pygame.font.SysFont("arial", 28)

# Imagens
nave = pygame.image.load("Recursos/imagens/OnibusEspacial.png")
nave = pygame.transform.scale(nave, (300, 200))

fundoInicio = pygame.image.load("Recursos/imagens/capaDoJogo.png")
fundoInicio = pygame.transform.scale(fundoInicio, (1000, 700))

fundoGame = pygame.image.load("Recursos/imagens/espaco.png")
fundoGame = pygame.transform.scale(fundoGame, (1000, 700))

meteoro = pygame.image.load("Recursos/imagens/meteoro.png")
meteoro = pygame.transform.scale(meteoro, (120, 200))

# Sons
SomMeteoro = pygame.mixer.Sound("Recursos/sons/SomMeteoro.wav")
ExplosaoImpacto = pygame.mixer.Sound("Recursos/sons/impacto.wav")
SomInicio = "Recursos/sons/SomInicioJogo.ogg"
SomJogo = "Recursos/sons/SomBatalhaEspacial.wav"

# Globais
nome = ""

# Funções auxiliares
def escreverDados(nick, pontos):
    now = datetime.datetime.now()
    dados = {
        "nickname": nick,
        "pontos": pontos,
        "data": now.strftime("%d/%m/%Y"),
        "hora": now.strftime("%H:%M:%S")
    }
    if os.path.exists("log.dat"):
        with open("log.dat", "r") as f:
            registros = json.load(f)
    else:
        registros = []
    registros.append(dados)
    with open("log.dat", "w") as f:
        json.dump(registros[-5:], f, indent=4)

def dead(pontos):
    pygame.mixer.music.stop()
    ExplosaoImpacto.play()
    pygame.time.delay(1000)

    fundoEnd = pygame.image.load("Recursos/imagens/TelaFimDoJogo.png")
    fundoEnd = pygame.transform.scale(fundoEnd, (largura_tela, altura_tela))
    tela.blit(fundoEnd, (0, 0))

    texto_gameover = fonteMorte.render("GAME OVER", True, branco)
    tela.blit(texto_gameover, (largura_tela // 2 - texto_gameover.get_width() // 2, 80))

    if os.path.exists("log.dat"):
        with open("log.dat", "r") as f:
            registros = json.load(f)
    else:
        registros = []

    y = 200
    for registro in registros:
        texto = f"{registro['nickname']} - {registro['pontos']} pontos - {registro['data']} {registro['hora']}"
        texto_render = fontePequena.render(texto, True, branco)
        tela.blit(texto_render, (largura_tela // 2 - texto_render.get_width() // 2, y))
        y += 40

    pygame.display.update()
    pygame.time.delay(4000)
    start()

def start():
    larguraButtonStart = 150
    alturaButtonStart = 40
    larguraButtonQuit = 150
    alturaButtonQuit = 40

    pygame.mixer.music.load(SomInicio)
    pygame.mixer.music.play(-1, fade_ms=1000)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.mixer.music.stop()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    nome = solicitar_nome()
                    tela_historia(tela, fonteHistoria, branco, relogio)
                    pygame.mixer.music.stop()
                    jogar(nome)
                elif quitButton.collidepoint(evento.pos):
                    pygame.mixer.music.stop()
                    quit()

        tela.fill(branco)
        tela.blit(fundoInicio, (0, 0))

        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 12))

        quitButton = pygame.draw.rect(tela, branco, (10, 60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25, 62))

        pygame.display.update()
        relogio.tick(60)

def solicitar_nome():
    largura_janela = 300
    altura_janela = 50
    nome_jogador = ""

    def obter_nome():
        nonlocal nome_jogador
        nome_jogador = entry_nome.get()
        if not nome_jogador:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    largura_tela_win = root.winfo_screenwidth()
    altura_tela_win = root.winfo_screenheight()
    pos_x = (largura_tela_win - largura_janela) // 2
    pos_y = (altura_tela_win - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()
    root.mainloop()

    return nome_jogador

def jogar(nome):
    pygame.mixer.music.load(SomJogo)
    pygame.mixer.music.play(-1)

    posicaoXNave = 410
    posicaoYNave = 480
    movimentoXNave = 0

    posicaoXMeteoro = random.randint(0, 700)
    posicaoYMeteoro = -200
    velocidadeMeteoro = 1
    pontos = 0

    larguraNave = 300
    alturaNave = 200
    larguraMeteoro = 120
    alturaMeteoro = 200
    margemImpacto = 30

    pygame.mixer.Sound.play(SomMeteoro)

    pausado = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXNave = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXNave = -15
                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoXNave = 0

        if pausado:
            continue

        posicaoXNave += movimentoXNave

        if posicaoXNave < 0:
            posicaoXNave = 0
        elif posicaoXNave > largura_tela - larguraNave:
            posicaoXNave = largura_tela - larguraNave

        tela.fill(branco)
        tela.blit(fundoGame, (0, 0))
        tela.blit(nave, (posicaoXNave, posicaoYNave))

        desenhar_sol(tela)

        posicaoYMeteoro += velocidadeMeteoro
        if posicaoYMeteoro > altura_tela:
            posicaoYMeteoro = -200
            pontos += 1
            velocidadeMeteoro += 1
            posicaoXMeteoro = random.randint(0, largura_tela - larguraMeteoro)
            pygame.mixer.Sound.play(SomMeteoro)

        tela.blit(meteoro, (posicaoXMeteoro, posicaoYMeteoro))

        texto = fonteMenu.render("Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (15, 15))

        textoPause = fonteMenu.render("Press SPACE to Pause Game", True, branco)
        tela.blit(textoPause, (150, 15))

        pixelsNaveX = list(range(posicaoXNave + margemImpacto, posicaoXNave + larguraNave - margemImpacto))
        pixelsNaveY = list(range(posicaoYNave + margemImpacto, posicaoYNave + alturaNave - margemImpacto))
        pixelsMeteoroX = list(range(posicaoXMeteoro, posicaoXMeteoro + larguraMeteoro))
        pixelsMeteoroY = list(range(posicaoYMeteoro, posicaoYMeteoro + alturaMeteoro))

        if set(pixelsMeteoroY).intersection(pixelsNaveY) and set(pixelsMeteoroX).intersection(pixelsNaveX):
            escreverDados(nome, pontos)
            dead(pontos)

        pygame.display.update()
        relogio.tick(60)

# Iniciar o jogo
start()
