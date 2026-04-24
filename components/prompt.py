from langchain_core.prompts import PromptTemplate

def get_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a business assistant for Nexora Technologies.

Answer ONLY from the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Provide a clear answer with source reference.
"""
    )