import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from criativo import rodar_formatos as rodar
CFG = dict(
    id="c4", ref="referencias/criativo-4", saida="saidas/criativo-4-v1.mp4",
    titulo=["Quem entra primeiro", "fica com o mercado"],
    t_gancho=5.35, t_titulo=12.80, legenda_desde="existe",
    gancho=[
        (0.00, 1.40, "pag1.png", 0.0, (0, 500, 1080, 1460)),        # Diário do Comércio: pequenos negócios do Brasil usam mais IA
        (1.40, 2.70, "exame-tiago-palco.jpg", 0.45, None),
        (2.70, 4.00, "pag2.png", 0.0, (0, 200, 1080, 1100)),        # Agência Sebrae
        (4.00, 5.35, "pag4.png", 0.0, (0, 430, 1080, 1560)),        # Exame: a era do lead barato acabou
    ],
    cutaways=[(16.60, 19.30, "pag1.png", 0.0, (0, 500, 1080, 1460)), (19.30, 21.90, "pag1.png", 0.5, (0, 900, 1080, 1500))],
    repl={109: (1, ["lead"]), 111: (3, ["3", "da", "manhã,"]), 173: (1, ["IA"]), 181: (1, ["agenda"])},
    frases="""E aqui, | eu vou explicar o porquê | na prática, tá? | Primeiro, custo. | Você faz com a IA | o que antes exigia | três ferramentas caras | e mais gente na equipe. | Segundo, lucro. | Você para de queimar dinheiro | em anúncio ruim | e também | em um processo lento. | E o que sobra | no fim do mês | acaba aumentando.
Terceiro, | e esse é o que mais dói | no seu concorrente. | A sua operação | fica ligada | 24 horas por dia. | O lead chegou | 3 da manhã, | foi atendido por uma IA | e já foi qualificado | pela IA. | Campanha fora da curva | no domingo. | Alguém viu, clicou | e a IA fez o resto. | Enquanto ele dorme, | você vende. | Enquanto ele contrata, | você automatiza.
É isso que a gente implementa | dentro do novo | Conversão Extrema | na era | da inteligência artificial, | mesmo que você | não entenda nada | de IA hoje. | Clica no link aqui embaixo | e agenda uma reunião | comigo e com o meu time, | que eu vou te explicar | tudo em detalhes, | como implementar IA | na sua operação, | no seu marketing, | no seu tráfego | e vai fazer você | lucrar muito mais. | Só que seja rápido, tá? | Clica aqui e bora.""",
    enquadro=lambda t: (1.15, 0.33),
)
rodar(CFG)
