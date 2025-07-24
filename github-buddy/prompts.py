# prompts.py

def build_readme_prompt(title: str, description: str = "") -> str:
    return f"""
You are an AI assistant generating README.md content in valid Markdown format.

Project Title: {title}
Project Description: {description or "No description provided."}

Include these sections in the README:
- Title
- Description
- Installation
- Usage
- Features
- License

Output only the README.md content in Markdown format.
""".strip()


def build_license_prompt(license_type: str = "MIT", author: str = "Your Name", year: int = 2025) -> str:
    return f"""
Generate the full text of the {license_type} license.
Set author as "{author}" and year as {year}.

Output only the plain license text, no extra commentary.
""".strip()
