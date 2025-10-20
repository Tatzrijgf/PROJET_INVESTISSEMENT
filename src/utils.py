import pandas as pd
import re

def lire_donnees(fichier):
    """
    Lit les données depuis un fichier CSV et les standardise
    """
    print(f"📊 Fichier : {fichier}")
    
    # Essayer différents séparateurs
    try:
        # Essayer d'abord avec point-virgule
        df = pd.read_csv(fichier, sep=';')
        print("✅ Séparateur : point-virgule (;)")
    except:
        try:
            # Essayer avec tabulation
            df = pd.read_csv(fichier, sep='\t')
            print("✅ Séparateur : tabulation (\\t)")
        except:
            # Essayer avec virgule
            df = pd.read_csv(fichier, sep=',')
            print("✅ Séparateur : virgule (,)")
    
    print(f"Colonnes originales : {list(df.columns)}")
    print(f"Nombre d'actions : {len(df)}")
    
    # Nettoyer les noms de colonnes (supprimer espaces et tabulations)
    df.columns = [col.strip() for col in df.columns]
    
    # Standardiser les noms de colonnes selon le type de fichier
    if 'name' in df.columns and 'price' in df.columns:
        # Format dataset1/dataset2
        df = df.rename(columns={'name': 'id', 'price': 'cost'})
        print("✅ Format : dataset1/dataset2")
        
    elif 'Actions' in df.columns and 'Cout par action (en euros)' in df.columns:
        # Format data_test
        df = df.rename(columns={
            'Actions': 'id', 
            'Cout par action (en euros)': 'cost',
            'Bénéfice après 2 ans': 'profit_pct'
        })
        print("✅ Format : data_test")
    else:
        # Si une seule colonne, essayer de la diviser
        if len(df.columns) == 1:
            print("⚠️  Une seule colonne détectée, tentative de division...")
            colonne_unique = df.columns[0]
            
            # Essayer de diviser par tabulation
            if '\t' in colonne_unique:
                nouvelles_colonnes = ['id', 'cost', 'profit_pct']
                df_split = df[colonne_unique].str.split('\t', expand=True)
                df_split.columns = nouvelles_colonnes
                df = df_split
                print("✅ Division par tabulation réussie")
    
    # Nettoyer les données
    df = nettoyer_donnees(df)
    
    # Calculer le profit réel
    df['profit_reel'] = df['cost'] * df['profit_pct'] / 100
    
    print(f"📈 Aperçu après nettoyage :")
    print(df[['id', 'cost', 'profit_pct', 'profit_reel']].head())
    
    return df

def nettoyer_donnees(df):
    """
    Nettoie les données : supprime les actions avec coût <= 0
    et convertit les pourcentages
    """
    # Convertir cost en numérique (gérer les erreurs)
    df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
    
    # Supprimer les lignes avec coût manquant, négatif ou nul
    df_clean = df[df['cost'] > 0].copy()
    
    # Convertir profit_pct si nécessaire (pour data_test avec '%')
    if df_clean['profit_pct'].dtype == 'object':
        df_clean['profit_pct'] = df_clean['profit_pct'].str.replace('%', '').str.replace(',', '.').astype(float)
    else:
        df_clean['profit_pct'] = df_clean['profit_pct'].astype(float)
    
    print(f"🗑️  {len(df) - len(df_clean)} actions supprimées (coût <= 0 ou invalide)")
    print(f"📋 {len(df_clean)} actions valides restantes")
    
    return df_clean