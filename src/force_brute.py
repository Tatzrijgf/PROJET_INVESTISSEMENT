import pandas as pd
import time
from itertools import combinations

def solution_force_brute(df, budget_max):
    """
    Solution par force brute - teste toutes les combinaisons possibles
    """
    print("💪 Début de la solution force brute...")
    
    meilleur_profit = 0
    meilleure_combinaison = []
    cout_total_meilleur = 0
    
    # Nombre total de combinaisons possibles (pour information)
    total_combinaisons = 2 ** len(df)
    print(f"📊 Nombre total de combinaisons à tester : {total_combinaisons:,}")
    
    # Si trop d'actions, on limite pour éviter le crash
    if len(df) > 25:
        print("⚠️  Trop d'actions pour la force brute (>25), utilisation limitée à 20 actions")
        df = df.head(20)
        total_combinaisons = 2 ** len(df)
        print(f"📊 Combinaisons après limitation : {total_combinaisons:,}")
    
    # Tester toutes les combinaisons possibles
    compteur = 0
    for taille in range(1, len(df) + 1):
        print(f"🔍 Test des combinaisons de {taille} actions...")
        
        for combinaison in combinations(df.iterrows(), taille):
            compteur += 1
            
            # Afficher la progression pour les gros calculs
            if compteur % 10000 == 0:
                print(f"📈 Progression : {compteur:,} / {total_combinaisons:,} combinaisons testées")
            
            cout_total = 0
            profit_total = 0
            actions_combinaison = []
            
            # Calculer le coût et profit de cette combinaison
            for index, action in combinaison:
                cout_total += action['cost']
                profit_total += action['profit_reel']
                actions_combinaison.append(action['id'])
            
            # Vérifier si c'est dans le budget et meilleur profit
            if cout_total <= budget_max and profit_total > meilleur_profit:
                meilleur_profit = profit_total
                meilleure_combinaison = actions_combinaison
                cout_total_meilleur = cout_total
    
    print(f"✅ Force brute terminée : {compteur:,} combinaisons testées")
    
    return meilleur_profit, meilleure_combinaison, cout_total_meilleur

def solution_force_brute_rapide(df, budget_max):
    """
    Version plus rapide de la force brute (pour petits datasets)
    """
    print("💪 Version rapide de la force brute...")
    
    meilleur_profit = 0
    meilleure_combinaison = []
    cout_total_meilleur = 0
    
    # Convertir le DataFrame en liste pour plus de rapidité
    actions_list = []
    for _, action in df.iterrows():
        actions_list.append({
            'id': action['id'],
            'cost': action['cost'],
            'profit': action['profit_reel']
        })
    
    # Tester toutes les combinaisons
    n = len(actions_list)
    total_combinaisons = 2 ** n
    
    print(f"📊 {n} actions → {total_combinaisons:,} combinaisons possibles")
    
    # Utiliser les bits pour représenter les combinaisons
    for i in range(1, total_combinaisons):
        cout_total = 0
        profit_total = 0
        actions_combinaison = []
        
        # Vérifier chaque bit pour voir quelles actions sont sélectionnées
        for j in range(n):
            if (i >> j) & 1:  # Si le j-ème bit est à 1
                action = actions_list[j]
                cout_total += action['cost']
                profit_total += action['profit']
                actions_combinaison.append(action['id'])
        
        # Vérifier le budget et le profit
        if cout_total <= budget_max and profit_total > meilleur_profit:
            meilleur_profit = profit_total
            meilleure_combinaison = actions_combinaison
            cout_total_meilleur = cout_total
    
    return meilleur_profit, meilleure_combinaison, cout_total_meilleur

# Test de la force brute
if __name__ == "__main__":
    from utils import lire_donnees
    
    print("🧪 Test de la force brute")
    
    # Test avec data_test.csv
    try:
        df = lire_donnees('../data/data_test.csv')
        
        # Limiter à 15 actions max pour la démo
        if len(df) > 15:
            df = df.head(15)
            print(f"🔧 Limité à 15 actions pour le test")
        
        debut = time.time()
        profit, actions, cout = solution_force_brute_rapide(df, 500000)
        fin = time.time()
        
        print(f"\n🎯 RÉSULTAT FORCE BRUTE :")
        print(f"Profit : {profit:.2f} F CFA")
        print(f"Coût total : {cout:,} F CFA")
        print(f"Actions : {actions}")
        print(f"⏱️  Temps : {fin - debut:.2f} secondes")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()