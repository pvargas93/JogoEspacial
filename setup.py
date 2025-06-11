from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('Recursos/imagens', [
        'Recursos/imagens/capaDoJogo.png',
        'Recursos/imagens/espaco.png',
        'Recursos/imagens/icone.png',
        'Recursos/imagens/meteoro.png',
        'Recursos/imagens/OnibusEspacial.png',
        'Recursos/imagens/TelaFimDoJogo.png'
    ]),
    ('Recursos/sons', [
        'Recursos/sons/impacto.wav',
        'Recursos/sons/SomBatalhaEspacial.wav',
        'Recursos/sons/SomInicioJogo.ogg',
        'Recursos/sons/SomMeteoro.wav'
    ]),
    ('Recursos', ['Recursos/funcoes.py']),
    ('', ['log.dat', 'base.atitus'])
]

OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame', 'tkinter', 'json', 'datetime'],
    'includes': ['os', 'random'],
    'iconfile': 'Recursos/imagens/icone.png'  # se quiser usar como ícone do app
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
