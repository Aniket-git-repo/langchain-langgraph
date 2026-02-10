from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

system_prompt = '''You are an expert in Email writing.

Draft a professional e-mail to clients summarizing project progress, milestones and request feedback from them

The e-mail should be formal and professional.


The e-mail body should have placeholder for client name, project name deadline and action items
The response should have separate subject line and e-mail body and the body should have bullet points for action items.
'''


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
result = llm.invoke(system_prompt)
print(result.content)