# 🚗 Chatbot ADAS - Assistant Intelligent

Chatbot intelligent pour la compréhension des systèmes ADAS (Advanced Driver Assistance Systems) basé sur RAG (Retrieval Augmented Generation).

## 📋 Fonctionnalités

- ✅ Réponses basées sur 9 documents techniques ADAS
- ✅ RAG avec ChromaDB et embeddings sentence-transformers
- ✅ LLM Gemini (Google, gratuit)
- ✅ Interface web Streamlit
- ✅ Sources citées pour chaque réponse

## 🚀 Installation

### 1. Activer l'environnement virtuel

```bash
cd chatbot_adas
.\venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install langchain langchain-community chromadb sentence-transformers PyPDF2 streamlit google-generativeai
```

### 3. Obtenir une clé API Gemini (gratuit)

1. Allez sur: https://makersuite.google.com/app/apikey
2. Créez une clé API gratuite
3. Copiez la clé

## 📊 Utilisation

### Étape 1: Créer la base vectorielle

```bash
cd scripts
python 2_create_vectordb.py
```

⏱️ Durée: 2-5 minutes (première fois seulement)

### Étape 2: Tester le chatbot

```bash
python 3_test_chatbot.py
```

⚠️ N'oubliez pas de remplacer `VOTRE_CLE_API_GEMINI` dans le script !

### Étape 3: Lancer l'interface web

```bash
cd ..
streamlit run app.py
```

🌐 L'interface s'ouvrira dans votre navigateur

## 📚 Base de connaissances

9 documents ADAS couvrant:
- Capteurs (Radar, LiDAR, Caméra)
- Systèmes (AEB, FCW, ESC)
- Méthodologies de développement
- Standards et tests
- Sécurité et performance

## 💡 Exemples de questions

- Comment fonctionne le freinage d'urgence automatique (AEB) ?
- Quels sont les capteurs utilisés dans les systèmes ADAS ?
- C'est quoi le sensor fusion ?
- Comment tester un capteur radar ADAS ?
- Quelle est l'architecture d'un système ADAS ?

## 🛠️ Technologies

- **LLM**: Gemini Pro (Google)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **Interface**: Streamlit

## 📁 Structure du projet

```
chatbot_adas/
├── data/
│   └── pdfs/          # 9 documents ADAS
├── scripts/
│   ├── 1_prepare_data.py
│   ├── 2_create_vectordb.py
│   └── 3_test_chatbot.py
├── chroma_db/         # Base vectorielle (créée automatiquement)
├── app.py             # Interface Streamlit
├── venv/              # Environnement virtuel
└── README.md
```

## ⚡ Performance

- **Temps de réponse**: 3-5 secondes
- **Précision attendue**: 80-85%
- **Couverture**: 70% des sujets ADAS

## 🔧 Dépannage

### Erreur "API key invalid"
→ Vérifiez que votre clé Gemini est correcte

### Erreur "ChromaDB not found"
→ Lancez d'abord `2_create_vectordb.py`

### Installation lente
→ C'est normal pour la première installation (téléchargement des modèles)

## 📝 Auteur

Projet de stage - Développement d'un chatbot intelligent d'assistance à la compréhension des systèmes ADAS

## 📄 Licence

Projet académique
