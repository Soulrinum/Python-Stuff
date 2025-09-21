from langchain_core.messages import HumanMessage #Langchain is a high level framework that allows us to build Ai Applications 
from langchain_openai import ChatOpenAI #Audits the use of OpenAi within Langchain and Langgraph. 
from langchain.tools import tool 
from langgraph.prebuilt import create_react_agent #Langgraph is a high level framework that allows us to build Ai Agents 
from dotenv import load_dotenv #Dotenv, loads envrioment variable files from within the python script. 
import numpy as np 

#I will be building an AI Agent which differes from a chatbot as AI Agents have access to a variety of tools. 

load_dotenv()

@tool 
def calc(v: float) -> str: 
    """Calculate the photon energy (in eV) from its frequency v (Hz)."""
    plancks_constant = 6.62e-34
    electron_charge = 1.602e-19
    print("X-ray Energy Calc Tool.")
    energy = (plancks_constant * v) / electron_charge
    return f"The energy of your X-ray photon is {energy:.3e} eV"

  

def main(): 
  model = ChatOpenAI(temperature=0) #The higher the tempreature the more random the model will be. 

  tools = [calc]
  agent_executor = create_react_agent(model, tools) #Creates an agent executor which requires the parameter of model and tools. 

  print("Welcome! I'm Rayeed Your AI Assistant. Type 'Exit' to exit.")
  print("As I am Bangladeshi You Can Ask Me To Perform Calculations.")

  while True: 
    user_input = input("\nYou:").strip()

    if user_input.lower() == "exit": 
      break 

    print("\nRayeed: ", end="") #Pritns next to "Rayeed:" rather then a new line which is default. 
    for chunk in agent_executor.stream( #Chunks are essentially parts of a response coming from the agent. 
        {"messages": [HumanMessage(content=user_input)]} #"Stream" collects the content from user input, where Humanmessage ensures the AI agent is aware the content is from an actual human. "Stream" is then used to collect responses from the LLM. Which we established earlier is agent_executor. 
    ):
        if "agent" in chunk and "messages" in chunk["agent"]:  #Checks if there is an agent response, if so check if there are any messages. If there are messages they will be looped through. Lastly they will be printed, where again end ensures the responses are on the same line. 
            for message in chunk["agent"]["messages"]: 
               print(message.content, end="")
    print()


if __name__ == "__main__": #Used to execute main function. Essentially main() will be only called within this file. This prevents issues when importing files. 
   main()

