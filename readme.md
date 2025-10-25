
# Snowflake Chat-Interface with Groq + LangChain

## 📋 Overview  
This project builds an interactive command-line chatbot that connects to a Snowflake database and uses a large language model via the ChatGroq integration (via LangChain) to answer natural‐language queries about your data.  
It uses:  
- A Snowflake connection via SQLAlchemy  
- The `SQLDatabaseChain` from LangChain to map natural language → SQL → result  
- The ChatGroq model (e.g., `llama3-70b-8192`) to interpret the queries and respond  

---

## 🧩 Features  
- Connects to Snowflake (warehouse, database, schema)  
- Translates user questions into SQL queries and executes them  
- Returns results with contextual responses via a LLM  
- Simple CLI interface (type queries; type `exit` to quit)  

---

## ⚙️ Prerequisites  
- A Snowflake account with:  
  - Username, password  
  - Account identifier (e.g., `xy12345.ap-south-1`)  
  - Database, schema, and warehouse accessible  
- A Groq API key. You’ll use a model from Groq (e.g., `llama3-70b-8192`) via ChatGroq. :contentReference[oaicite:2]{index=2}  
- Python 3.9+ (tested)  
- Packages: `langchain`, `langchain-community`, `langchain-groq`, `sqlalchemy`, `snowflake-connector-python` (or SQLAlchemy driver)  

---

 🚀 Installation  

``bash
# Clone the repo  
git clone <your-repo-url>  
cd <repo-folder>

# Create a virtual environment  
python3 -m venv venv  
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies  
pip install -U langchain langchain-community langchain-groq sqlalchemy snowflake-sqlalchemy   # and any others
`



🧰 Environment Configuration

Create a `.env` file or set the following environment variables:

`text
SNOWFLAKE_USER=<your_username>
SNOWFLAKE_PASSWORD=<your_password>
SNOWFLAKE_ACCOUNT=<account_identifier>
SNOWFLAKE_DATABASE=<database_name>
SNOWFLAKE_SCHEMA=<schema_name>
SNOWFLAKE_WAREHOUSE=<warehouse_name>

GROQ_API_KEY=<your_groq_api_key>
GROQ_MODEL=<model_name>   # e.g., llama3-70b-8192 or llama3-8b-8192
`

You can also embed these values directly in `app.py` (though environment variables are recommended for security).

---

## 🧮 Usage

1. Ensure your Snowflake credentials and Groq API key are correctly set.
2. Run the app:

``bash
python app.py
``

3. You’ll see the prompt:

`
📊 Connected to Snowflake DB via LLaMA3.3  
💬 Ask a question (type 'exit' to quit):
``

4. Enter your query in natural language (for example: *“Show me total sales by region for last year.”*)
5. The system will:

   * Use the `SQLDatabaseChain` to interpret the query
   * Run the equivalent SQL on Snowflake
   * Use ChatGroq to provide a conversational answer
6. To exit the chat: type `exit` or `quit`

---

## 🛠 Customization

* **Model:** Adjust `GROQ_MODEL` in `app.py` to use a different model supported by Groq.
* **Verbosity:** The chain is set with `verbose=True` to log SQL queries; you may disable it.
* **Prompting:** You may customise the system/human messages, prompt templates, or add memory chains to support conversational history.
* **Error Handling:** The example catches exceptions; for production you may add more robust logging.

---

## ✅ Limitations & Notes

* The SQL generation relies on the quality of the LLM’s interpretation; you should validate generated SQL for correctness & safety (especially destructive statements).
* Ensure your Snowflake warehouse can handle the queries in terms of cost and performance.
* The Groq key and model usage may incur cost depending on your plan at Groq.
* For production, consider authentication, secrets management, and frontend integration (e.g., Web UI) rather than CLI.

---

## 📚 References

* ChatGroq (LangChain integration) docs: [LangChain Groq Integration]([LangChain][1])
* LangChain SQLDatabaseChain docs: ([GitHub][2])
* Medium guide: Building RAG App with LangChain + Groq ([Medium][3])

---

## 🔏 License & Attribution

Specify your own license (e.g., MIT) and attribution details as needed.

---

Thank you for using this demo — feel free to contribute improvements or ask questions!

[1]: https://python.langchain.com/docs/integrations/chat/groq/?utm_source=chatgpt.com "ChatGroq - ️ LangChain"
[2]: https://github.com/langchain-ai/langchain/blob/master/docs/docs/integrations/chat/groq.ipynb?utm_source=chatgpt.com "langchain/docs/docs/integrations/chat/groq.ipynb at master - GitHub"
[3]: https://sangeethasaravanan.medium.com/building-a-simple-rag-app-using-langchain-chroma-and-groqs-mixtral-ee6504206a9d?utm_source=chatgpt.com "Building a Simple RAG App Using LangChain, Chroma, and Groq's ..."
