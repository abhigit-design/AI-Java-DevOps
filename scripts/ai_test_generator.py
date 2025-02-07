import openai
import os
import sys

# Load API Key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tests():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Add repo_root to the Python path so pytest can find app.py
    sys.path.append(repo_root)
    
    # Construct the full path to app.py
    app_file_path = os.path.join(repo_root, "app.py")

    # Open the file
    with open(app_file_path, "r") as f:
        code_snippet = f.read()

    # Update the prompt to generate only pytest test code without extra text
    prompt = f"Generate unit tests for this Python code using pytest. Do not include any additional explanation or comments, only the test code. Ensure the test imports the functions correctly from 'app.py':\n{code_snippet}"

    # Request the test code from OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )

    # Extract the generated test code
    test_code = response.choices[0].message.content.strip()  # Clean any extra whitespace or unwanted text

    # Clean up any markdown formatting or non-Python syntax (like ```python)
    test_code = test_code.replace("```python", "").replace("```", "").strip()

    # Replace 'your_module' with 'app'
    test_code = test_code.replace("your_module", "app")

    tests_dir = os.path.join(repo_root, 'tests')
    os.makedirs(tests_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Save the test code to a file
    with open(os.path.join(tests_dir, "test_app.py"), "w") as f:
        f.write(test_code)

    print("AI-Generated Unit Tests:\n", test_code)

if __name__ == "__main__":
    generate_tests()
