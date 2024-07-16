# POC FILE: to test the functionality before making complete project. this can be used to get results without running
# server to test the functionality
# Import necessary libraries
import os
from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from RAG import vector_store, extractor


def find_answers_in_pdf(index_name, questions, client, model, pinecone):
    # Connect to the Pinecone index
    index = pinecone.Index(index_name)

    answers = {}

    for question in questions:
        # Encode the question
        query_vector = model.encode(question).tolist()

        # Query Pinecone
        results = index.query(vector=query_vector, top_k=4, include_metadata=True)

        # Extract the relevant text chunks
        context = " ".join([result.metadata['text'] for result in results.matches])

        # Generate an answer using OpenAI
        answer = generate_answer(client, question, context)

        answers[question] = answer

    return answers


def generate_answer(client, question, context):
    prompt = f"""
    Context: {context}

    Question: {question}

    Please provide a concise and accurate answer to the question based on the given context. 
    If the context doesn't contain enough information to answer the question confidently, 
    please state that the information is not available in the given context.

    Answer:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that answers questions based on provided context."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        n=1,
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()


# Example usage
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Initialize SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Initialize Pinecone
    pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    pdf_filepath = "../docs/soc2_csa_ccm_report.pdf"
    questions = [
        "What is the main topic of the document?",
        "What are the key findings mentioned in the text?",
    ]

    index_name = "soc-csa-ccm-report"

    # create the pinecone index
    vector_store.create_index(pinecone, index_name)

    # get the data from pdf
    pdf_data = extractor.get_text_from_pdf(pdf_filepath)

    # add the data to the vector store
    vector_store.add_text_to_vector_store(index_name, pdf_data, model, pinecone)

    answers = find_answers_in_pdf(index_name, questions, client, model, pinecone)

    for question, answer in answers.items():
        print(f"Q: {question}")
        print(f"A: {answer}\n")