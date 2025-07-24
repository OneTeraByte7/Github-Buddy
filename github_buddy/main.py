# main.py
from .llm_client import LLMClient
from .prompts import build_readme_prompt, build_license_prompt
import os
import subprocess
import argparse
import git
from dotenv import load_dotenv


load_dotenv()


def generate_project_files(title, description, license_type="MIT", author="Your Name", year=2025):
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise EnvironmentError("❌ Set your LLM_API_KEY as an environment variable or in .env file.")

    client = LLMClient(api_key)

    readme_prompt = build_readme_prompt(title, description)
    license_prompt = build_license_prompt(license_type, author, year)

    readme = client.generate(readme_prompt)
    license_text = client.generate(license_prompt)

    return readme, license_text


def generate_commit_message(llm_client):
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--cached"], stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()

        if not diff_output:
            return None

        prompt = f"""
You're an expert Git assistant.

Here's a git diff of the staged changes:

{diff_output}

Write a concise, conventional commit message (max 1 line) that summarizes the purpose of these changes. Start with one of: feat:, fix:, docs:, chore:, refactor:, test:, or perf:.

Output only the message.
""".strip()

        return llm_client.generate(prompt, max_tokens=50).strip()
    except Exception as e:
        print("⚠️ Failed to generate commit message:", e)
        return None


def should_auto_commit(threshold=10):
    try:
        changed_files = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip().splitlines()
        return len(changed_files) >= threshold
    except Exception as e:
        print("❌ Could not determine change count:", e)
        return False


def auto_commit(llm_client):
    try:
        repo = git.Repo(os.getcwd())
        repo.git.add(A=True)

        message = generate_commit_message(llm_client)
        if not message:
            print("⚠️ No staged changes or no meaningful diff. Skipping commit.")
            return

        repo.index.commit(message)
        print(f"✅ Auto-committed: {message}")
    except Exception as e:
        print("❌ Git auto-commit failed:", e)


def handle_rml():
    print("📁 GitHub Buddy - AI README & LICENSE Generator\n")

    title = input("🔤 Enter Project Title: ").strip()
    if not title:
        print("❌ Title is required.")
        exit(1)

    description = input("📝 Enter Project Description (optional): ").strip()
    license_type = input("📄 License Type (default: MIT): ").strip() or "MIT"
    author = input("👤 Author Name (default: Your Name): ").strip() or "Your Name"

    readme_md, license_txt = generate_project_files(title, description, license_type, author)

    with open("README.md", "w") as f:
        f.write(readme_md)

    with open("LICENSE", "w") as f:
        f.write(license_txt)

    print("✅ Files generated: README.md and LICENSE")

    if should_auto_commit(threshold=2):
        client = LLMClient(os.getenv("LLM_API_KEY"))
        auto_commit(client)
    else:
        print("ℹ️ Not enough changes to auto-commit.")


def handle_ac():
    client = LLMClient(os.getenv("LLM_API_KEY"))
    if should_auto_commit(threshold=10):
        auto_commit(client)
    else:
        print("ℹ️ Less than 10 changes. Skipping auto-commit.")


def main():
    parser = argparse.ArgumentParser(description="GitHub Buddy CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("rml", help="Generate README.md and LICENSE")
    subparsers.add_parser("ac", help="Auto-commit staged files if enough changes")

    args = parser.parse_args()

    if args.command == "rml":
        handle_rml()
    elif args.command == "ac":
        handle_ac()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
