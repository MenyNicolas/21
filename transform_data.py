import pandas as pd

# Supposons que df est votre DataFrame
# Conversion des colonnes en listes
main_joueur_list = df['main_joueur'].tolist()
main_dealer_list = df['main_dealer'].tolist()
actions_list = df['actions'].tolist()

# Affichage des résultats
print("Main joueur:", main_joueur_list)
print("\nMain dealer:", main_dealer_list)
print("\nActions:", actions_list) 