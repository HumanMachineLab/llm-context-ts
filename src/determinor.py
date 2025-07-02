from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_openai import ChatOpenAI
import os

# Load OpenAI API key from environment variable
# You can set this in a .env file or as an environment variable
# Example: OPENAI_API_KEY=your_actual_api_key_here
if 'OPENAI_API_KEY' not in os.environ:
    # Try to load from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # dotenv not installed, that's okay

MAX_CONTEXT_WINDOW = 5

QUERY_PROMPT = """
Given the following paragraph:

{prev_paragraph}

Does the following sentence continue the paragraph?

{sentence}

If it does, output "True". If they are not, output "False". Do not provide any explanation. Ensure your answer is limited to "True" or "False".
"""

MEETING_PROMPT = """
Given the following meeting transcript:

{prev_paragraph}

Does the following sentence continue the same dialogue?

{sentence}

If it does, output "True". If they are not, output "False". Do not provide any explanation. Ensure your answer is limited to "True" or "False".
"""


class Determinor:
    def __init__(self, deepseek=False, openai_4o=False, openai_o1=False, meeting_dataset=False, max_context_window=MAX_CONTEXT_WINDOW):
        self.openai_4o = openai_4o
        self.openai_o1 = openai_o1
        if openai_4o:
            self.model = ChatOpenAI(model="gpt-4o-mini")
        elif openai_o1:
            self.model = ChatOpenAI(model="o1-mini", temperature=1)
        elif deepseek:
            self.model = Ollama(model="deepseek-r1:8b")
        else:
            self.model = Ollama(model="mistral")
        self.prev_paragraph = []
        self.max_context_window = max_context_window
        self.meeting_dataset = meeting_dataset
        
    def query_data(self, sentence_1: str, sentence_2: str):
        assert sentence_1 is not None, "Sentence 1 is required."
        assert sentence_2 is not None, "Sentence 2 is required."
        return self.query(sentence_1, sentence_2)

    def query_batch_data(self, sentences: list[str]) -> list[bool]:
        assert sentences is not None, "Sentences are required."
        assert len(sentences) > 0, "Sentences are required."
        predictions = []
        for sentence in sentences:
            predictions.append(self.query(sentence))
        return predictions
    
    def get_response(self, response):
        if self.openai_4o or self.openai_o1:
            return response.content
        else:
            return response
    
    def query(self, sentence):
        PROMPT = MEETING_PROMPT if self.meeting_dataset else QUERY_PROMPT
        prompt_template = ChatPromptTemplate.from_template(PROMPT)
        # get last self.max_context_window sentences and join them with newlines
        prev_paragraph_str = "\n".join(self.prev_paragraph[-self.max_context_window:])
        
        prompt = prompt_template.format(prev_paragraph=prev_paragraph_str, sentence=sentence)

        response_text = self.model.invoke(prompt)
        response_text = self.get_response(response_text)

        formatted_output = response_text.lower().strip()
        print("." if "true" in formatted_output else "|", end="")

        if "false" in formatted_output:
            # dump the entire previous paragraph and start a new one with the current sentence
            self.prev_paragraph = [sentence]
        else:
            self.prev_paragraph.append(sentence)
        return True if "true" in formatted_output else False
    
    def format_predictions(self, predictions: list[str]) -> list[int]:
        predictions = [p.lower().strip() for p in predictions]
        return [0 if prediction == "True" else 1 for prediction in predictions]