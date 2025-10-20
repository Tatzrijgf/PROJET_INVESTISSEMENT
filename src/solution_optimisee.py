import pandas as pd

def solution_intelligente(df, budget_max):
    """
    Trouve le profit maximum avec le budget donné
    """
    # Convertir le budget en entier
    budget_max = int(budget_max)
    
    # Nos "enveloppes magiques"
    enveloppes = [0] * (budget_max + 1)
    achats = [[] for _ in range(budget_max + 1)]
    
    # Trier les actions par ratio profit/coût (meilleur d'abord)
    df_sorted = df.copy()
    df_sorted['ratio'] = df_sorted['profit_reel'] / df_sorted['cost']
    df_sorted = df_sorted.sort_values('ratio', ascending=False)
    
    # Parcourir chaque action
    for i in range(len(df_sorted)):
        action_id = df_sorted.iloc[i]['id']
        cout = int(df_sorted.iloc[i]['cost'])
        profit = df_sorted.iloc[i]['profit_reel']
        
        # Vérifier si l'action est trop chère
        if cout > budget_max:
            continue
            
        # Parcourir les budgets de haut en bas
        for budget in range(budget_max, cout - 1, -1):
            budget_reste = budget - cout
            nouveau_profit = enveloppes[budget_reste] + profit
            
            # Si c'est mieux, on met à jour
            if nouveau_profit > enveloppes[budget]:
                enveloppes[budget] = nouveau_profit
                achats[budget] = achats[budget_reste] + [action_id]
    
    return enveloppes[budget_max], achats[budget_max]

# Test rapide
if __name__ == "__main__":
    from utils import lire_donnees
    
    print("🧪 Test de la solution optimisée")
    
    # Test avec data_test.csv (plus simple)
    try:
        df = lire_donnees('../data/data_test.csv')
        profit, actions = solution_intelligente(df, 500000)
        
        print(f"\n🎯 RÉSULTAT :")
        print(f"Profit maximum : {profit:.2f} F CFA")
        print(f"Actions à acheter : {actions}")
    except Exception as e:
        print(f"❌ Erreur : {e}")