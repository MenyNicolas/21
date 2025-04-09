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

    historique_df = pd.DataFrame(columns=[
    'main_joueur',
    'main_dealer',
    'actions',
    'total_joueur',
    'total_dealer',
    'running_count',
    'true_count',
    'résultat',
    'is_doubled'
    ])

    while(len(sabot) > (utils_env.NUM_DECKS * 52 * 0.25)):
        main_joueur, main_dealer, action_stack, running_count, sabot = tour_BJ(sabot, running_count, historique_df)
        historique_df = utils_env.fin_de_tour(main_dealer, main_joueur, action_stack, running_count, sabot, historique_df)
    
    historique_df.to_csv('historique_df.csv', index=False)

def tour_BJ(sabot, running_count, historique_df):
    main_joueur, main_dealer, running_count = utils_env.distribution_initial(sabot, running_count)
    action_stack = []

    # on regarde si le dealer a fait blackjack
    if utils_env.blackjack(main_dealer):
        return main_joueur, main_dealer, action_stack, running_count, sabot

    # on joue les mains dealers et joueurs
    main_joueur, running_count, sabot = jouer_main_joueur(action_stack, main_joueur, main_dealer, running_count, sabot)
    main_dealer, running_count, sabot = jouer_main_dealer(main_dealer, running_count, sabot)
    
    return main_joueur, main_dealer, action_stack, running_count, sabot

def jouer_main_dealer(main_dealer, running_count, sabot):
    while True:
        # Calcul du total + détection soft/hard
        total = utils_env.valeur_main(main_dealer)

        # Stand sur 17 ou plus
        if total >= 17:
            break

        # Tirer une carte
        card = sabot.pop()
        main_dealer.append(card)
        running_count = utils_env.update_running_count(card, running_count)

    return main_dealer, running_count, sabot

def jouer_main_joueur(action_stack, main_joueur, main_dealer, running_count, sabot):

    if utils_env.valeur_main(main_joueur) > 21:
        return main_joueur, running_count, sabot
        # historique_df = utils_env.end_of_hand(main_dealer, main_joueur, action_stack, running_count, sabot, historique_df)

    # on propose un split à l'IA
    '''
    if utils_env.is_pair(main_joueur):
        if IA_BJ(3, action_stack, main_joueur, main_dealer, running_count, sabot):
            action_stack.append("SP")
            main_1, main_2, running_count, sabot = utils_env.split_management(main_joueur, running_count, sabot)

            if main_joueur == [11, 11]:
                historique_df = utils_env.end_of_hand(main_dealer, main_1, action_stack, running_count, sabot, historique_df)
                historique_df = utils_env.end_of_hand(main_dealer, main_2, action_stack, running_count, sabot, historique_df)

            sabot, running_count, sabot = jouer_main_joueur(action_stack.copy(), main_1.copy(), main_dealer, running_count, sabot, historique_df, True)
            sabot, running_count, sabot = jouer_main_joueur(action_stack.copy(), main_2.copy(), main_dealer, running_count, sabot, historique_df, False)
    '''

    action = IA_BJ(4, action_stack, main_joueur, main_dealer, running_count, sabot)

    if action == 'H':
        action_stack.append('H')
        main_joueur, running_count, sabot = utils_env.hit_double_management(main_joueur, running_count, sabot)
        main_joueur, running_count, sabot = jouer_main_joueur(action_stack, main_joueur, main_dealer, running_count, sabot)
    if action == 'S':
        action_stack.append('S')
        # historique_df = utils_env.end_of_hand(main_dealer, main_joueur, action_stack, running_count, sabot, historique_df)
    if action == 'D':
        action_stack.append('D')
        main_joueur, running_count, sabot = utils_env.hit_double_management(main_joueur, running_count, sabot)
        # historique_df = utils_env.end_of_hand(main_dealer, main_joueur, action_stack, running_count, sabot, historique_df)

    return main_joueur, running_count, sabot

partie_BJ()