import argparse
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from .get_embedding_function import get_embedding_function, get_embedding_function_ollama

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are a helpful assistant that is skilled at being able to differentiate between sentences in different paragraphs.
Answer the question based on the context provided:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)



def query_data(query_text: str):
    assert query_text is not None, "Query text is required."
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    # embedding_function = get_embedding_function()
    embedding_function = get_embedding_function_ollama()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()
