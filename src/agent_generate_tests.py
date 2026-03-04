import anthropic
import os

def generate_tests(source_file: str, output_file: str):
    with open(source_file, "r") as f:
        source_code = f.read()

    print(f"🤖 AI Agent reading {source_file}...")

    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": f"""You are a Python testing expert.

Read the following Python source code and generate comprehensive pytest unit tests for it.

Rules:
- Use pytest style (no unittest classes)
- Cover normal cases, edge cases, and error/exception cases
- Use descriptive test function names
- Only output raw Python code, no markdown, no explanation

Source code:
{source_code}
"""
            }
        ]
    )

    generated_tests = response.content[0].text

    with open(output_file, "w") as f:
        f.write(generated_tests)

    print(f"✅ Tests written to {output_file}")

if __name__ == "__main__":
    generate_tests("src/calculator.py", "tests/test_calculator.py")