# Question-Answering Bot API

This project implements a backend API for a Question-Answering bot that leverages the capabilities of a large language model. The bot can answer questions based on the content of a document using OpenAI's GPT model and Pinecone vector database.

## Features

- Supports input file types: JSON and PDF
- Processes three input files:
  - A JSON file containing a list of questions
  - A PDF file containing the document to be queried
  - A JSON file with additional data
- Outputs a structured set of answers to the provided questions based on the document content
- Uses Pinecone as a vector database for efficient document querying
- Implements the API using Flask with a web interface

## Technologies Used

- Python 3.x
- OpenAI API (gpt-3.5-turbo model)
- Pinecone (Vector Database)
- Flask
- PyMuPDF (for PDF processing)
- Sentence Transformers
- dotenv (for environment variable management)

## Setup and Installation

1. Clone the repository:
   ```
   https://github.com/tech-sumit/docRAG.git
   cd docRAG
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   FLASK_SECRET_KEY=your_flask_secret_key
   ```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Access the web interface at `http://localhost:5000`

3. Upload the required files:
   - JSON file with questions
   - PDF file with the document content
   - JSON file with additional data

4. The application will process the files, create a Pinecone index, add the document content to the vector store, and generate answers to the questions.

5. The answers will be displayed on the results page.

## File Structure

- `app.py`: Main Flask application
- `RAG/`: Package containing the core functionality
  - `agent.py`: Implements the question-answering logic
  - `extractor.py`: Handles text extraction from PDF and JSON files
  - `vector_store.py`: Manages interactions with the Pinecone vector database
- `templates/`: HTML templates for the web interface
  - `template.html`: Upload form template
  - `results.html`: Results display template
- `uploads/`: Temporary storage for uploaded files (not included in the repository)

## API Endpoints

- `GET /`: Renders the upload form
- `POST /`: Handles file uploads, processes the documents, and returns the answers
- `GET /uploads/<name>`: Serves uploaded files (for downloading)

## Error Handling

The application includes basic error handling for file uploads and processing. Error messages are displayed to the user using Flask's flash messages.

## Security Considerations

- The application uses `werkzeug.utils.secure_filename()` to sanitize uploaded filenames.
- A maximum content length of 16MB is set for uploads.
- The Flask secret key is stored as an environment variable.

## Limitations

- The current implementation does not include user authentication or rate limiting.
- Uploaded files are temporarily stored on the server and should be cleaned up regularly in a production environment.
- The application is set to run in debug mode, which should be disabled in a production setting.

## Potential Improvements

- Authentication and Authorization: Implement user authentication and authorization to secure the API and manage access to different functionalities.
- Rate Limiting: Add rate limiting to prevent abuse of the API and ensure fair usage among users.
- Asynchronous Processing: Implement asynchronous processing for large documents or multiple requests to improve performance and user experience.
- Improved Error Handling: Enhance error handling and provide more detailed error messages to assist in troubleshooting.
- File Cleanup: Implement a scheduled task to clean up temporary files in the uploads folder.
- Caching: Implement caching mechanisms to store frequently accessed data and reduce processing time for repeated queries.
- Logging: Add comprehensive logging throughout the application for better monitoring and debugging.
- Testing: Develop a comprehensive test suite including unit tests, integration tests, and end-to-end tests.
- Documentation: Improve inline code documentation and create API documentation using tools like Swagger or ReDoc.
- Containerization: Containerize the application using Docker for easier deployment and scaling.
- Scalability: Implement load balancing and consider serverless options for improved scalability.
- User Interface Enhancements: Improve the web interface with features like progress indicators, better error displays, and a more intuitive design.
- Support for Additional File Formats: Extend support to other document formats beyond PDF and JSON.
- Fine-tuning: Explore options for fine-tuning the language model on domain-specific data to improve answer quality.
- Answer Quality Metrics: Implement metrics to evaluate the quality of answers and provide confidence scores.
- Feedback Mechanism: Add a user feedback system to continually improve the model's performance based on user input.
- Multi-language Support: Extend the application to support multiple languages for both input documents and questions.


# Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
