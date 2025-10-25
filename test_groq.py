from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key="your_api_key",
    model="llama3-70b-8192"
)

response = llm.invoke("Summarize the benefits of Snowflake database.")
print(response.content)
