# bot_server.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
import re

load_dotenv()

# Bot registration secrets
APP_ID = os.getenv("APP_ID")
APP_PASSWORD = os.getenv("APP_PASSWORD")

adapter = BotFrameworkAdapter(BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD))
app = FastAPI()

# Snowflake config
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

# Groq config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# 1. Connect to Snowflake
try:
    engine = create_engine(
        f'snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}?warehouse={SNOWFLAKE_WAREHOUSE}'
    )
    db = SQLDatabase(engine)
except Exception as e:
    print("❌ Failed to connect to Snowflake:", e)
    exit()

# 2. Create LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model=GROQ_MODEL
)

# 3. Custom prompt to prevent markdown wrapping
custom_prompt = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template="""
You are an expert data analyst. Given a user's question and the database schema, write a valid SQL SELECT query to answer it.

- Use only columns that exist in the schema.
- NEVER wrap the query in markdown or backticks.
- Do not explain the query, just write it.

Schema:
{table_info}

Question:
{input}

SQL:
"""
)

# 4. LangChain SQL chain - returning actual query results
db_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    prompt=custom_prompt,
    verbose=True,
    use_query_checker=True,
    return_direct=True  # ✅ THIS makes it return actual query results
)


# 5. Strip ``` from SQL if model still adds them
def extract_sql(text):
    match = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text.strip()

# 6. CLI chat
# def chat():
#     print("\n✅ Connected to Snowflake via LangChain + Groq (LLaMA3)")
#     print("💬 Ask questions about your clinical/financial data.")
#     print("🛑 Type 'exit' to quit.\n")

#     while True:
#         user_input = input("You: ").strip()
#         if user_input.lower() in ["exit", "quit"]:
#             print("👋 Goodbye!")
#             break
#         if not user_input:
#             print("⚠️ Please enter a valid question.")
#             continue

#         try:
#             result = db_chain.invoke({"query": user_input})
#             raw_result = result.get("result", "")
#             clean_result = extract_sql(raw_result)
#             print("\n🤖 Bot:", clean_result, "\n")
#         except Exception as e:
#             print("❌ Error:", str(e))

def chat():
    print("\n✅ Connected to Snowflake via LangChain + Groq (LLaMA3)")
    print("💬 Ask questions about your clinical/financial data.")
    print("🛑 Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        if not user_input:
            print("⚠️ Please enter a valid question.")
            continue

        try:
            result = db_chain.invoke({"query": user_input})
            print("\n🤖 Bot:", result, "\n")  # now prints the DB result directly
        except Exception as e:
            print("❌ Error:", str(e))


if __name__ == "__main__":
    chat()

@app.post("/api/messages")
async def messages(req: Request):
    body = await req.json()
    activity = Activity().deserialize(body)

    async def process(turn_context: TurnContext):
        user_query = turn_context.activity.text
        try:
            result = db_chain.invoke({"query": user_query})
            await turn_context.send_activity(str(result))
        except Exception as ex:
            await turn_context.send_activity(f"Error: {ex}")

    auth = req.headers.get("Authorization", "")
    return await adapter.process_activity(activity, auth, process)
