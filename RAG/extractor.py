import fitz  # PyMuPDF
import json


def get_text_from_pdf(pdf_path):
    try:
        document = fitz.open(pdf_path)
        text = ""
        for page in document:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        raise
    finally:
        if 'document' in locals():
            document.close()


def summarize_data_from_json(json_filepath, client):
    # Read JSON data from file
    with open(json_filepath, 'r') as file:
        data = json.load(file)

    summaries = []

    for item in data:
        # Prepare the content to be summarized
        content = f"Question: {item['content']}\n"
        content += f"Answer: {item['answer']}\n"
        content += f"Comment: {item['comment']}\n"

        # Generate summary using OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes information."},
                {"role": "user", "content": f"Please summarize the following content:\n\n{content}"}
            ],
            max_tokens=1024
        )

        summary = response.choices[0].message.content.strip()
        summaries.append(summary)

    return "\n".join(summaries)
