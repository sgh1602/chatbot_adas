# -*- coding: utf-8 -*-
"""
Interface Streamlit pour le chatbot ADAS
"""

import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq
import time

# Configuration de la page
st.set_page_config(
    page_title="Chatbot ADAS",
    page_icon="🚗",
    layout="wide"
)

# Titre
st.title("🚗 Chatbot ADAS - Assistant Intelligent")
st.markdown("Posez vos questions sur les systemes ADAS (Advanced Driver Assistance Systems)")

# Configuration Groq dans la sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    # Cle API Groq en dur (cachee)
    groq_api_key = "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"
    
    st.markdown("---")
    st.markdown("### 📚 Base de donnees")
    st.info("11 documents PDF charges\n3560 chunks indexes")
    
    st.markdown("---")
    st.markdown("### ℹ️ A propos")
    st.markdown("""
    - **RAG**
    - **ChromaDB**
    - **Groq + GPT-OSS-120B**
    - **Sentence Transformers**
    """)

# Charger la base vectorielle (cache)
@st.cache_resource
def load_vectordb():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    return vectordb

# Fonction de reponse avec GROQ (ultra-rapide)
def ask_chatbot(question, vectordb, api_key):
    import time
    
    # MESURE 1: Recherche vectorielle
    t_start_search = time.time()
    docs = vectordb.max_marginal_relevance_search(question, k=8, fetch_k=20)
    t_search = time.time() - t_start_search
    
    # Contexte court
    context = "\n\n".join([doc.page_content[:500] for doc in docs])
    
    # Prompt STRICT pour éviter les hallucinations
    prompt = f"""Tu es un expert en systemes ADAS. Reponds UNIQUEMENT avec les informations du contexte fourni.

REGLES STRICTES:
- N'ajoute AUCUN chiffre, duree ou detail qui n'est pas dans le contexte
- Si l'info n'est pas dans le contexte, dis "Cette information n'est pas precisee dans ma base"
- Maximum 2-3 phrases
- Si la question contient une abreviation (ADAS, SAE, ACC...), donne sa signification puis explique

Contexte:
{context}

Question: {question}

Reponse (basee UNIQUEMENT sur le contexte):"""
    
    # Client Groq
    client = Groq(api_key=api_key)
    
    # MESURE 2: Appel API Groq
    t_start_api = time.time()
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "Tu es un expert ADAS. Reponds UNIQUEMENT avec le contexte fourni. N'invente RIEN."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,  # Temperature a 0 pour eviter les hallucinations
            max_tokens=300
        )
        
        t_api = time.time() - t_start_api
        
        answer = response.choices[0].message.content
        
        # LOGS de debug
        print(f"[DEBUG] Temps recherche: {t_search:.2f}s | Temps API Groq: {t_api:.2f}s | Total: {t_search+t_api:.2f}s")
        
        return answer, docs, {"search_time": t_search, "api_time": t_api, "model": "gpt-oss-120b"}
        
    except Exception as e:
        raise Exception(f"Erreur Groq: {str(e)}")

# Zone principale
# Groq API key deja configuree
# Charger la base
with st.spinner("Chargement de la base vectorielle..."):
    vectordb = load_vectordb()

# Zone de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Empecher les soumissions multiples
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.write(f"{i}. {source}")

# Input utilisateur - desactive pendant le traitement
if prompt := st.chat_input("Posez votre question sur les systemes ADAS...", disabled=st.session_state.is_processing):
    # Marquer comme en cours de traitement
    st.session_state.is_processing = True
    
    # Ajouter message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generer reponse
    with st.chat_message("assistant"):
        with st.spinner("⚡ Recherche..."):
            try:
                answer, docs, timings = ask_chatbot(prompt, vectordb, groq_api_key)
                st.markdown(answer)
                
                # Sources
                sources = [doc.metadata.get('source', 'Unknown').split('\\')[-1] for doc in docs]
                with st.expander("📚 Sources"):
                    for i, source in enumerate(sources, 1):
                        st.write(f"{i}. {source}")
                
                # AFFICHAGE DES TEMPS (debug)
                with st.expander("⏱️ Performances"):
                    st.write(f"🔍 Recherche: {timings['search_time']:.2f}s")
                    st.write(f"🤖 API ({timings['model']}): {timings['api_time']:.2f}s")
                    st.write(f"⏱️ Total: {timings['search_time'] + timings['api_time']:.2f}s")
                
                # Sauvegarder dans l'historique
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                
            except Exception as e:
                error_msg = str(e)
                if "momentanement indisponible" in error_msg or "surcharges" in error_msg:
                    st.error(f"⚠️ {error_msg}")
                else:
                    st.error(f"❌ Erreur: {error_msg}")
            
            finally:
                # Debloquer pour la prochaine question
                st.session_state.is_processing = False
                st.rerun()

# Bouton pour effacer l'historique
if st.session_state.messages:
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("**Projet:** Chatbot Intelligent d'Assistance a la Comprehension des Systemes ADAS")
