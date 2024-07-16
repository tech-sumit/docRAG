from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import ServerlessSpec
import pinecone


def create_index(pc, index_name):
    try:
        if index_name not in pc.list_indexes().names():
            pc.create_index(index_name,
                                  dimension=384,
                                  metric="cosine",
                                  spec=ServerlessSpec(
                                      cloud="aws",
                                      region="us-east-1"
                                  ))
    except pinecone.exceptions.PineconeException as e:
        print(f"Error creating index: {e}")
        raise


def add_text_to_vector_store(index_name, text, model, pinecone):
    try:
        index = pinecone.Index(index_name)

        chunk_size_tok = 1024
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size_tok, chunk_overlap=512
        )
        texts_split = text_splitter.split_text(text)

        for i, chunk in enumerate(texts_split):
            vector = model.encode(chunk).tolist()
            vector_id = f"chunk-{i}-{hash(chunk)}"
            index.upsert([(vector_id, vector, {"text": chunk})])
    except Exception as e:
        print(f"Error adding text to vector store: {e}")
        raise
