import openai
import os

# Load API Key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def review_code():
    # Get the absolute path of the repository root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construct the full path to app.py
    app_file_path = os.path.join(repo_root, "HelloWorld.java")

    # Open the file
    with open(app_file_path, "r") as f:
        code_snippet = f.read()
    
    # Uses AI to review the quality and security of the code
    prompt = f"""
    Review the following Python code for security vulnerabilities, performance optimizations, and best practices:
    ```
    {code_snippet}
    ```
    Provide suggestions in bullet points.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a java code reviewer."},
                  {"role": "user", "content": prompt}]
    )
    review_feedback = response.choices[0].message.content
    # Ensure the reports directory exists
    reports_dir = os.path.join(repo_root, 'reports')
    os.makedirs(reports_dir, exist_ok=True)  # This will create the directory if it doesn't exist

    # Write feedback to file
    with open(os.path.join(reports_dir, "code_review.txt"), "w") as f:
        f.write(review_feedback)

    print("✅ AI Code Review Completed! Report saved to reports/code_review.txt")

if __name__ == "__main__":
    review_code()
