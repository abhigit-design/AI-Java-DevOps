import openai
import os
import json

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_security():
    # Path to the Snyk security scan report
    security_scan_report = os.path.join(os.getcwd(), "snyk-report", "snyk-report.json")

    # Read the security scan report
    try:
        with open(security_scan_report, "r") as f:
            report_data = json.load(f)  # Assuming the report is in JSON format
    except FileNotFoundError:
        print(f"⚠️ Report {security_scan_report} not found.")
        return

    # Send the report data to AI for analysis
    prompt = f"""
    You are an AI security analyst. Below is a security scan report for a Java project. Please analyze the findings and provide recommendations for mitigating the vulnerabilities, along with any critical security flaws in the dependencies or code.
    
    Report Data: {report_data}
    
    Provide your security recommendations.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )

    security_feedback = response.choices[0].message.content.strip()

    # Print the AI security feedback
    print("AI Security Feedback:\n", security_feedback)

if __name__ == "__main__":
    analyze_security()
