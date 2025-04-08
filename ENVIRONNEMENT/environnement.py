import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
import ENVIRONNEMENT.utils_env as utils_env

from IA.IA import IA_BJ

def log(action_stack, main_joueur, main_dealer, running_count):
    print("\n-------------------log-------------------")
    print(f"Main joueur: {main_joueur} | Main dealer: {main_dealer} | Actions: {action_stack} | Running count: {running_count}")
    print("-----------------------------------------\n")

def partie_BJ():
    running_count = 0
    sabot = utils_env.creer_sabot()

    tour_BJ(sabot, running_count)

def tour_BJ(sabot, running_count):
    main_joueur = [8, 8]
    main_dealer = [9, 7]
    action_stack = []

    # on regarde si le dealer a fait blackjack
    if utils_env.blackjack(main_dealer):
        print(utils_env.end_of_hand(main_dealer, main_joueur, action_stack, running_count, sabot))
        exit()

    # on joue les mains dealers et joueurs
    main_dealer, running_count, sabot = jouer_main_dealer(main_dealer, running_count, sabot)
    sabot, running_count, sabot = jouer_main_joueur(action_stack, main_joueur, main_dealer, running_count, sabot, False)

    print('oklm')

    return 0

def jouer_main_dealer(main_dealer, running_count, sabot):
    while True:
        total = sum(main_dealer)
        soft = 11 in main_dealer and total <= 21
        if total > 21:
            break
        card = sabot.pop()
        main_dealer.append(card)
        running_count = utils_env.update_running_count(card, running_count)

    return main_dealer, running_count, sabot

def jouer_main_joueur(action_stack, main_joueur, main_dealer, running_count, sabot, split_security):

    #log(action_stack, main_joueur, main_dealer, running_count)

    if utils_env.valeur_main(main_joueur) > 21:
        print(utils_env.end_of_hand(main_dealer, main_joueur, action_stack, running_count, sabot))
        if not split_security: exit()

    # on propose un split à l'IA
    if utils_env.is_pair(main_joueur):
        if IA_BJ(3, action_stack, main_joueur, main_dealer, running_count, sabot):
            action_stack.append("SP")
            main_1, main_2, running_count, sabot = utils_env.split_management(main_joueur, running_count, sabot)

            if main_joueur == [11, 11]:
                print(utils_env.end_of_hand(main_dealer, main_1, action_stack, running_count, sabot))
                print(utils_env.end_of_hand(main_dealer, main_2, action_stack, running_count, sabot))
                if not split_security: exit()

            sabot, running_count, sabot = jouer_main_joueur(action_stack.copy(), main_1.copy(), main_dealer, running_count, sabot, True)
            sabot, running_count, sabot = jouer_main_joueur(action_stack.copy(), main_2.copy(), main_dealer, running_count, sabot, False)

    action = IA_BJ(4, action_stack, main_joueur, main_dealer, running_count, sabot)

    if action == 'H':
        action_stack.append('H')
        main_joueur, running_count, sabot = utils_env.hit_management(main_joueur, running_count, sabot)
        sabot, running_count, sabot = jouer_main_joueur(action_stack, main_joueur, main_dealer, running_count, sabot, split_security)
    if action == 'S':
        action_stack.append('S')
        print(utils_env.end_of_hand(main_dealer, main_joueur, action_stack, running_count, sabot))
        if not split_security: exit()
    if action == 'D':
        action_stack.append('D')
        main_joueur, running_count, sabot = utils_env.double_management(main_joueur, running_count, sabot)
        print(utils_env.end_of_hand(main_dealer, main_joueur, action_stack, running_count, sabot))
        if not split_security: exit()

    return main_joueur, running_count, sabot

partie_BJ()