import random
import numpy as np
import pandas as pd

# === CONFIGURATION SIMULATEUR ===
NUM_DECKS = 6

def creer_sabot(num_decks=NUM_DECKS):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 11] * 4 * num_decks
    random.shuffle(deck)
    return deck


def update_running_count(card, count):
    if card in [2, 3, 4, 5, 6]:
        return count + 1
    elif card in [10, 'J', 'Q', 'K', 11]:
        return count - 1
    else:
        return count

'''
def distribution_initial_pair(deck, running_count):
    dealer = []

    # Trouver une paire pour le joueur
    for i in range(len(deck)):
        for j in range(i + 1, len(deck)):
            if deck[i] == deck[j]:
                player_card = deck[i]
                player = [player_card, player_card]
                deck.pop(j)
                deck.pop(i)
                running_count = update_running_count(player_card, running_count)
                running_count = update_running_count(player_card, running_count)
                break
        else:
            continue
        break
    else:
        raise ValueError("Aucune paire disponible dans le deck.")

    for _ in range(2):
        card = deck.pop()
        dealer.append(card)
        running_count = update_running_count(card, running_count)

    return player.copy(), dealer.copy(), running_count
'''

def distribution_initial(deck, running_count):
    player = []
    dealer = []
    for _ in range(2):
        for hand in [player, dealer]:
            card = deck.pop()
            hand.append(card)
            running_count = update_running_count(card, running_count)
    return player.copy(), dealer.copy(), running_count

def blackjack(main):
    return len(main) == 2 and valeur_main(main) == 21

def is_pair(main_joueur):
    return len(main_joueur) == 2 and main_joueur[0] == main_joueur[1]

def split_management(main_joueur, running_count, sabot):
    carte1 = sabot.pop()
    carte2 = sabot.pop()

    # print(f"SPLIT >> Carte1 : {carte1}, Carte2 : {carte2}, taille sabot : {len(sabot)}")

    main_1 = [main_joueur[0], carte1]
    main_2 = [main_joueur[1], carte2]

    running_count = update_running_count(carte1, running_count)
    running_count = update_running_count(carte2, running_count)

    return main_1.copy(), main_2.copy(), running_count, sabot

def hit_double_management(main_joueur, running_count, sabot):
    carte = sabot.pop()
    main_joueur.append(carte)
    running_count = update_running_count(carte, running_count)

    return main_joueur.copy(), running_count, sabot

def valeur_carte(carte):
    return 10 if carte in ['J', 'Q', 'K'] else carte

def valeur_main(main_joueur):
    total = 0
    ace_count = 0

    for card in main_joueur:
        v = valeur_carte(card)
        if v == 11:
            ace_count += 1
        total += v

    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1

    return total



def resultat(main_dealer, main_joueur, is_doubled):
    mise = 2 if is_doubled else 1

    if valeur_main(main_joueur) > 21:
        return -mise
    elif valeur_main(main_dealer) > 21:
        return mise
    elif blackjack(main_joueur):
        return 0 if blackjack(main_dealer) else 1.5 * mise
    elif valeur_main(main_joueur) > valeur_main(main_dealer):
        return mise
    elif valeur_main(main_joueur) == valeur_main(main_dealer):
        return 0
    else:
        return -mise

def fin_de_tour(main_dealer, main_joueur, action_stack, running_count, sabot, historique_df):
    is_doubled = action_stack[-1] == 'D' if action_stack else False

    true_count = int(running_count / (len(sabot) / 52)) if len(sabot) > 0 else 0
    resultat_main = resultat(main_dealer, main_joueur, is_doubled)

    total_joueur = valeur_main(main_joueur)
    total_dealer = valeur_main(main_dealer)

    series_resultat = pd.Series({
        'main_joueur': main_joueur.copy(),
        'main_dealer': main_dealer.copy(),
        'actions': action_stack.copy(),
        'total_joueur': total_joueur,
        'total_dealer': total_dealer,
        'running_count': running_count,
        'true_count': true_count,
        'résultat': resultat_main,
        'is_doubled': is_doubled
    })

    return pd.concat([historique_df, series_resultat.to_frame().T], ignore_index=True)