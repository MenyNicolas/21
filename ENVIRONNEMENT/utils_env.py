import random
import numpy as np
import pandas as pd

# === CONFIGURATION SIMULATEUR ===
NUM_DECKS = 6

def creer_sabot(num_decks=NUM_DECKS):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4 * num_decks
    random.shuffle(deck)
    return deck

def update_running_count(card, count):
    if card in [2, 3, 4, 5, 6]:
        return count + 1
    elif card in [10, 11]:
        return count - 1
    else:
        return count
    
def distribution_initial(deck, running_count):
    player = []
    dealer = []
    for _ in range(2):
        for hand in [player, dealer]:
            card = deck.pop()
            hand.append(card)
            running_count = update_running_count(card, running_count)
    return player, dealer, running_count

def blackjack(main):
    return len(main) == 2 and sorted(main) == [10, 11]

def is_pair(main_joueur):
    return (main_joueur[0] == main_joueur[1]) and (len(main_joueur) == 2)

def split_management(main_joueur, running_count, sabot):
    carte1 = sabot.pop()
    carte2 = sabot.pop()

    main_1 = [main_joueur[0], carte1]
    main_2 = [main_joueur[0], carte2]

    running_count = update_running_count(carte1, running_count)
    running_count = update_running_count(carte2, running_count)

    return main_1, main_2, running_count, sabot

def hit_double_management(main_joueur, running_count, sabot):
    carte = sabot.pop()
    main_joueur.append(carte)
    running_count = update_running_count(carte, running_count)

    return main_joueur, running_count, sabot

def valeur_main(main_joueur):
    total = 0
    ace_count = 0

    for card in main_joueur:
        if card == 11:
            ace_count += 1
        total += card

    # Ajustement des As (11 → 1) si nécessaire
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1

    return total

def resultat(main_dealer, main_joueur, is_doubled):
    mise = 1
    if is_doubled: mise *= 2

    if valeur_main(main_joueur) > 21: return -mise
    elif valeur_main(main_dealer) > 21: return mise
    elif blackjack(main_joueur):
        if blackjack(main_dealer): return 0
        else: return 1.5*mise
    elif valeur_main(main_joueur) > valeur_main(main_dealer): return mise
    elif valeur_main(main_joueur) == valeur_main(main_dealer): return 0
    else: return -1

def fin_de_tour(main_dealer, main_joueur, action_stack, running_count, sabot, historique_df):
    is_doubled = False
    if(len(action_stack) > 0): is_doubled = action_stack[-1] == 'D'

    true_count = int(running_count / (len(sabot) / 52))
    resultat_main = resultat(main_dealer, main_joueur, is_doubled)

    total_joueur = valeur_main(main_joueur)
    total_dealer = valeur_main(main_dealer)

    # Création de la série de suivi
    series_resultat = pd.Series({
        'main_joueur': main_joueur,
        'main_dealer': main_dealer,
        'actions': action_stack,
        'total_joueur': total_joueur,
        'total_dealer': total_dealer,
        'running_count': running_count,
        'true_count': true_count,
        'résultat': resultat_main,
        'is_doubled': is_doubled
    })

    return pd.concat([historique_df, series_resultat.to_frame().T], ignore_index=True)