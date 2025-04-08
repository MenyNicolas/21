import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
import ENVIRONNEMENT.utils_env as utils_env

from IA.IA import IA_BJ

# === CONFIGURATION SIMULATEUR ===
NUM_SPLIT = 2
HIT_SOFT_17 = True

def log(action_stack, main_joueur, main_dealer, running_count):
    print("\n-------------------log-------------------")
    print(f"Main joueur: {main_joueur} | Main dealer: {main_dealer} | Actions: {action_stack} | Running count: {running_count}")
    print("-----------------------------------------\n")

def partie_BJ():
    running_count = 15
    sabot = utils_env.creer_sabot()

    tour_BJ(sabot, running_count)

def tour_BJ(sabot, running_count):
    print("nouveau tour")
    main_joueur = [8, 6]
    main_dealer = [9, 7]
    action_stack = []

    true_count = running_count / int(len(sabot)/52)

    log(action_stack, main_joueur, main_dealer, running_count)

    # on propose une assurance à l'IA
    if main_dealer[0] == 11:
        print("proposition d'assurance à l'IA")
        action_stack.append(IA_BJ(1, main_joueur, main_dealer, true_count))
        log(action_stack, main_joueur, main_dealer, running_count)

    # on regarde si le dealer a fait blackjack
    if utils_env.blackjack(main_dealer):
        print("blackjack dealer")
        log(action_stack, main_joueur, main_dealer, running_count)
        print("fin du tour")
        exit()
    
    # on propose un surrender à l'IA
    if IA_BJ(2, main_joueur, main_dealer, true_count):
        print("surrender pris par l'IA")
        action_stack.append("SU")
        log(action_stack, main_joueur, main_dealer, running_count)
        print("fin du tour")
        exit()

    # le dealer joue sa main
    main_dealer, running_count = jouer_main_dealer(main_dealer, running_count, sabot)

    print("main joué par le dealer")
    log(action_stack, main_joueur, main_dealer, running_count)

    # on joue la main
    jouer_main_joueur(action_stack, main_joueur, main_dealer, running_count, sabot)

    return 0

def jouer_main_dealer(main_dealer, running_count, sabot):
    while True:
        total = sum(main_dealer)
        soft = 11 in main_dealer and total <= 21
        if total > 21:
            break
        if total > 17 or (total == 17 and (not HIT_SOFT_17 or not soft)):
            break
        card = sabot.pop()
        main_dealer.append(card)
        running_count = utils_env.update_running_count(card, running_count)

    return main_dealer, running_count

def jouer_main_joueur(action_stack, main_joueur, main_dealer, running_count, sabot):
    print("nouvelle main joueur")
    true_count = running_count / int(len(sabot)/52)
    log(action_stack, main_joueur, main_dealer, running_count)

    if utils_env.valeur_main(main_joueur) > 21:
        print("bust joueur")
        log(action_stack, main_joueur, main_dealer, running_count)
        exit()


    # on propose un split à l'IA
    if utils_env.is_pair(main_joueur) and (action_stack.count('SP') < NUM_SPLIT):
        print("proposition de paire à l'IA")
        if IA_BJ(3, main_joueur, main_dealer, true_count):
            print("prise de split par l'IA")
            action_stack.append("SP")
            main_1, main_2 = utils_env.split_management(main_joueur, running_count, sabot)

            if main_joueur == [11, 11]:
                print("split sur As")
                log(action_stack, main_1, main_dealer, running_count)
                log(action_stack, main_2, main_dealer, running_count)
                exit()

            jouer_main_joueur(action_stack, main_1, main_dealer, running_count, sabot)
            jouer_main_joueur(action_stack, main_2, main_dealer, running_count, sabot)

    action = IA_BJ(4, main_joueur, main_dealer, true_count)


partie_BJ()