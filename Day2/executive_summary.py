from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader


def load_pdf_doc(doc_path):
    try:
            loader = PyPDFLoader(rf"{doc_path}")
            pages = loader.load()  # Returns a list of Document objects
            final_document = []
            j=0
            for i in pages:

                final_document.append(pages[j].page_content)
                j = j+1
            return final_document

    except Exception as e:
            raise RuntimeError(f"Error loading PDF: {e}")
document_path = input("Please enter the path of the pdf document ")
final_doc = load_pdf_doc(document_path)
all_pages = " ".join(final_doc)
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
template = ('''You are a helpful assistant and your task is to summarize the given topic in 150 words and include table of metrics, risk/opportunity sections
            The response should be generated based on the source document with no reference to outside source
            Strictly follow source citation''')
human_template =  "Write a summary about {user_inpt} "
prompt_message = ChatPromptTemplate.from_messages([("system", template),
("human", human_template)])
messages  = prompt_message.invoke({"user_inpt" : all_pages})
response = model.invoke(messages)
print('Generating response ...')
print(response.content)
