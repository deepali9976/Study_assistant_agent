from phi.tools import Toolkit
from typing import Optional
from phi.utils.log import logger
from groq import Groq  # assuming you're using Groq model

class SummarizerToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="summarizer_tools")
        self.register(self.summarize_text)

    def summarize_text(self, text: str, max_length: Optional[int] = 500) -> str:
        """Summarizes input text."""
        logger.info("Summarizing text...")

        if len(text) > max_length * 2:
            text = text[:max_length * 2]  # truncate long input

        # You can replace this with your LLM call
        return f"This is a summarized version of the content:\n\n{text[:max_length]}..."
