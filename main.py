from fastapi import FastAPI, Request, UploadFile, File ,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil, os
from test import Multiagent  # your agent setup
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
USER_ACTIVITY_LOG = "user_activity.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def log_user_activity(username: str, question: str, filename: str):
    if not os.path.exists(USER_ACTIVITY_LOG):
        with open(USER_ACTIVITY_LOG, "w") as f:
            json.dump({}, f)

    with open(USER_ACTIVITY_LOG, "r+") as f:
        data = json.load(f)
        if username not in data:
            data[username] = []
        data[username].append({"question": question, "filename": filename})
        f.seek(0)
        json.dump(data, f, indent=2)
def get_user_history(username: str):
    if os.path.exists(USER_ACTIVITY_LOG):
        with open(USER_ACTIVITY_LOG, "r") as f:
            data = json.load(f)
            return data.get(username, [])
    return []


@app.get("/", response_class=HTMLResponse)
async def new(request: Request):
    return templates.TemplateResponse("new.html", {"request": request, "result": None})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, pdf_file: UploadFile = File(...), question: str = "",user_name: str = Form(...)):
    # Save the uploaded PDF
    file_path = os.path.join(UPLOAD_DIR, pdf_file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(pdf_file.file, f)

    normalized_path = file_path.replace("\\", "/")
    log_user_activity(user_name, question, pdf_file.filename)

    # Fetch last 3 activities of the user
    history = get_user_history(user_name)
    history_text = "\n".join(
        f"- {entry['question']} (on {entry['filename']})" for entry in history[-3:]
    ) if history else "No prior history."

    # Build prompt using user question
    prompt = (
        f"You are a helpful study assistant.\n"
        f"The user uploading this file is: {user_name}.\n"
        f"The uploaded file is at: '{normalized_path}'.\n"
        f"The user's current question is: '{question}'.\n"
        f"Please answer their question using the content from the PDF.\n"
        f"If needed, use tools to search the web or YouTube.\n"
        f"Respond in plain text only with links in HTML like <a href='...'>Link</a>.\n"
        f"Here is a brief history of this user's past questions:\n{history_text}\n"
        f"Analyse user's behaviour and suggest links/articles.\n"
        f"Then use relevant tools to answer the question clearly and optionally provide helpful links.\n"
        f"Format all links as <a href='...'>Link</a> and avoid Markdown or bold syntax."
    )
    

    result = Multiagent.run(prompt)
    result_text = result.content
    cleaned_result = result_text.replace("**", "")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": cleaned_result,
        "pdf_path": normalized_path
    })
@app.post("/ask", response_class=HTMLResponse)
async def ask_question(
    request: Request,
    pdf_path: str = Form(...),
    question: str = Form(...),
    user_name: str = Form(...)
):
    pdf_path = pdf_path.replace("\\", "/")  # Normalize path

    # Load last 3 questions from this user
    history = get_user_history(user_name)
    history_text = "\n".join(
        f"- {entry['question']} (on {entry['filename']})" for entry in history[-3:]
    ) if history else "No prior history."

    prompt = (
        f"The user is '{user_name}'.\n"
        f"They previously uploaded the file at '{pdf_path}' and now asked: '{question}'.\n"
        f"Recent questions by this user:\n{history_text}\n\n"
        f"Use the read_pdf tool on '{pdf_path}' and provide a helpful answer.\n"
        f"Use other tools like duckduckgo or youtube if needed.\n"
        f"Format links like <a href='...'>Link</a>.\n"
        f"Do not use Markdown or explain the steps."
    )

    result = Multiagent.run(prompt)
    cleaned_result = result.content.replace("**", "")

    # Log this new interaction
    log_user_activity(user_name, question, pdf_path)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": cleaned_result,
        "pdf_path": pdf_path,
        "user_name": user_name
    })
