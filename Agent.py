from phi.agent import Agent
from phi.model.groq import Groq
from tools.pdf_reader import PDFReaderToolkit
from tools.summarizer import SummarizerToolkit
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.youtube_tools import YouTubeTools
from tools.youtube_search import YouTubeChannelToolkit
from dotenv import load_dotenv
load_dotenv()

pdf_toolkit = PDFReaderToolkit()
summarize_toolkit = SummarizerToolkit()
duckduckgo_tool = DuckDuckGo()
youtube_tools = YouTubeTools() 
channel_tool =YouTubeChannelToolkit()

Multiagent = Agent(
    tools=[pdf_toolkit, summarize_toolkit, duckduckgo_tool, youtube_tools, channel_tool],
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    instructions="""
You are a helpful study assistant.
- Always prioritize the user's latest question, and try to answer it in detail using the PDF content and online tools if needed.
- Use the read_pdf tool on the provided path to extract content.
- Use summarize_text if asked to summarize.
- If the user asks a question, always answer it based on the PDF first, and if not enough, use duckduckgo_tool and youtube_tools.
- Respond ONLY in plain text and format links as <a href="...">...</a>.
- DO NOT use Markdown or explain your steps. Just be helpful.
- If the user asks for additional information or videos, use duckduckgo_tool, youtube_tools, or channel_tool.- Format all links using <a href="...">...</a>
- Do not use **markdown**, bullet points, or explanation of your process.
- Do not output or describe steps or code. Use "\\n" for line breaks.
-do not use ## for headings or any other formatting.
""",
    show_tool_calls=True,
    markdown=False,
)
#Multiagent.print_response("Summarize and provide additional information and YouTube videos and channel links for this file: Test_data\Sequence_Rules_EN.pdf")