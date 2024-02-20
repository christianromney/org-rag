from orgstore import OrgModeDocumentStore
collection = "org-rag"
directory = "/Users/christian/Documents/personal/notes/content/roam/"
store = OrgModeDocumentStore(collection=collection, directory=directory)

i, query = 1, ""
print("Enter search query at the prompt or type 'quit' to exit.")
while not query == "quit":
  query = input(f"{i}> ")
  if query == "quit":
    print("Goodbye.")
  else:
    i += 1
    results = store.mmr_search(query)
    for doc in results:
      print(f"file: {doc.metadata['source']}")
      print(f"length: {len(doc.page_content)}")
      print(f"content: {doc.page_content}\n" )
