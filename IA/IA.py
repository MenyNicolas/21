import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
import random

import IA.utils_ia as utils_ia

def IA_BJ(id_action, action_stack, main_joueur, main_dealer, running_count, sabot):

    true_count = int(running_count / (len(sabot) / 52))

    # gestion de l'assurance
    if(id_action == 1):
        if true_count > 2:
            return 'A'
        else:
            return 'N'
        
    # gestion du surrender
    if(id_action == 2):
        return utils_ia.surrender(main_joueur, main_dealer, true_count)
    
    # gestion des splits
    if(id_action == 3):
        return utils_ia.model_split(main_joueur, main_dealer, true_count)
    
    # gestion stand hit double
    if(id_action == 4):
        double_possible = len(main_joueur) == 2
        return random.choice(['H', 'S', 'D'])
    
    return 0