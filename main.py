import os
import traceback

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# Import project modules
# --------------------------------------------------

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(title="EduGenie.AI")

# --------------------------------------------------
# Base directory
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# --------------------------------------------------
# Check required folders
# --------------------------------------------------

if not os.path.isdir(STATIC_DIR):
    print(f"WARNING: Static folder not found: {STATIC_DIR}")

if not os.path.isdir(TEMPLATES_DIR):
    print(f"WARNING: Templates folder not found: {TEMPLATES_DIR}")

# --------------------------------------------------
# Static files
# --------------------------------------------------

if os.path.isdir(STATIC_DIR):
    app.mount(
        "/static",
        StaticFiles(directory=STATIC_DIR),
        name="static"
    )

# --------------------------------------------------
# Templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory=TEMPLATES_DIR
)

# --------------------------------------------------
# Request model
# --------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request}
        )

    except Exception as e:
        print("\n========== HOME ERROR ==========")
        traceback.print_exc()
        print("================================\n")

        return HTMLResponse(
            content=f"""
            <h1>EduGenie Server Error</h1>
            <p>Could not load index.html.</p>
            <pre>{TEMPLATES_DIR}\\index.html</pre>
            <hr>
            <h3>Error:</h3>
            <pre>{str(e)}</pre>
            """,
            status_code=500
        )

# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "running",
        "gemini_configured": bool(
            os.getenv("GEMINI_API_KEY")
        ),
        "static_folder_exists": os.path.isdir(STATIC_DIR),
        "templates_folder_exists": os.path.isdir(TEMPLATES_DIR),
        "index_file_exists": os.path.isfile(
            os.path.join(TEMPLATES_DIR, "index.html")
        )
    }


# --------------------------------------------------
# Question Answering
# --------------------------------------------------

@app.post("/qa")
async def qa(request: TextRequest):

    try:

        result = answer_question(
            request.text,
            request.level
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        print("\n========== QA ERROR ==========")
        traceback.print_exc()
        print("==============================\n")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


# --------------------------------------------------
# Explanation
# --------------------------------------------------

@app.post("/explain")
async def explain(request: TextRequest):

    try:

        result = explain_topic(
            request.text,
            request.level
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        print("\n========== EXPLAIN ERROR ==========")
        traceback.print_exc()
        print("===================================\n")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


# --------------------------------------------------
# Quiz
# --------------------------------------------------

@app.post("/quiz")
async def quiz(request: TextRequest):

    try:

        result = generate_quiz(
            request.text,
            request.level
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        print("\n========== QUIZ ERROR ==========")
        traceback.print_exc()
        print("================================\n")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


# --------------------------------------------------
# Summary
# --------------------------------------------------

@app.post("/summarize")
async def summarize(request: TextRequest):

    try:

        result = summarize_text(
            request.text,
            request.level
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        print("\n========== SUMMARY ERROR ==========")
        traceback.print_exc()
        print("===================================\n")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


# --------------------------------------------------
# Learning recommendations
# --------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    request: TextRequest
):

    try:

        result = get_learning_recommendations(
            request.text,
            request.level
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        print("\n========== LEARNING PATH ERROR ==========")
        traceback.print_exc()
        print("=========================================\n")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


# --------------------------------------------------
# Global exception handler
# --------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    print("\n========================================")
    print("GLOBAL SERVER ERROR")
    print("URL:", request.url)
    print("METHOD:", request.method)
    print("ERROR:", str(exc))
    print("========================================")

    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "message": "Internal server error. Check the terminal for the full traceback."
        }
    )