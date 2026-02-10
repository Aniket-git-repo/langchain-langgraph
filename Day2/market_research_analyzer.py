from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import input_content
load_dotenv()

system_prompt = '''You are a market research analyst.

Generate a market analysis brief from the below provided article 

{market_article}
Include SWOT analysis, top 3 trends with source citations and narrative summary

Please do not fabricate ant data and ensure all outputs are supported by the source article provided

Return your response strictly in the following format

  "SWOT": {{ "..." }},
  "trends": {{ "..." }},
  "citation": {{ "..." }},
  "summary" : {{ "..." }}
'''

prompt_template = ChatPromptTemplate.from_template(system_prompt)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
chain = prompt_template | llm
result = chain.invoke({"market_article" : input_content.market_article})
print(result.content.replace('```','').replace('json',''))