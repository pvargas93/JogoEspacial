import pygame
import os
import json
import datetime

def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")

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

def desenhar_sol(tela):
    global raio_sol, crescendo
    if crescendo:
        raio_sol += 0.1
        if raio_sol >= 40:
            crescendo = False
    else:
        raio_sol -= 0.1
        if raio_sol <= 30:
            crescendo = True
    pygame.draw.circle(tela, (255, 255, 255), (950, 50), int(raio_sol + 10))  # halo
    pygame.draw.circle(tela, (255, 255, 240), (950, 50), int(raio_sol))        # centro

# Variáveis globais para o sol
raio_sol = 35
crescendo = True

def tela_historia(tela, fonte, cor_fonte, relogio):
    esperando = True
    historia = [
        "Em uma missão espacial, sua nave foi enviada para consertar",
        "uma estação espacial danificada. Na volta para a Terra,",
        "vocês foram surpreendidos por uma chuva de meteoros.",
        "",
        "Agora, como capitão da expedição, sua missão é desviar dos",
        "meteoritos e trazer a tripulação em segurança de volta ao planeta.",
        "",
        "Clique com o mouse para iniciar a missão."
    ]
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

        tela.fill((0, 0, 0))
        y = 150
        for linha in historia:
            sombra = fonte.render(linha, True, (30, 30, 30))
            texto = fonte.render(linha, True, cor_fonte)
            tela.blit(sombra, (102, y + 2))  # sombra
            tela.blit(texto, (100, y))       # texto principal
            y += 40

        pygame.display.update()
        relogio.tick(60)
