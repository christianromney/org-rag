from orgstore import OrgModeDocumentStore
collection = "org-rag"
directory = "/Users/christian/Documents/personal/notes/content/roam/"
store = OrgModeDocumentStore(collection=collection, directory=directory)
document_ids = store.create_index()
data = zip(document_ids, store.documents)
for id, doc in data:
  print(f"{id}: {doc.metadata['source']}")
