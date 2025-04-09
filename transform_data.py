import numpy as np
import pandas as pd

df = pd.read_csv('historique_df.csv')

df['main_joueur'] = df['main_joueur'].apply(eval)
df['main_dealer'] = df['main_dealer'].apply(eval)
df['actions'] = df['actions'].apply(eval)

df['total_joueur_calcule'] = df['main_joueur'].apply(sum)
df['total_dealer_calcule'] = df['main_dealer'].apply(sum)

def carte_tour(row):
    main_joueur = row['main_joueur']
    main_dealer = row['main_dealer']
    nb_carte = len(main_joueur) + len(main_dealer)
    
    return nb_carte

def hi_lo_count(row):
    main_joueur = row['main_joueur']
    main_dealer = row['main_dealer']

    count = 0

    for carte in (main_joueur + main_dealer):
        if(carte in [2, 3, 4, 5, 6]):
            count += 1
        elif(carte in [10, 11]):
            count -= 1
    
    return count

df["carte_tour"] = df.apply(carte_tour, axis=1)
df["hi_lo_count"] = df.apply(hi_lo_count, axis=1)

df['carte_tour_cumul'] = df['carte_tour'].cumsum()
df['hi_lo_count_cumul'] = df['hi_lo_count'].cumsum()

df['true_count_calculated'] = (
    df['hi_lo_count_cumul'] / ((312 - df['carte_tour_cumul']) / 52)
)

# Remplace les valeurs infinies ou NaN par 0 (ou autre valeur logique)
df['true_count_calculated'] = df['true_count_calculated'].replace([np.inf, -np.inf], np.nan)
df['true_count_calculated'] = df['true_count_calculated'].fillna(0).astype(int)


# Création des nouvelles colonnes pour main_joueur
for i in range(1, 7):
    df[f'main_joueur_{i}'] = df['main_joueur'].apply(lambda x: x[i-1] if len(x) >= i else None)

# Création des nouvelles colonnes pour main_dealer
for i in range(1, 7):
    df[f'main_dealer_{i}'] = df['main_dealer'].apply(lambda x: x[i-1] if len(x) >= i else None)

# Création des nouvelles colonnes pour actions
for i in range(1, 7):
    df[f'actions_{i}'] = df['actions'].apply(lambda x: x[i-1] if len(x) >= i else None)

# Conversion des colonnes main_joueur en int
for i in range(1, 7):
    df[f'main_joueur_{i}'] = df[f'main_joueur_{i}'].astype('Int64')  # Int64 permet de gérer les valeurs None

# Conversion des colonnes main_dealer en int
for i in range(1, 7):
    df[f'main_dealer_{i}'] = df[f'main_dealer_{i}'].astype('Int64')

df.to_excel('historique_df_transforme.xlsx', index=False)