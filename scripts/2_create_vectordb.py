"""
Script 2: Création de la base vectorielle ChromaDB
Stocke les chunks avec embeddings
"""

import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def load_and_split():
    """Charge et découpe les PDFs"""
    print("[+] Chargement des PDFs...")
    
    # Charger PDFs
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "data", "pdfs")
    pdf_loader = DirectoryLoader(
        pdf_path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = pdf_loader.load()
    print(f"[OK] {len(documents)} pages PDF chargees")
    
    print("\n[>] Decoupage en chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"[OK] {len(chunks)} chunks crees")
    
    return chunks

def create_vectordb(chunks):
    """Crée la base vectorielle avec embeddings"""
    print("\n[>] Creation des embeddings...")
    print("   (Cela peut prendre 2-5 minutes la premiere fois)")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    print("\n[>] Creation de ChromaDB...")
    db_path = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )
    
    vectordb.persist()
    print("[OK] Base vectorielle creee et sauvegardee !")
    
    return vectordb

def main():
    # Étape 1: Charger et découper
    chunks = load_and_split()
    
    # Étape 2: Créer vectordb
    vectordb = create_vectordb(chunks)
    
    print(f"\n[#] Resume:")
    print(f"   - Chunks stockes: {len(chunks)}")
    print(f"   - Base: ../chroma_db")
    print(f"\n[OK] Base vectorielle prete ! Lancez maintenant: 3_test_chatbot.py")

if __name__ == "__main__":
    main()
