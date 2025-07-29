from phi.agent import Agent
from phi.model.groq import Groq
from tools.pdf_reader import PDFReaderToolkit
from tools.summarizer import SummarizerToolkit
from dotenv import load_dotenv
load_dotenv()
import os
 
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")  
#print("loaded key",os.environ["GROQ_API_KEY"])

# Create instance of the toolkit
pdf_toolkit = PDFReaderToolkit()
summarize_toolkit=SummarizerToolkit()
pdf_agent = Agent(
    name="pdf_agent",
    role="Reads PDFs and summarize",
    tools=[pdf_toolkit,summarize_toolkit],
    model=Groq(id="deepseek-r1-distill-llama-70b"),  # or any Groq model
    #markdown=True,
    instructions="""
You are a helpful agent that:
1. Uses `read_pdf` to extract all text from the provided PDF path(Dont Read the title of pdf and draw conclusions from the content).
2. Uses `summarize_text` to extract the most important ideas from the full content.
3. Provide a well-structured summary in bullet points (max 2 lines each).
4. Each bullet point should be meaningful, concise, and informative.
5. Then, show the same data in a markdown-like table format with two columns: Topic and Description.

Respond only with:
📄 Summary:
- Bullet 1
- Bullet 2

📊 Table View:
| Topic | Description |
|-------|-------------|
| ...   | ...         |
""",

)

# You can now run:
#response = pdf_agent.print_response("Read this file in a neat format and summarize: Test_data\Sequence_Rules_EN.pdf")
#print(response)
