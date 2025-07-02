from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain.vectorstores.chroma import Chroma

from .get_embedding_function import get_embedding_function, get_embedding_function_ollama

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based on the context provided:

{context}

---

Answer the question based on the above context: {question}
"""

QUERY_PROMPT = """
Are the following sentences talking about the same topic?

Sentence 1: {sentence_1}

Sentence 2: {sentence_2}

If they are, output "True". If they are not, output "False"
"""

query_prompt_template = ChatPromptTemplate.from_template(QUERY_PROMPT)

class RAG:
    def __init__(self):
        pass

    def query_data(self, query_text: str):
        assert query_text is not None, "Query text is required."
        return self.query_rag(query_text)

    def query_batch_data(self, query_text_arr: list[str]) -> list[bool]:
        assert query_text_arr is not None, "Queries are required."
        assert len(query_text_arr) > 0, "Queies are required."
        predictions = []
        for i, query in enumerate(query_text_arr):
            if i == 0:
                continue
            sentence_1 = query_text_arr[i - 1]
            sentence_2 = query
            prompt = query_prompt_template.format(sentence_1=sentence_1, sentence_2=sentence_2)
            predictions.append(self.query_rag(prompt))
        return predictions

    def query_rag(self, query_text: str):
        # Prepare the DB.
        # embedding_function = get_embedding_function()
        embedding_function = get_embedding_function_ollama()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=5)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        model = Ollama(model="mistral")
        response_text = model.invoke(prompt)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        # formatted_response = f"Response: {response_text}\nSources: {sources}"
        return bool(response_text)
    