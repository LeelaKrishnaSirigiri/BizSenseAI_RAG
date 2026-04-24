from langchain.chat_models import ChatOpenAI

def generate_answer(prompt):
    llm = ChatOpenAI(temperature=0)
    return llm.predict(prompt)
