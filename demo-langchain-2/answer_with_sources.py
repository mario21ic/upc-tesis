from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader, WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

brs_as_markdown_url = "https://raw.githubusercontent.com/cabforum/servercert/main/docs/BR.md"
mozilla_policy_url = "https://raw.githubusercontent.com/mozilla/pkipolicy/master/rootstore/policy.md"
loader = WebBaseLoader([brs_as_markdown_url, mozilla_policy_url])
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500)
texts = text_splitter.split_documents(documents)
for i, text in enumerate(texts):
    text.metadata["source"] = f"{i}-pl"
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

from langchain.chains import create_qa_with_sources_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-4o")

qa_chain = create_qa_with_sources_chain(llm)

doc_prompt = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)

final_qa_chain = StuffDocumentsChain(
    llm_chain=qa_chain,
    document_variable_name="context",
    document_prompt=doc_prompt,
)

retrieval_qa = RetrievalQA(
    retriever=docsearch.as_retriever(), combine_documents_chain=final_qa_chain
)

query = "What are the allowed ECDSA elliptic curves?"

json_string = retrieval_qa.run(query)

# Parse `json_string`
import json
data = json.loads(json_string)
print("Answer: " + data["answer"])

# Iterate over the sources
for source in data["sources"]:
    # Search in `texts` for the source
    for text in texts:
        if text.metadata["source"] == source:
            print("\n#######################")
            print("Source (" + source + "):")
            print(text.page_content)
            print("#######################")
            # break

