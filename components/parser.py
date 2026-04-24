def format_output(answer, docs):
    sources = []
    for doc in docs:
        page = doc.metadata.get("page", "N/A")
        sources.append(f"Page {page}")

    return {
        "answer": answer,
        "sources": list(set(sources))
    }