import math
from numpy import sort
import _thread
import random
import sys
import colorama

colorama.init()  # https://stackoverflow.com/a/64362146/4072641

# num jogo War da Grow, na média, o atacante perde 1,71 exércitos para cada 1 exército perdido da defesa.
# quando posso atacar (defesa x ataque = %vitória):
#     1x2 =75%
#     2x3 =66%
#     3x5 =57%
#     4x6 =52%
#     5x8 =54%
#     6x10=56%
#     7x11=51%
#     8x13=52%
#     9x15=54%
#    10x17=55%
#    11x18=51%
#    12x20=53%
#    13x22=54%
#    14x23=51%
#    15x25=52%


def input_thread(a_list):
    input()
    a_list.append(True)


def main():
    global a_list

    _thread.start_new_thread(input_thread, (a_list,))  # https://stackoverflow.com/a/25442391/4072641

    maxbatalhas = int(sys.argv[1]) if len(sys.argv) > 1 else math.inf
    qtddefensores = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    qtdatacantes = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    qtdbatalhas = 0
    qtdvitoriasataque = 0
    qtdderrotasataque = 0

    print("atacantes:", qtdatacantes, "defensores:", qtddefensores)

    while not a_list and qtdbatalhas < maxbatalhas:
        qtdataques, qtdatacantesrestantes, qtddefensoresrestantes, totalbaixasataque, totalbaixasdefesa = batalhar(qtdatacantes, qtddefensores)
        qtdbatalhas += 1
        if qtdatacantesrestantes > qtddefensoresrestantes:
            qtdvitoriasataque += 1
        else:
            qtdderrotasataque += 1
        taxa = qtdvitoriasataque/qtdderrotasataque if qtdderrotasataque > 0 else qtdvitoriasataque
        vitoriaspercent = qtdvitoriasataque/(qtdvitoriasataque+qtdderrotasataque)
        derrotaspercent = qtdderrotasataque/(qtdvitoriasataque+qtdderrotasataque)
        print("batalhas", "atacantesrestantes", "defensoresrestantes", "qtdvitorias", "qtdderrotas", "taxa", "vit", "der")
        print("%8d %18d %19d %11d %11d %.2f %.2f %.2f" % (qtdbatalhas, qtdatacantesrestantes, qtddefensoresrestantes, qtdvitoriasataque, qtdderrotasataque, taxa, vitoriaspercent, derrotaspercent))
        print("\033[A\033[A\033[A\033[A", end="")
    print("\n\n\n")


def batalhar(qtdatacantes, qtddefensores):
    global a_list

    qtdataques = 0
    totalbaixasdefesa = 0
    totalbaixasataque = 0

    while qtdatacantes > 0 and qtddefensores > 0 and not a_list:
        ataque = randlist(qtdatacantes)
        defesa = randlist(qtddefensores)

        baixasdefesa = 0
        baixasataque = 0

        qtd = len(defesa) if len(defesa) < len(ataque) else len(ataque)

        for i in range(qtd):
            if(ataque[i] > defesa[i]):
                baixasdefesa += 1
            else:
                baixasataque += 1

        totalbaixasataque += baixasataque
        totalbaixasdefesa += baixasdefesa
        taxa = totalbaixasataque/totalbaixasdefesa if totalbaixasdefesa > 0 else totalbaixasataque
        qtdatacantes -= baixasataque
        qtddefensores -= baixasdefesa
        qtdataques += 1

        print("qtdataques", "qtdatacantes", "qtddefensores", "totalbaixasataque", "totalbaixasdefesa",  "taxa")
        print("%10d %12d %13d %17d %17d %.2f" % (qtdataques, qtdatacantes, qtddefensores, totalbaixasataque, totalbaixasdefesa, taxa))
        print("\033[A\033[A", end="")
    print("\n")
    return [qtdataques, qtdatacantes, qtddefensores, totalbaixasataque, totalbaixasdefesa]


def randlist(qtd):
    list = []
    for i in range(min(3, qtd)):
        list.append(random.randint(1, 6))
    list.sort(reverse=True)
    return list


a_list = []
if __name__ == "__main__":
    main()
