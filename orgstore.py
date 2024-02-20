from langchain_community.document_loaders import DirectoryLoader, UnstructuredOrgModeLoader
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

class OrgModeDocumentStore:
  def __init__(self, collection, directory, model="mixtral:latest",
               search_type="mmr", mmr_diversity=0.75,
               num_search_results=5, show_progress=True):
    self.collection = collection
    self.directory = directory
    if not os.path.exists(directory):
      raise RuntimeError(f"Directory {directory} does not exist.")

    self.index_directory = os.path.join(directory, ".chroma")
    if not os.path.exists(self.index_directory):
      os.mkdir(self.index_directory)

    self.loader = DirectoryLoader(directory, glob="**/*.org", use_multithreading=True,
                                  loader_cls=UnstructuredOrgModeLoader)

    self.search_type = search_type
    self.k = num_search_results
    self.diversity = mmr_diversity

    self.model = model
    self.embeddings = OllamaEmbeddings(model=model, show_progress=show_progress)
    self.db = Chroma(collection_name=collection,
                     embedding_function=self.embeddings,
                     persist_directory=self.index_directory)

  def __repr__(self):
    return f"""
    OrgModeDocumentStore(
      collection={self.collection!r},
      directory={self.directory!r},
      index_directory={self.index_directory!r},
      loader={self.loader!r},
      embeddings={self.embeddings!r},
      model={self.model!r},
      db={self.db!r},
      search_type={self.search_type!r},
      k={self.k!r},
      diversity={self.diversity!r}
    )"""

  # indexing management
  def load(self):
    "Loads all org-mode documents found under the given directory recursively."
    self.documents = self.loader.load()

  def chunked_documents(self, overlap=128):
    "Returns the loaded documents split into chunks."
    splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=overlap)
    return splitter.transform_documents(self.documents)

  def add_documents(self, docs):
    "Adds the given docs to the Chroma vectorstore and returns the document ids."
    return self.db.add_documents(docs)

  def update_document(self, id, doc):
    "Updates the single document identified by the id."
    return self.db.update_document(id, doc)

  def update_documents(self, ids, docs):
    "Updates the documents identified by the given ids."
    return self.db.update_documents(ids, docs)

  def create_index(self):
    "Creates the index from the loaded documents. This should only be run once."
    self.load()
    chunks = self.chunked_documents()
    print(f"Indexing {len(chunks)} chunks of {len(self.documents)} documents.")
    return self.add_documents(chunks)

  # query
  def similarity_search(self, query):
    "Search the vectorstore for docs relevant to the query."
    return self.db.similarity_search(query, self.k)

  def mmr_search(self, query):
    return self.db.max_marginal_relevance_search(query, k=self.k, lambda_mult=self.diversity)

  def as_retriever(self):
    "Returns a retriever for this vectorstore."
    return self.db.as_retriever(search_type=self.search_type,
                                search_kwargs={'k': self.k,
                                               'lambda_mult': self.diversity})
