import os
from dotenv import load_dotenv
from prompts import system_prompt
from config import MAX_ITERS

from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import create_agent
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file_content import write_file_content
from functions.create_directory import create_directory
from functions.delete_file_or_directory import delete_path
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

style = Style.from_dict({"placeholder": "#888888 italic"})

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
model = os.environ.get("MODEL")
# coding_temperature = os.environ.get("CODING_TEMPERATURE")
temperature = os.environ.get("TEMPERATURE")
coding_top_p = os.environ.get("CODING_TOP_P")
num_predict = os.environ.get("NUM_PREDICT")

tools = [
    get_files_info,
    get_file_content,
    run_python_file,
    write_file_content,
    create_directory,
    delete_path,
]

client = ChatGoogleGenerativeAI(model=model, google_api_key=api_key, temperature=float(temperature))
# client = ChatOllama(
#     model=model,
#     temperature=float(coding_temperature),
#     validate_model_on_init=True,
#     num_predict=int(num_predict),
#     top_p=float(coding_top_p),
# )
agent = create_agent(model=client, tools=tools, system_prompt=system_prompt)


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
        return AIMessage(
            content=f"Error: {str(e)}\nPlease try rephrasing your request or provide more specific details."
        )


def main():
    print("\n*********************************************")
    print("Hi there! What do you want me to do for you?")
    print("*********************************************\n")

    history = [SystemMessage(content=system_prompt)]
    current_iterations = 0
    while True:
        if current_iterations > MAX_ITERS:
            print("Max iterations reached!")
            break

        user_query = prompt(
            ">>> ", placeholder="Send a message (/bye to quit)", style=style
        ).strip()

        if user_query.lower() in ["/bye"]:
            print("Goodbye!")
            break

        print(
            f"\nAGENT"
            + (" (Type '/bye' to quit)" if "exit" in user_query else "")
            + ": ",
            end="",
            flush=True,
        )

        if user_query == "":
            res = "Empty query! Please provide some input."
            print(res + "\n")
        else:
            history.append(HumanMessage(content=user_query))
            res = run_agent(history)
            history.append(res)
            current_iterations += 1
            print(res.content + "\n")


if __name__ == "__main__":
    main()
