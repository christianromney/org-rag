from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredOrgModeLoader
directory = "/Users/christian/Documents/personal/notes/content/roam/"
loader = DirectoryLoader(directory, glob="**/*.org", use_multithreading=True,
                         loader_cls=UnstructuredOrgModeLoader)
documents = loader.load()
print(f"Loaded {len(documents)} org-mode documents.")

from langchain.text_splitter import NLTKTextSplitter
splitter = NLTKTextSplitter(chunk_size=1000, chunk_overlap=30)
chunks = splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks.")

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
collection = "org-rag"
embeddings = OllamaEmbeddings(model="mixtral:latest", show_progress=True)
db = Chroma(embedding=embeddings, collection_name="org-rag",
            persist_directory=f"{directory}/.chroma")
db.add_documents(chunks)
