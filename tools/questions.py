from phi.tools import Toolkit
from phi.utils.log import logger
from tools.pdf_reader import extract_text_from_pdf
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm import LLM

class FollowUpQuestionToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="followup_chat_toolkit")
        self.register(self.answer_followup_question)

        def answer_followup_question(question: str, pdf_path: str) -> str:
            # Step 1: Extract PDF content
            pdf_text = extract_text_from_pdf(pdf_path)

            # Step 2: Web search for extra info
            web_snippets = DuckDuckGo().search(question)[:2]  # only top 2 results
            web_text = "\n".join([r.text for r in web_snippets])

            # Step 3: Prompt the model
            prompt = f"""
Use the PDF content and web info to answer the question clearly.

PDF content:
{pdf_text[:8000]}

Web info:
{web_text}

Question: {question}

Answer:
"""
            return LLM().complete(prompt)
