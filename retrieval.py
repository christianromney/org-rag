from orgstore import OrgModeDocumentStore
collection = "org-rag"
directory = "/Users/christian/Documents/personal/notes/content/roam/"
store = OrgModeDocumentStore(collection=collection, directory=directory, silent_errors=True)

i, query = 1, ""
print("Enter search query at the prompt or type '?list' for docs, or '?quit' to exit.\n")
while not query.lower() == "?quit":
  query = input(f"{i}> ")
  if query == "?quit":
    print("Goodbye.")
  elif query == "?list":
    i += 1
    store.print_documents()
  else:
    i += 1
    #results = store.as_retriever().get_relevant_documents(query)
    #results = store.mmr_search(query)
    results = store.similarity_search(query)
    for doc in results:
      print(f"file: {doc.metadata['source']}, length: {len(doc.page_content)}")
      display = input("Display page content? (y|n)> ")
      if display.lower() == "y":
        print(f"content: {doc.page_content}\n" )
        print("-" * 80)
