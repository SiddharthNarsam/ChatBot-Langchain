import os
from xml.parsers.expat import model
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "❌ GROQ_API_KEY not found! Did you create a .env file with "
        "GROQ_API_KEY=your_key_here?"
    )
elif not GROQ_API_KEY.startswith("gsk_"):
    print("⚠️ Warning: Your API key doesn't start with 'gsk_'. It might be invalid.")

def Generate_Summary():
    summary_prompt = f"""
            I am giving you the list of conversations (chat history).
            Please summarize:

            1) System/Assistant responses
            2) Human/User inputs

            First give system summary.
            Then use '***' as separator.
            Then give human summary.

            Chat History:
            {MESSAGES}
            """
    response = llm.invoke(summary_prompt)
    summary_output=response.content

    system_summary, human_summary = summary_output.split("***")

    system_summary = system_summary.strip()
    human_summary = human_summary.strip()

    print(f"\n\n Note: ---- Summary Generated ----")
    # print("Human Summary:\n", human_summary)
    # print("System Summary:\n", system_summary)





# conversation history  
MESSAGES = []
try:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant and chatbot for conversations."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}")
    ])

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
    )


    while True:
        user_query = input("USER : ")

        if user_query.lower() == "exit":
            break

        formatted_prompt = prompt.format_messages(
            chat_history=MESSAGES,
            input=user_query
        )

        print("\nLLM :\n")

        answer_response = ""

        for chunk in llm.stream(formatted_prompt):
            print(chunk.content, end="", flush=True)
            answer_response += chunk.content

        MESSAGES.append({'role':'user','content':user_query})
        MESSAGES.append({'role':'assistant','content':answer_response})

        if len(MESSAGES)==6:
            Generate_Summary()


        print(f"\n\n----Debug History Size: {len(MESSAGES)} messages----")



except Exception as e:
    print(f"❌ An error occurred: {e}")
    
