#!/usr/bin/env python

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


# 1. Leer Documento

# Markdown
# text = ""
# with open("BR.md", "r") as file:
#     text = file.read()

# with open("policy.md", "r") as file:
#     text += file.read()

text = ""

# PDF
# from PyPDF2 import PdfReader
# pdf_obj = open("BR.pdf", "rb")
# pdf_reader = PdfReader(pdf_obj)
# for page in pdf_reader.pages:
#     text += page.extract_text()
# pdf_obj = open("policy.pdf", "rb")
# pdf_reader = PdfReader(pdf_obj)
# for page in pdf_reader.pages:
#     text += page.extract_text()

# Markdown
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document

loader = UnstructuredMarkdownLoader("BR.md")
data = loader.load()
text += data[0].page_content

loader = UnstructuredMarkdownLoader("policy.md")
data = loader.load()
text += data[0].page_content

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
# from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


"""
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 # 471M
sentence-transformers/paraphrase-multilingual-mpnet-base-v2 # 1.11G
"""
embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# Crear embeddings de todo el texto
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS

knowledge_base = FAISS.from_texts(chunks, embeddings)


import os
os.environ["OPENAI_API_KEY"]

# 4. Preguntar al documento
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

# llm = ChatOpenAI(model_name="gpt-3.5-turbo")
# llm = ChatOpenAI(model_name="gpt-4-turbo")
llm = ChatOpenAI(model_name="gpt-4o", temperature=1)

chain = load_qa_chain(llm, chain_type="stuff")

while True:
    # pregunta = "Indica qué curvas elípticas se pueden utilizar para firmar certificados con ECDSA?"
    pregunta = "cuales son las curvas elipticas que se pueden usar para firmar certificados con ECDSA?"
    # pregunta = "Tell which elliptic curves can be used to sign certificates with ECDSA?"
    # pregunta = "What elliptic curve algorithms can be used in certificate chains according to the CA/Browser Forum’s Baseline Requirements for the Issuance and Management of Publicly-Trusted TLS Server Certificates and the Mozilla Root Store Policy?"
    pregunta = input("Ingrese la pregunta: ")
    print("Pregunta: ", pregunta)

    # docs = knowledge_base.similarity_search(pregunta, k=3)
    docs = knowledge_base.similarity_search(pregunta) # k default is 20


    # 5. Respuesta
    respuesta = chain.run(input_documents=docs, question=pregunta)
    print(f"Respuesta: {respuesta}")
    print("="*15)

    # 6. Review cost
    #from langchain.callbacks import get_openai_callback
    #with get_openai_callback() as cb:
    #    response = chain.run(input_documents=docs, question=pregunta)
    #    print(cb)

