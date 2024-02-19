from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

collection = "org-rag"
directory =  "/Users/christian/Documents/personal/notes/content/roam/"
index = f"{directory}/.chroma"

embeddings = OllamaEmbeddings(model="mixtral:latest")
db = Chroma("org-rag", embeddings, persist_directory=index)

query = input("user> ")
results = db.search(query, "mmr", fetch_k=10, lambda_mult=0.75)

for doc in results:
    print("*" * 80)
    print(f"file: {doc.metadata['source']}, length: {len(doc.page_content)}")
    print(f"content: {doc.page_content}\n\n" )
