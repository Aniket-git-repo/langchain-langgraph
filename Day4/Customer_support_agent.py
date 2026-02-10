from langgraph.graph import StateGraph, START, END
from typing_extensions import  TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import json
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import input_content
load_dotenv()

# 1. Define the expected output schema using Pydantic
class EmailInfo(BaseModel):
    Urgency: str = Field(description="Urgency of the email")
    Topic: str = Field(description="Email Topic")

# 2. Create a JSON output parser based on the schema
parser = JsonOutputParser(pydantic_object=EmailInfo)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

class State_Gh(TypedDict):
    email_details : str
    email_urgency: str
    email_topic: str
    email_response : str
    human_support_escalation: str
    final_outcome: str
    email_drafted: str

email_workflow = StateGraph(state_schema=State_Gh)

def analyze_email(state: State_Gh) -> State_Gh:
    prompt_template = ChatPromptTemplate.from_template("Analyze the email and categorize the urgency of the email as 'Low', 'Medium', 'High' also "
                                                       "categorize the email into topics like 'Account', 'Billing', 'Bug', 'Feature Request', 'Technical Issue'"
                                                       "Email : {email}"
                                                       "{format_instructions}"
                                                       "If the urgency and topic is undermined return the value as UNKNOWN"
                                                      )
    chain = prompt_template | model

    orig_response = chain.invoke({"email" : state["email_details"],
                                  "format_instructions" : parser.get_format_instructions()})
                                  

    response_str = orig_response.content.replace("```", "").replace("json","")

    json_content = json.loads(response_str)

    if (json_content["Urgency"] == "UNKNOWN") or (json_content["Topic"] == "UNKNOWN"):
        return {"email_urgency": json_content["Urgency"],
                "email_topic": json_content["Topic"],
                "human_support_escalation": "Y",
                "email_drafted" : "N"}

    else :
        return {"email_urgency" : json_content["Urgency"],
                "email_topic" : json_content["Topic"],
                "human_support_escalation": "N",
                "email_drafted" : "N"}



def draft_email_response(state: State_Gh) -> State_Gh:
    prompt_template = ChatPromptTemplate.from_template("You are expert in drafting e-mail"
                "Based on the e-mail below draft a response for the user. Refer to the knowledge base to get answers to the question asked"
                "Email : {email}"
                "Knowledge Base document : {knowledge_base}"
                "The solutions provided should follow the knowledge base document"
                "Do not draft any e-mail if there are no matching details related to the issue in the knowledge base document return the keyword UNKNOWN"
                )
    chain = prompt_template | model
    response = chain.invoke({"email": state["email_details"],
                             "knowledge_base" : input_content.knowledge_base_doc_string}).content
    if response.__contains__("UNKNOWN"):
        return {"human_support_escalation": "Y", "email_drafted" : "N", "email_response" : "UNKNOWN"}
    else :

        return {"final_outcome" : "Based on the e-mail received, please find the response below",
               "email_response": response,
               "email_drafted" : "Y",
               "human_support_escalation": "N"}


def human_sup_escalation(state: State_Gh) -> State_Gh:

    return {"final_outcome" : "No specific details found from the knowledge base provided, escalating to human support agent"}

def send_email(state: State_Gh) -> State_Gh:
    pass
    return {"send_email" : "Sending Email ...."}


def routing_function(state: State_Gh) -> str :


    if state["human_support_escalation"] == "Y" :
        return "human_sup_escalation"
    elif state["email_drafted"] == "Y" :
        return "send_email"
    else:
        return "draft_email_response"


selection_map = {"draft_email_response": "draft_email_response",
                 "human_sup_escalation": "human_sup_escalation",
                }
selection_map1 = {"send_email": "send_email",
                 "human_sup_escalation": "human_sup_escalation",
                }
email_workflow.add_node("analyze_email", analyze_email)
email_workflow.add_node("draft_email_response", draft_email_response)
email_workflow.add_node("human_sup_escalation", human_sup_escalation)
email_workflow.add_node("send_email", send_email)
email_workflow.add_edge(START,"analyze_email")
email_workflow.add_conditional_edges("analyze_email", routing_function, selection_map )
email_workflow.add_conditional_edges("draft_email_response", routing_function, selection_map1 )
email_workflow.add_edge("send_email",END)
email_workflow.add_edge("human_sup_escalation",END)
app = email_workflow.compile()
print_graph = input('Do you want to print the graph? (Y/N) ')
match print_graph:
  case 'Y':
      graph_path = input('Please enter the path of the graph: ')
      app.get_graph().draw_mermaid_png(output_file_path=rf'{graph_path}\email_flow_graph.png')
  case _ :
      pass
sample_email = input_content.email_details
final_response = app.invoke({"email_details": sample_email})
print('Final Output .......')
print('Email Urgency : ', final_response['email_urgency'])
print('Identified Topic : ', final_response['email_topic'])
print('Generated Response Draft : ', final_response['email_response'])
print('Decision on Autoreply vs Escalation : ', 'Auto Reply' if final_response['email_drafted'] == 'Y'  else 'Escalation')
print('Followup Action Required : ', 'Yes' if final_response['email_drafted'] == 'Y' else 'No')
