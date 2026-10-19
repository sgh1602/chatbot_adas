"""
Script 1: Préparation des données ADAS
Charge les PDFs et les découpe en chunks
"""

import os
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdfs(data_path):
    """Charge tous les PDFs du dossier"""
    print(f"📂 Chargement des PDFs depuis {data_path}...")
    
    loader = DirectoryLoader(
        data_path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    
    documents = loader.load()
    print(f"✅ {len(documents)} pages chargées depuis les PDFs")
    
    return documents

def split_documents(documents):
    """Découpe les documents en chunks"""
    print("\n✂️ Découpage des documents en chunks...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✅ {len(chunks)} chunks créés")
    
    return chunks

def main():
    # Chemins
    data_path = "../data/pdfs"
    
    # Étape 1: Charger les PDFs
    documents = load_pdfs(data_path)
    
    # Étape 2: Découper en chunks
    chunks = split_documents(documents)
    
    # Sauvegarde info
    print(f"\n📊 Résumé:")
    print(f"   - Nombre de documents: {len(documents)}")
    print(f"   - Nombre de chunks: {len(chunks)}")
    print(f"   - Taille moyenne chunk: ~{sum(len(c.page_content) for c in chunks)//len(chunks)} caractères")
    
    return chunks

if __name__ == "__main__":
    chunks = main()
    print("\n✅ Preprocessing terminé ! Lancez maintenant: 2_create_vectordb.py")
