# main.py

from llm_client import LLMClient
from prompts import build_readme_prompt, build_license_prompt
import os
from dotenv import load_dotenv
load_dotenv()


def generate_project_files(title, description, license_type="MIT", author="Your Name", year=2025):
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise EnvironmentError("❌ Set your LLM_API_KEY as an environment variable.")

    client = LLMClient(api_key)

    readme_prompt = build_readme_prompt(title, description)
    license_prompt = build_license_prompt(license_type, author, year)

    readme = client.generate(readme_prompt)
    license_text = client.generate(license_prompt)

    return readme, license_text

if __name__ == "__main__":
    print("📦 GitHub Buddy - AI README & LICENSE Generator\n")

    title = input("🔤 Enter Project Title: ").strip()
    if not title:
        print("❌ Title is required.")
        exit(1)

    description = input("📝 Enter Project Description (optional): ").strip()
    license_type = input("📄 License Type (default: MIT): ").strip() or "MIT"
    author = input("👤 Author Name (default: Your Name): ").strip() or "Your Name"

    readme_md, license_txt = generate_project_files(
        title, description, license_type, author
    )

    with open("README.md", "w") as f:
        f.write(readme_md)

    with open("LICENSE", "w") as f:
        f.write(license_txt)

    print("\n✅ Files generated: README.md and LICENSE")
