import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from reels2 import rodar
V = lambda t0, t1, src, ini, foco=0.5, rec=None: dict(t0=t0, t1=t1, tipo="video", src=src, ini=ini, foco=foco, rec=rec)
I = lambda t0, t1, src, rec=None, foco=0.0: dict(t0=t0, t1=t1, tipo="img", src=src, rec=rec, foco=foco)
CNNTOP = (0, 0, 1920, 890)          # tira o lower-third da CNN
CFG = dict(
    id="r5", ref="referencias/reel-ia-humanidade", saida="saidas/reel-ia-humanidade-v2.mp4",
    t_cheia=61.90,                  # "Você provavelmente já viveu essa lógica"
    topo=[
        # recortes conferidos quadro a quadro (fonte 1920x1080): CNN = só a caixa de conteúdo à direita; Forbes = sem a legenda de baixo; Gênova 1280x720 sem o bug do tempo
        # "um ex-funcionário da OpenAI e da Anthropic confessou que a IA pode acabar com a humanidade até 2030"
        V(0.00, 3.30, "cbs-coxon.mp4", 62.0),                                       # Coxon (CBS)
        V(3.30, 5.60, "bbc-coxon.mp4", 21.5, 0.5, (380, 100, 1540, 880)),              # post de demissão dele no X ("racing straight to self-improving superintelligence")
        I(5.60, 10.10, "metropoles.png", (0, 240, 1080, 1140)),                    # Metrópoles
        # "deixa eu explicar por que isso importa"
        I(10.10, 13.10, "newsweek.png", (0, 80, 1080, 980)),                       # Newsweek: Who Is Jacob Coxon?
        # "O nome dele é Jacob Coxon, pesquisador que passou três anos treinando a IA da OpenAI e da Anthropic"
        V(13.10, 18.00, "bbc-coxon.mp4", 56.0),                                     # Coxon (BBC)
        V(18.00, 21.20, "forbes-hubinger.mp4", 54.0, 0.5, (200, 0, 1720, 760)),      # logos OpenAI e Anthropic (sem legenda)
        # "ele não é da área de segurança, ele construía a tecnologia"
        V(21.20, 25.90, "bbc-coxon.mp4", 14.0, 0.5, (60, 40, 1140, 1000)),        # ele na tela do notebook (BBC)
        # "é o engenheiro da ponte dizendo que a ponte não aguenta"
        V(25.90, 29.30, "ponte-genova.mp4", 9.6, 0.5, (180, 90, 900, 640)),       # ponte de Gênova, plano aberto (9,6–13 s)
        V(29.30, 32.30, "ponte-genova.mp4", 13.2, 0.5, (100, 60, 1180, 560)),      # escombros (13,2–16 s, corte acima da legenda)        # ponte de Gênova, sem o bug do tempo
        # "o chefe de alinhamento da Anthropic, Evan Hubinger, concordou publicamente"
        V(32.30, 35.70, "cnn-amodei.mp4", 48.0, 0.5, (60, 40, 1560, 720)),         # post do Hubinger (CNN, 48–51,5 s)
        V(35.70, 37.70, "bbc-coxon.mp4", 66.0),                                     # Coxon (BBC)       # post do Hubinger (caixa da CNN)
        # "mais de 10% de chance na próxima década"
        V(37.70, 41.20, "forbes-hubinger.mp4", 4.0, 0.5, (300, 0, 1620, 1080)),       # Forbes: ">10% chance AI could kill all humans"
        V(41.20, 45.80, "forbes-hubinger.mp4", 32.0, 0.5, (0, 0, 1100, 650)),      # Anthropic no celular
        # "por que ninguém para a IA? Está escrito no próprio texto do Coxon"
        V(45.80, 50.70, "cnn-coxon.mp4", 26.0, 0.5, (580, 130, 1880, 730)),        # post do Coxon (caixa da CNN)
        I(50.70, 54.60, "nbc.png", (0, 200, 1080, 1100)),                          # NBC: resigned with a warning
        # "cada empresa acredita que as outras vão agir com responsabilidade... prefere chegar primeiro"
        V(54.60, 58.10, "bbc-coxon.mp4", 9.5, 0.5, (380, 60, 1540, 860)),            # Slack "Greetings, whoever you are" (BBC)
        V(58.10, 61.90, "cbs-coxon.mp4", 40.0),                                     # Coxon (CBS)
    ],
    repl={3: (2, ["ex-funcionário"]), 9: (1, ["Anthropic"]), 42: (2, ["Jacob", "Coxon,"]), 56: (1, ["Anthropic."]), 74: (1, ["ponte."]), 79: (1, ["ponte"]), 83: (1, ["ponte"]),
          91: (1, ["Anthropic,"]), 92: (2, ["Evan", "Hubinger,"]), 104: (2, ["10%"]), 126: (1, ["Coxon."]), 288: (2, ["SDR"])},
    frases="""É, galera, | um ex-funcionário | da OpenAI | e da Anthropic | confessou | que a IA | pode acabar | com a humanidade | até 2030. | Deixa eu explicar | por que isso importa | para você. | O motivo? | Você já viveu | no seu negócio.
O nome dele | é Jacob Coxon, | pesquisador | que passou três anos | treinando a IA | da OpenAI | e da Anthropic. | Ele não é | da área de segurança. | Ele construía | apenas a tecnologia. | É basicamente | um engenheiro da ponte. | É o engenheiro da ponte | dizendo | que a ponte não aguenta.
O chefe de alinhamento | da Anthropic, | Evan Hubinger, | concordou publicamente | isso. | Ele disse achar | que existe | mais de 10% de chance | disso acontecer | na próxima década. | Então, | por que ninguém | para a IA? | Está escrito | no próprio texto | do Coxon. | Cada empresa acredita | que as outras | vão agir | com responsabilidade. | Então, prefere | chegar primeiro, | mesmo achando perigoso, | porque é pior | deixar o concorrente | chegar antes.
Você provavelmente | já viveu essa lógica. | Quando o concorrente | da sua rua, | lá ele baixou o preço | e você vai lá | e baixa também, | sabendo | que ia até destruir | a margem dos dois. | Você mesmo assim, | baixa, | impactando o seu negócio | porque ele baixou. | E na verdade | o cliente ganha, | mas vocês dois | perderam. | Os dois passaram | a trabalhar mais | e ganhar menos. | É a mesma armadilha, | só que muda o tamanho. | A saída | também é a mesma, | parar de competir | na coisa | que todo mundo compete. | Quando você é o único | que responde rápido, | o preço | ele deixa de ser | o critério.
Se você quer parar | de perder cliente | para quem responde primeiro, | a gente criou uma IA, | que atende o seu lead | no WhatsApp | na hora | e a qualquer hora. | Então, olha só, | comenta SDR | aqui embaixo | que o meu time | vai te chamar | no Direct | e te explicar | como nós colocamos | uma IA | para responder | os seus leads | automaticamente | no WhatsApp. | Você vai responder | primeiro, | melhor, | qualificar os leads | e magicamente, | vender mais, | lucrar mais. | Então, escreva aqui, | SDR.""",
    enquadro=lambda t: (1.25, 0.33),
)
rodar(CFG)
