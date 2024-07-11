#!/usr/bin/env python


from PyPDF2 import PdfReader

# 1. Leer Documento

# Markdown
# text = ""
# with open("BR.md", "r") as file:
#     text = file.read()

# with open("policy.md", "r") as file:
#     text += file.read()

text = ""

pdf_obj = open("BR.pdf", "rb")
pdf_reader = PdfReader(pdf_obj)
for page in pdf_reader.pages:
    text += page.extract_text()


pdf_obj = open("policy.pdf", "rb")
pdf_reader = PdfReader(pdf_obj)
for page in pdf_reader.pages:
    text += page.extract_text()

"""
# Ejemplo con ppt
from langchain.document_loaders import UnstructuredPowerPointLoader
loader = UnstructuredPowerPointLoader("calidad.pptx")

text = loader.load()
text = text[0].page_content
"""

#print("text", text)


# print(text[:1000])


# 2. Chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    length_function=len,
)

chunks = text_splitter.split_text(text) 
print("chunks:", len(chunks))
# print(chunks[2])


# 3. Embeddings
from langchain.embeddings import HuggingFaceBgeEmbeddings


"""
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 # 471M
sentence-transformers/paraphrase-multilingual-mpnet-base-v2 # 1.11G
"""
embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# Ejemplo de embedding
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
sentence_embeddings = model.encode("El perro de san roque no tiene rabo")
# print(len(sentence_embeddings)) # dimensiones del embedding
# print(sentence_embeddings)

# Crear embeddings de todo el texto
from langchain.vectorstores import FAISS
knowledge_base = FAISS.from_texts(chunks, embeddings)
#pregunta = "Como se llama el caso de estudio?"
#docs = knowledge_base.similarity_search(pregunta, k=3)
# print("docs:", docs)


import os
os.environ["OPENAI_API_KEY"]

# 4. Preguntar al documento
from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

#llm = ChatOpenAI(model_name="gpt-3.5-turbo")
# llm = ChatOpenAI(model_name="gpt-4-turbo")

llm = ChatOpenAI(model_name="gpt-4o")
chain = load_qa_chain(llm, chain_type="stuff")

pregunta = "Indica qué curvas elípticas se pueden utilizar para firmar certificados con ECDSA?"
# pregunta = input("Ingrese la pregunta: ")
print("pregunta: ", pregunta)

docs = knowledge_base.similarity_search(pregunta, k=3)
respuesta = chain.run(input_documents=docs, question=pregunta)
print(f"Respuesta ChatGPT: {respuesta}")

# 5. Review cost
from langchain.callbacks import get_openai_callback
with get_openai_callback() as cb:
    response = chain.run(input_documents=docs, question=pregunta)
    print(cb)

