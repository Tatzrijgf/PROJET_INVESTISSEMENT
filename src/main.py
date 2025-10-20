import pandas as pd
import time
import os
from solution_optimisee import solution_intelligente
from force_brute import solution_force_brute_rapide
from utils import lire_donnees

def afficher_resultats(profit, actions, df, temps_execution, budget_max, methode):
    """
    Affiche joliment les résultats
    """
    print("\n" + "="*60)
    print(f"🎯 RÉSULTATS {methode}")
    print("="*60)
    
    print(f"💰 Profit total : {profit:,.2f} F CFA")
    print(f"⏱️  Temps d'exécution : {temps_execution:.4f} secondes")
    
    cout_total = 0
    profit_total = 0
    
    print(f"\n🛒 {len(actions)} actions à acheter :")
    print("-" * 40)
    
    for action_id in actions:
        # Trouver les infos de l'action
        action_data = df[df['id'] == action_id].iloc[0]
        cout = action_data['cost']
        profit_action = action_data['profit_reel']
        cout_total += cout
        profit_total += profit_action
        
        print(f"• {action_id}")
        print(f"  Coût : {cout:,} F CFA")
        print(f"  Profit : {profit_action:,.2f} F CFA")
        print(f"  Ratio : {(profit_action/cout*100):.1f}%")
        print()
    
    print(f"📊 RÉSUMÉ :")
    print(f"Total dépensé : {cout_total:,} F CFA / {budget_max:,} F CFA")
    print(f"Budget restant : {budget_max - cout_total:,} F CFA")
    print(f"Profit total : {profit_total:,.2f} F CFA")
    print(f"Rentabilité globale : {(profit_total/cout_total*100):.1f}%")

def comparer_solutions(df, budget_max):
    """
    Compare la solution optimisée et la force brute
    """
    print("\n" + "="*70)
    print("🔍 COMPARAISON DES SOLUTIONS")
    print("="*70)
    
    # Solution optimisée
    print("\n🚀 Solution optimisée (Programmation Dynamique)")
    print("-" * 50)
    debut_opti = time.time()
    profit_opti, actions_opti = solution_intelligente(df, budget_max)
    fin_opti = time.time()
    temps_opti = fin_opti - debut_opti
    
    afficher_resultats(profit_opti, actions_opti, df, temps_opti, budget_max, "SOLUTION OPTIMISÉE")
    
    # Solution force brute (seulement pour petits datasets)
    if len(df) <= 20:
        print("\n💪 Solution Force Brute")
        print("-" * 50)
        debut_brute = time.time()
        profit_brute, actions_brute, cout_brute = solution_force_brute_rapide(df, budget_max)
        fin_brute = time.time()
        temps_brute = fin_brute - debut_brute
        
        afficher_resultats(profit_brute, actions_brute, df, temps_brute, budget_max, "FORCE BRUTE")
        
        # Comparaison
        print("\n📊 COMPARAISON DÉTAILLÉE")
        print("-" * 30)
        print(f"Profit optimisé : {profit_opti:,.2f} F CFA")
        print(f"Profit force brute : {profit_brute:,.2f} F CFA")
        print(f"Différence : {profit_opti - profit_brute:,.2f} F CFA")
        print(f"Temps optimisé : {temps_opti:.4f} secondes")
        print(f"Temps force brute : {temps_brute:.4f} secondes")
        print(f"Accélération : {temps_brute/temps_opti:.1f}x plus rapide")
        
        # Vérification
        if abs(profit_opti - profit_brute) < 0.01:
            print("✅ Les deux solutions donnent le MÊME résultat !")
        else:
            print("❌ Les solutions donnent des résultats DIFFÉRENTS !")
    
    else:
        print(f"\n⚠️  Force brute non exécutée : {len(df)} actions > 20 (trop long)")

def main():
    print("🚀 PROGRAMME D'OPTIMISATION D'INVESTISSEMENT")
    print("=" * 50)
    
    # Liste des fichiers disponibles
    fichiers = {
        '1': '../data/data_test.csv',
        '2': '../data/dataset1_Python+P3.csv', 
        '3': '../data/dataset2_Python+P3.csv'
    }
    
    print("\n📁 Fichiers disponibles :")
    print("1. data_test.csv (petit test - idéal pour force brute)")
    print("2. dataset1_Python+P3.csv") 
    print("3. dataset2_Python+P3.csv")
    
    choix = input("\n👉 Choisis un fichier (1, 2 ou 3) : ")
    
    if choix not in fichiers:
        print("❌ Choix invalide")
        return
    
    fichier = fichiers[choix]
    budget_max = 500000
    
    try:
        # Charger les données
        print(f"\n📁 Chargement de {fichier}...")
        df = lire_donnees(fichier)
        
        if len(df) == 0:
            print("❌ Aucune action valide après nettoyage")
            return
        
        # Pour la force brute, on peut limiter le nombre d'actions
        if len(df) > 20 and choix == '1':
            utiliser_tout = input(f"🔧 {len(df)} actions détectées. Limiter à 20 pour la force brute ? (o/n) : ")
            if utiliser_tout.lower() == 'o':
                df = df.head(20)
                print("✅ Limité à 20 actions")
        
        # Lancer la comparaison
        comparer_solutions(df, budget_max)
        
    except FileNotFoundError:
        print(f"❌ Erreur : Fichier {fichier} non trouvé")
        print("💡 Vérifie que le fichier existe dans le dossier data/")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()