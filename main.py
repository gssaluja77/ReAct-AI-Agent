import os
from dotenv import load_dotenv
from prompts import system_prompt
from config import MAX_ITERS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import create_agent
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file_content import write_file_content

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
model = os.environ.get("MODEL")
temperature = os.environ.get("TEMPERATURE")

tools = [get_files_info, get_file_content, run_python_file, write_file_content]

client = ChatGoogleGenerativeAI(model=model, google_api_key=api_key, temperature=float(temperature))
agent = create_agent(client, tools=tools, system_prompt=system_prompt)

def run_agent(messages):
    try:
        res = agent.invoke(input={"messages": messages}, config={"recursion_limit": 50})
        last_message = res["messages"][-1]

        ai_text = ""
        if isinstance(last_message.content, list):
            ai_text = " ".join(
                chunk.get("text", "").strip()
                for chunk in last_message.content
                if isinstance(chunk, dict) and chunk.get("type") == "text"
            )
        else:
            ai_text = str(last_message.content).strip()

        return AIMessage(content=ai_text)
        
    except Exception as e:
        return AIMessage(content=f"Error: Please try rephrasing your request or provide more specific details.")

def main():
    print("\n*************************************************")
    print("Hi there! What do you want me to do for you?")
    print("*************************************************\n")

    history = [SystemMessage(content=system_prompt)]
    current_iterations = 0
    while True:
        if current_iterations > MAX_ITERS:
            print("Max iterations reached!")
            break
        user_query = input("You: ").strip()

        if user_query.lower() in ['/bye']:
            print("Goodbye!")
            break
        
        print("\nAgent: ", end="", flush=True)
        if user_query == "":
            res = "Empty query! Please provide some input."
            print(res + '\n')
        else:
            history.append(HumanMessage(content=user_query))
            res = run_agent(history)
            history.append(res)
            current_iterations += 1
            print(res.content + '\n')

if __name__ == "__main__":
    main()