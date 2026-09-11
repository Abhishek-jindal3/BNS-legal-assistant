
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_chroma import Chroma

from bns_loader import load_and_chunk_bns

from config import (
    EMBEDDING_MODEL,
    CHROMA_PATH,
    COLLECTION_NAME,
    RETRIEVAL_K
)



# Create embedding model


embedding_model = NVIDIAEmbeddings(
    model=EMBEDDING_MODEL
)



# Get or create Chroma database


def get_vectorstore():

    # Open existing Chroma database
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,

        embedding_function=embedding_model,

        persist_directory=CHROMA_PATH
    )


    # Check whether the database already contains documents
    document_count = vectorstore._collection.count()


    # If database is empty, create it for the first time
    if document_count == 0:

        final_chunks = load_and_chunk_bns()


        vectorstore.add_documents(
            documents=final_chunks
        )


    return vectorstore


# --------------------------------------------------
# Create retriever
# --------------------------------------------------

def get_retriever():

    vectorstore = get_vectorstore()


    retriever = vectorstore.as_retriever(

        search_type="similarity",

        search_kwargs={
            "k": RETRIEVAL_K
        }
    )


    return retriever


# --------------------------------------------------
# Format retrieved BNS documents
# --------------------------------------------------

def format_docs(docs):

    return "\n\n".join(

        f"Section {doc.metadata.get('section', 'Unknown')}:\n"
        f"{doc.page_content}"

        for doc in docs
    )