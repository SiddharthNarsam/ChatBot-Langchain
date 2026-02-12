import os
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

MESSAGES = []
CURRENT_SUMMARY = ""


def Generate_Summary():
    global MESSAGES, CURRENT_SUMMARY
    
    # We ask the LLM to merge the old summary with the new messages
    summary_prompt = f"""
    Current Summary: {CURRENT_SUMMARY}
    
    New Conversation to add:
    {MESSAGES}
    
    Please provide a new, updated summary that captures the key points of the 
    entire conversation so far. Be concise.
    """
    
    response = llm.invoke(summary_prompt)
    CURRENT_SUMMARY = response.content
    
    # Clear history after summarizing to save space/tokens
    MESSAGES = [] 
    print(f"\n--- ✨ Summary Updated & History Cleared ---")




try:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Previous context: {summary}"),
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
            summary=CURRENT_SUMMARY,
            input=user_query
        )

        print("\nLLM :", end="")

        answer_response = ""

        for chunk in llm.stream(formatted_prompt):
            print(chunk.content, end="", flush=True)
            answer_response += chunk.content

        MESSAGES.append({'role':'human','content':user_query})
        MESSAGES.append({'role':'assistant','content':answer_response})

        if len(MESSAGES)>=6:
            Generate_Summary()


        print(f"\n\n----Debug History Size: {len(MESSAGES)} messages----")



except Exception as e:
    print(f"❌ An error occurred: {e}")
    
