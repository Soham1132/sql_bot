# app.py
# app.py

from langchain_groq import ChatGroq
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain  # ✅ correct source
from sqlalchemy import create_engine
import os

# 1. ENV CONFIG (replace with your real values or use dotenv)
SNOWFLAKE_USER = 'username'
SNOWFLAKE_PASSWORD = 'password'
SNOWFLAKE_ACCOUNT = 'account'   # like xy12345.ap-south-1
SNOWFLAKE_DATABASE = 'db'
SNOWFLAKE_SCHEMA = 'PUBLIC'
SNOWFLAKE_WAREHOUSE = 'warehouse'

GROQ_API_KEY = 'your_api_key'
GROQ_MODEL = 'llama3-70b-8192'  # or llama3-8b-8192

# 2. Connect to Snowflake using SQLAlchemy
engine = create_engine(
    f'snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}?warehouse={SNOWFLAKE_WAREHOUSE}'
)

# Create LLM
llm = ChatGroq(
    groq_api_key="your_api_key",
    model="llama3-70b-8192"
)

# Set up LangChain SQL DB wrapper
db = SQLDatabase(engine)

# Set up the chain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)


# 5. Chat Loop
def chat():
    print("📊 Connected to Snowflake DB via LLaMA3.3")
    print("💬 Ask a question (type 'exit' to quit):\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        try:
            response = db_chain.run(user_input)
            print("Bot:", response)
        except Exception as e:
            print("❌ Error:", str(e))

if __name__ == "__main__":
    chat()
