from phi.agent import Agent
from phi.model.groq import Groq
from tools.pdf_reader import PDFReaderToolkit
from tools.summarizer import SummarizerToolkit
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.youtube_tools import YouTubeTools
from tools.youtube_search import YouTubeSearchToolkit
from pdf_agent import pdfagent
from phi.model.groq import Groq
from phi.model.together import Together
from dotenv import load_dotenv
import os

load_dotenv()
from phi.model.base import Model
from typing import List, Any

#class SimpleFallbackModel(Model):
#    def __init__(self, models: List[Model]):
#        self.models = models
#
#    def response(self, messages: List[dict], **kwargs: Any) -> str:
#        last_error = None
#        for model in self.models:
#            try:
#                return model.response(messages=messages, **kwargs)
#            except Exception as e:
#                print(f"[⚠️ Fallback] {model.__class__.__name__} failed: {e}")
#                last_error = e
#        raise last_error



#model = SimpleFallbackModel(models=[
#    Groq(api_key=os.environ["GROQ_API_KEY"],id="deepseek-r1-distill-llama-70b"),
#    Together(api_key=os.getenv("TOGETHER_API_KEY"), id="mistralai/Mixtral-8x7B-Instruct-v0.1")
#])

#print("loaded key",os.environ["GROQ_API_KEY"])

# Create instances of the toolkits for validation
pdf_toolkit = PDFReaderToolkit()
summarize_toolkit=SummarizerToolkit()
duckduckgo_tool = DuckDuckGo()
#youtube_tool = YouTubeSearchToolkit()
youtube_tools = YouTubeTools() 

# ...existing code...

pdf_agent = Agent(
    name="pdf_agent",
    role="Reads PDFs and summarizes",
    tools=[pdf_toolkit, summarize_toolkit],
    model=Together(api_key=os.getenv("TOGETHER_API_KEY"), id="mistralai/Mixtral-8x7B-Instruct-v0.1"),
    instructions="""
You are a helpful agent that:
- First, use the read_pdf tool to extract text from a PDF file: read_pdf(path="...")
- Then, use the summarize_text tool to summarize the extracted text: summarize_text(text="...", max_length=1000)
- Use plain language and avoid Markdown or special formatting.
always fromat your points in a numbered way, example:
1.point1,
2.point2,
3...
Example workflow:
1. Extract text: read_pdf(path")
2. Summarize: summarize_text(text="(extracted text here)", max_length=1000)
""",
)

Web_search_agent = Agent(
    name="web search agent",
    role="Give additional and related information about the content and provide YouTube links and summaries.",
    tools=[duckduckgo_tool, youtube_tools],
    model=Together(api_key=os.getenv("TOGETHER_API_KEY"), id="mistralai/Mixtral-8x7B-Instruct-v0.1"),
    instructions="""
Give additional information about the topic in a bullet-wise format.
Use the duckduckgo_tool for web search and youtube_search for YouTube video links.
Respond in plain text, using "numbers" for bullet points.
example of format:
1.point1,
2.point2,
3...

Example tool call:
duckduckgo_tool(query="your search query")
search_youtube(query="your search query")
""",
)

Multiagent = Agent(
    team=[pdf_agent, Web_search_agent],
    model=Together(api_key=os.getenv("TOGETHER_API_KEY"), id="mistralai/Mixtral-8x7B-Instruct-v0.1"),
    instructions="""
You are a helpful study assistant.
- When given a PDF file path, use the read_pdf tool to extract its text.
- Summarize the extracted text using summarize_text.
- Use duckduckgo_tool for related web info and youtube_search for related videos.
- Respond with the summary, additional info, and YouTube links in plain text.
- Respond ONLY with the summary, additional info, and YouTube links in plain text.
- DO NOT describe your process, DO NOT output code, DO NOT explain steps, DO NOT use the words 'task', 'transfer', or 'agent'.
Just give the final results as if you are answering a student.

""",
    show_tool_calls=True,
    markdown=False,
)
# ...existing code...
# ...existing code...
#Multiagent.print_response("Summarize and provide additional information and YouTube links for this file: Test_data\Sequence_Rules_EN.pdf")
# ...existing code...