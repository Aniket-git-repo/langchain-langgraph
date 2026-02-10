from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import input_content
load_dotenv()

system_prompt = '''You are a meeting assistant, who summarizes the meeting minutes based on the transcript provided.

Summarize the following transcript into structured markdown with sections as shown below:

{transcript}

Decision : ...
Action Item: ...
Ownership :
Deadline :
Confidence score to achieve the deadline :

Please avoid putting any details outside of the meeting transcript provided.
'''

prompt_template = ChatPromptTemplate.from_template(system_prompt)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
chain = prompt_template | llm
result = chain.invoke({"transcript" : input_content.meeting_transcript})
print(result.content)