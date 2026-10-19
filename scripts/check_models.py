# -*- coding: utf-8 -*-
"""
Script pour lister les modèles Gemini disponibles avec ta clé
"""

from google import genai

GEMINI_API_KEY = "AQ.Ab8RN6LkMgrdOxuJcBPZftf7MztJqhL0rhS1_tSN9M-qS6s5zw"

print("[+] Test de connexion a l'API Gemini...")
print(f"[i] Cle API: {GEMINI_API_KEY[:10]}...")

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    print("\n[>] Liste des modeles disponibles:")
    print("-" * 60)
    
    models = client.models.list()
    
    for model in models:
        print(f"  - {model.name}")
        if hasattr(model, 'display_name'):
            print(f"    Display: {model.display_name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"    Methods: {model.supported_generation_methods}")
        print()
    
    print("-" * 60)
    print(f"[OK] {len(list(models))} modele(s) trouve(s)")
    
except Exception as e:
    print(f"\n[X] ERREUR: {str(e)}")
    print("\n[i] Details de l'erreur:")
    import traceback
    traceback.print_exc()
