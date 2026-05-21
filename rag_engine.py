import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

CHROMA_PATH = "chroma_db"
DATA_PATH = "company_guidelines.txt"

def build_rag_database():
    """Reads the guidelines text file and embeds it into ChromaDB."""
    print("Building RAG Database...")
    
    # 1. Load the document
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return
        
    loader = TextLoader(DATA_PATH)
    documents = loader.load()

    # 2. Split into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)

    # 3. Save to ChromaDB (Create vector embeddings)
    # Note: Requires OPENAI_API_KEY in .env
    db = Chroma.from_documents(
        chunks, 
        OpenAIEmbeddings(), 
        persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

def get_rag_context(query: str) -> str:
    """Retrieves relevant company guidelines from the database."""
    # Note: Requires OPENAI_API_KEY in .env
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # Retrieve top 3 most relevant chunks
    results = db.similarity_search_with_relevance_scores(query, k=3)
    
    if len(results) == 0:
        return "No specific guidelines found for this query."
        
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    return context_text

if __name__ == "__main__":
    # If run directly, build the database
    build_rag_database()
