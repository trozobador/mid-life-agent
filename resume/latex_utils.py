import json
import shutil
import subprocess
import os


def render_latex_to_pdf(tex_file_path, output_dir):
    """
    Renders a LaTeX file to PDF using pdflatex.
    Falls back to reportlab if pdflatex is not installed.
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(tex_file_path))[0]

    if shutil.which("pdflatex"):
        try:
            for _ in range(2):
                subprocess.run(
                    ["pdflatex", "-output-directory", output_dir, tex_file_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            for ext in (".aux", ".log", ".out"):
                aux = os.path.join(output_dir, base_name + ext)
                if os.path.exists(aux):
                    os.remove(aux)
            pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
            print(f"PDF generated successfully: {pdf_path}")
            return pdf_path
        except subprocess.CalledProcessError as e:
            print(f"pdflatex error: {e} — falling back to reportlab")

    # Fallback: derive json_path from tex_file location
    tex_dir  = os.path.dirname(os.path.abspath(tex_file_path))
    root_dir = os.path.dirname(tex_dir)          # outputs/<role>/
    json_path = os.path.join(root_dir, "json", "resume.json")
    pdf_path  = os.path.join(output_dir, f"{base_name}.pdf")

    if not os.path.exists(json_path):
        print(f"pdflatex not found and JSON not available at {json_path}")
        return None

    print("pdflatex not found — using reportlab to generate PDF")
    from resume.pdf_reportlab import generate_pdf
    return generate_pdf(json_path, pdf_path)
    
def escape_latex(text):
    """
    Escapes special LaTeX characters in a given string.

    Args:
    text (str): The input string to escape.

    Returns:
    str: The escaped string suitable for LaTeX.
    """
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
    }
    return ''.join(special_chars.get(c, c) for c in text)

