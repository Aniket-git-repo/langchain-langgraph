from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import input_content
load_dotenv()

system_prompt = '''You are an HR compliance auditor.

Review the draft policy and find out missing compliance clauses , any ambiguous language and suggest improvements
{policy_text}

Return your response strictly in the following JSON format
{{
  "Issues": [],
  "Severity": [],
  "Recommendations": []
}} 
Cite references from the original policy text where applicable, with format as Context : Policy text

Do not invent new compliance rules instead suggest suggestion from provided context only.
'''


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
prompt_template = ChatPromptTemplate.from_template(system_prompt)
chain = prompt_template | llm
result = chain.invoke({"policy_text" : input_content.policy_text})
print(result.content.replace('```','').replace('json',''))