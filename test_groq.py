from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key="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",
    model="llama3-70b-8192"
)

response = llm.invoke("Summarize the benefits of Snowflake database.")
print(response.content)
