from phi.agent import Agent
from phi.model.groq import Groq
#from tools.pdf_reader import PDFReaderToolkit
#from tools.summarizer import SummarizerToolkit
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.youtube_tools import YouTubeTools
from tools.youtube_search import YouTubeChannelToolkit

from phi.model.together import Together
from dotenv import load_dotenv
import os
duckduckgo_tool = DuckDuckGo()
#youtube_tool = YouTubeSearchToolkit()
youtube_tools = YouTubeTools() 
channel_tools= YouTubeChannelToolkit()
load_dotenv()
web_search_agent = Agent(
    name="web_search_agent",
    role="Research assistant that finds related web and video content and youtube channels for a given topic.",
    tools=[duckduckgo_tool, youtube_tools,channel_tools],
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    instructions="""
Given a topic or concept, your job is to:
1. Use duckduckgo_tool to find 2 to 3 useful web articles.
2. Use youtube_search(query="...") to find 1to2 relevant YouTube videos.
3. Use channel_tools to find related channels.
4. Use search_channels(query="...") to find YouTube channels.
You must decide what queries to search based on the topic .

Return your final answer in this format:
- Summary of topic
- Related web links (with 1-sentence descriptions)
- YouTube links (with brief summaries)
- YouTube channel links (with brief summaries)
- Provide additional information or insights that you find relevant.
Do not describe what you are doing. Only return the final output to the user.
""",
    show_tool_calls=True,
    markdown=True
)
Debug = True

#web_search_agent.print_response("Summarize and provide additional information and YouTube vidoes and youtube channel links for this ""Generative AI"" topic.")
