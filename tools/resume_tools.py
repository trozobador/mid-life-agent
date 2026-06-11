import json
import os
from typing import Union
import sys
from crewai.tools import tool

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume.generator import generate
from tools.tools_utils import count_pages_and_lines, generate_comparison_pdf


def _output_dir() -> str:
    return os.getenv("RESUME_OUTPUT_DIR", "outputs")


@tool("save_resume_json")
def save_resume_json(resume_data: Union[str, dict]) -> str:
    """
    Saves the provided resume data as JSON to the current profile's output directory.

    Args:
    resume_data (Union[str, dict]): A JSON string or Python dict with resume data.

    Returns:
    str: Success or error message.
    """
    try:
        if isinstance(resume_data, str):
            resume_json = json.loads(resume_data)
        elif isinstance(resume_data, dict):
            resume_json = resume_data
        else:
            return "Error: Input must be a JSON string or a Python dictionary."

        path = os.path.join(_output_dir(), "json", "resume.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(resume_json, f, indent=2)
        return f"Resume JSON successfully saved to '{path}'."
    except json.JSONDecodeError:
        return "Error: The provided string data is not valid JSON."
    except IOError as e:
        return f"Error: Unable to write file. {e}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"


@tool("generate_resume")
def generate_resume_tool(resume_content: str) -> str:
    """
    Generates a LaTeX document from the saved resume JSON and converts it to PDF.

    Args:
    resume_content (str): Ignored — reads from the saved JSON in the output directory.

    Returns:
    str: Confirmation message.
    """
    output_dir = _output_dir()
    json_path = os.path.join(output_dir, "json", "resume.json")
    latex_path = os.path.join(output_dir, "latex", "output_resume.tex")
    pdf_dir = os.path.join(output_dir, "pdf")

    os.makedirs(os.path.dirname(latex_path), exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)

    generate(json_path=json_path, latex_path=latex_path, pdf_dir=pdf_dir)
    pdf_path = os.path.join(pdf_dir, "output_resume.pdf")

    try:
        from tools.tools_utils import count_pages_and_lines
        pages, extra_lines = count_pages_and_lines(pdf_path)
        if pages == 2:
            page_feedback = f"Page count: 2 pages — fits perfectly. No changes needed."
        elif pages == 1:
            page_feedback = "Page count: 1 page — too short. Expand work experiences and highlights to fill 2 pages."
        else:
            page_feedback = f"Page count: {pages} pages — too long, needs trimming to fit within 2 pages."
    except Exception:
        page_feedback = "Page count check skipped."

    return f"Resume generated: {pdf_path}. {page_feedback}"


generate_resume_tool.cache_function = lambda *_: False


@tool("line count on extra page")
def pgcount_tool(pdf_path: str) -> str:
    """
    Counts the number of pages and extra lines on the last page of a PDF.

    Args:
    pdf_path (str): Path to the generated resume PDF file (ignored — always reads the
                    output_resume.pdf from the current output directory).

    Returns:
    str: Page count and line count feedback.
    """
    resolved_path = os.path.join(_output_dir(), "pdf", "output_resume.pdf")

    if not os.path.exists(resolved_path):
        return "PDF not found. Run generate_resume first, then call this tool."

    print(f"Counting pages from: {resolved_path}")
    try:
        pages, extra_lines = count_pages_and_lines(resolved_path)

        if pages == 2:
            return "The resume fits on 2 pages perfectly. No changes needed."
        elif pages == 1:
            return "The resume is only 1 page — too short. Expand work experiences and highlights to fill 2 pages."
        elif pages > 2:
            return (
                f"The resume is {pages} pages long. "
                "Please remove less relevant work experiences to make it fit within two pages."
            )
        else:
            return "Error: Unable to determine page count."
    except Exception as e:
        return f"Error: {str(e)}"


@tool("pdf_comparison_tool")
def pdf_comparison_tool(pdf_file1: str, pdf_file2: str, output_pdf: str) -> str:
    """
    Generates a side-by-side comparison PDF of two resume PDFs.

    Args:
    pdf_file1 (str): Path to the first PDF file.
    pdf_file2 (str): Path to the second PDF file.
    output_pdf (str): Path where the comparison PDF will be saved.

    Returns:
    str: Result message.
    """
    try:
        generate_comparison_pdf(pdf_file1, pdf_file2, output_pdf)
        return f"Comparison PDF successfully generated and saved to {output_pdf}"
    except Exception as e:
        return f"Error generating comparison PDF: {str(e)}"


@tool("save_interview_prep")
def save_interview_prep_tool(content: str) -> str:
    """
    Saves the interview preparation guide as a Markdown file in the output directory.

    Args:
    content (str): The full interview preparation guide in Markdown format.

    Returns:
    str: Success or error message.
    """
    try:
        path = os.path.join(_output_dir(), "interview_prep.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Interview preparation guide saved to '{path}'."
    except Exception as e:
        return f"Error saving interview prep guide: {str(e)}"
