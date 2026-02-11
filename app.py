import os
from xml.parsers.expat import model
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "❌ GROQ_API_KEY not found! Did you create a .env file with "
        "GROQ_API_KEY=your_key_here?"
    )
elif not GROQ_API_KEY.startswith("gsk_"):
    print("⚠️ Warning: Your API key doesn't start with 'gsk_'. It might be invalid.")




# conversation history
MESSAGES = []
choice=''

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant and chatbot for conversations."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}")
])


try:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    while(True):
        if(choice.lower()=='exit'):break
        
        answer_response=""
        # response=llm.invoke("Hey hi how are you?")
        # print(response.content)
        # user_query="How to stream (tokens must be displayed one after another) in langchain?"
        user_query = input("user: ")

        formatted_prompt = prompt.format_messages(
            chat_history=MESSAGES,
            input=user_query
        )

        MESSAGES.append({'role':'User','content:':user_query})
        print("\nLLM: \n")
        for chunk in llm.stream(formatted_prompt):
            print(chunk.text, end="", flush=True)
            answer_response+=chunk.text


        MESSAGES.append({'role':'assistant','content':answer_response})
        print("\n----Debug----\n ",MESSAGES)

        choice=input("Enter exit for terminating or enter for continue :")


except Exception as e:
    print(f"❌ An error occurred: {e}")
    
