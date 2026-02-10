from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import input_content
load_dotenv()

system_prompt = '''You are an expert AI prompt engineer.

Evaluate the user prompt based on the criteria below.


Evaluation Criteria:
1. Clarity – Is the goal clear and easy to understand?
2. Specificity & Details – Are sufficient details and requirements provided?
3. Context – Is background, audience, or use case mentioned?
4. Output Format & Constraints – Is output format, tone, or length specified?
5. Persona Defined – Is a role or persona assigned to the AI?

Return your response strictly in the following format

  "clarity": {{ "score": X, "reason": "..." }},
  "specificity": {{ "score": X, "reason": "..." }},
  "context": {{ "score": X, "reason": "..." }},
  "output_constraints": {{ "score": X, "reason": "..." }},
  "persona": {{ "score": X, "reason": "..." }},
  "final_score": X,
  "summary": "...",
  "suggestions": ["...", "...", "..."]
'''


prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
final_prompt = prompt_template.invoke({"input":input_content.sample_prompt})
result = llm.invoke(final_prompt)
print(result.content)