from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_core.output_parsers import StrOutputParser
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from src.prompt import *


load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")


def file_processing(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()
    question_gen = ""
    for page in data :
        question_gen = question_gen + page.page_content

    splitter_gen = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200
)
    chunks_generation = splitter_gen.split_text(question_gen)
    doc_generation = [Document(page_content = t) for t in chunks_generation ]
    documnet_splitter_template = RecursiveCharacterTextSplitter(
    chunk_size=2000,  # number of characters
    chunk_overlap=200
)
    docs =  documnet_splitter_template.split_documents(doc_generation)
    llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0,
    max_tokens=512,
   
)
    
    PROMPT_TEMPLATE  = PromptTemplate(
    template=prompt,
    input_variables=['text']
)
    SUMMARY_PROMPT = PromptTemplate(
    template=prompt,
    input_variables=["text"]
)
    map_chain = SUMMARY_PROMPT | llm | StrOutputParser()
    config = RunnableConfig(
    max_concurrency=2  # start with 1 or 2
)
    chunk_summaries = []

    for doc in docs:
        summary = map_chain.invoke({
        "text": doc.page_content
    })
    chunk_summaries.append(summary)

    COMBINE_PROMPT = PromptTemplate(
    template=COMBINE_THIS_PROMPT,
    input_variables=["text"]
)
    combine_chain = COMBINE_PROMPT | llm | StrOutputParser()
    final_summary = combine_chain.invoke({
    "text": "\n\n".join(chunk_summaries)
})
    # bullet_lines = []
    # for line in final_summary:
    #     for subline in line.split("\n"):
    #         clean_line = subline.strip()
    #         if clean_line:  # remove empty lines
    #             bullet_lines.append(clean_line)
    # # final_summary = final_summary.split("\n")
    # # final_summary = [q.strip() for q in final_summary if q.strip()]
    # # return bullet_lines
    # char_list =  bullet_lines            
    # summary_text = "".join(char_list)
    # # Remove first sentence (optional)
    # sentences = summary_text.split(". ")  # split by period + space
    # bullet_lines = sentences[1:]  # skip the first sentence

    # # Clean up whitespace
    # bullet_lines = [line.strip() for line in bullet_lines if line.strip()]

    return final_summary
    # from fastapi.responses import JSONResponse
    # return JSONResponse(content={"bullets": bullet_lines})
    



