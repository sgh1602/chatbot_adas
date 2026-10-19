# -*- coding: utf-8 -*-
"""
Script 3: Test du chatbot ADAS avec Gemini (gratuit)
"""

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from google import genai
from google.genai import types

# Configuration Gemini - REMPLACE PAR TA CLÉ
GEMINI_API_KEY = "AQ.Ab8RN6LkMgrdOxuJcBPZftf7MztJqhL0rhS1_tSN9M-qS6s5zw"  # Mets ta clé qui commence par AQ.

def load_vectordb():
    """Charge la base vectorielle"""
    print("[+] Chargement de ChromaDB...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectordb = Chroma(
        persist_directory="../chroma_db",
        embedding_function=embeddings
    )
    
    print("[OK] Base vectorielle chargee")
    return vectordb

def ask_question(vectordb, question, api_key):
    """Pose une question au chatbot"""
    print(f"\n{'='*60}")
    print(f"[?] Question: {question}")
    print(f"{'='*60}")
    
    # Récupérer documents pertinents
    print("\n[>] Recherche dans la base...")
    docs = vectordb.similarity_search(question, k=3)
    
    # Préparer contexte
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Prompt pour Gemini
    prompt = f"""Tu es un assistant expert en systèmes ADAS (Advanced Driver Assistance Systems).

Réponds à la question suivante en te basant UNIQUEMENT sur le contexte fourni.
Si l'information n'est pas dans le contexte, dis "Je n'ai pas cette information dans ma base de données."

Contexte:
{context}

Question: {question}

Réponse:"""
    
    # Appel Gemini
    print("[>] Generation de la reponse...")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='models/gemini-3.8-flash',
        contents=prompt
    )
    
    print(f"\n[!] Reponse:")
    print(f"{'-'*60}")
    print(response.text)
    print(f"{'-'*60}")
    
    print(f"\n[#] Sources ({len(docs)} documents):")
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get('source', 'Unknown').split('\\')[-1]
        print(f"   {i}. {source}")
    
    return response.text

def main():
    # Vérifier clé API
    if GEMINI_API_KEY == "VOTRE_CLE_API_GEMINI":
        print("[X] ERREUR: Vous devez configurer votre cle API Gemini !")
        print("\n[i] Instructions:")
        print("   1. Allez sur: https://makersuite.google.com/app/apikey")
        print("   2. Creez une cle API gratuite")
        print("   3. Remplacez VOTRE_CLE_API_GEMINI a la ligne 12 de ce script")
        return
    
    print("\n" + "="*60)
    print("TEST DU CHATBOT ADAS")
    print("="*60)
    
    # Charger base
    vectordb = load_vectordb()
    
    # Questions de test
    questions = [
        "Comment fonctionne le freinage d'urgence automatique (AEB) ?",
        "Quels sont les capteurs utilises dans les systemes ADAS ?",
        "C'est quoi le sensor fusion ?"
    ]
    
    for question in questions:
        try:
            ask_question(vectordb, question, GEMINI_API_KEY)
            print("\n")
        except Exception as e:
            print(f"[X] Erreur: {str(e)}")
    
    print("="*60)
    print("[OK] Test termine !")
    print("="*60)

if __name__ == "__main__":
    main()
