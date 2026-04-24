def retrieve_docs(db, query, k=3):
    return db.similarity_search(query, k=k)