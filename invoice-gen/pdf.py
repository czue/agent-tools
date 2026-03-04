from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright


TEMPLATES_DIR = Path(__file__).parent / "templates"


def render_invoice_html(context: dict) -> str:
    """Render the invoice HTML template with the given context."""
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("invoice.html")
    return template.render(**context)


def generate_pdf(html: str, output_path: Path) -> Path:
    """Convert HTML string to PDF using Playwright."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        page.pdf(path=str(output_path), format="A4", print_background=True)
        browser.close()
    return output_path
