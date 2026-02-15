import json
import httpx
import time

# Questions derived from handbook_content.md
# ... (rest of the file remains similar but using httpx)
QUESTIONS = [
    "What is the effective date of this employee handbook?",
    "Who must the handbook be returned to upon termination of service?",
    "What language prevails if there is a dispute in the translation of the handbook?",
    "What are some examples of sexual harassment mentioned in the Code of Conduct?",
    "Are employees allowed to accept gifts from business partners?",
    "What should an employee do if they want to report improper conduct (whistleblowing)?",
    "What is the consequence of being absent for more than two consecutive working days without notification?",
    "What is the minimum hiring age specified in the handbook?",
    "How is the hiring of employees post-retirement age handled?",
    "Who must approve all requisitions for additional headcount?",
    "Is headcount approval required for replacement roles?",
    "Can former employees be re-employed if they were dismissed for misconduct?",
    "What is the cooling period required before a former employee can be considered for re-employment?",
    "How many candidate profiles must HR provide to the hiring manager for a role?",
    "What is the mandatory background screening requirement for successful candidates?",
    "How many professional references are required for a candidate?",
    "What is the incentive for referring a successful candidate for a Managerial role?",
    "Are local employees given priority over expatriates for vacancies?",
    "Is the hiring of family members permitted in the same department?",
    "What happens if an employee conceals the hiring of a family member?",
    "What are the criteria for the company to accept academic qualifications?",
    "What is the consequence of providing false information during hiring?",
    "What happens if a new employee fails to complete the onboarding programme?",
    "How must an employee notify the company of their intention to resign?",
    "What is required of a resigning employee on their last day regarding company property?",
    "When is the final wage paid to a resigning employee?",
    "What is the retirement age specified in the handbook?",
    "How many days of annual leave is an employee with 3 years of service entitled to?",
    "How many days in advance must an employee submit a leave request?",
    "How many days of unutilised annual leave can be carried forward to the next year?"
]

def test_retrieval():
    url = "http://localhost:8000/chat/blocking"
    results = []
    
    print(f"Starting retrieval test with {len(QUESTIONS)} questions...")
    
    for i, q in enumerate(QUESTIONS):
        print(f"[{i+1}/30] Asking: {q}")
        payload = {
            "question": q,
            "history": []
        }
        try:
            start_time = time.time()
            with httpx.Client() as client:
                response = client.post(url, json=payload, timeout=30.0)
            end_time = time.time()
            
            print(f"DEBUG: Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    answer = response.json().get("answer", "No answer field")
                    results.append({
                        "question": q,
                        "answer": answer,
                        "latency": f"{end_time - start_time:.2f}s",
                        "status": "PASS"
                    })
                except Exception as json_err:
                    print(f"DEBUG: JSON Error: {json_err}")
                    print(f"DEBUG: Raw Content: {response.content[:200]}")
                    results.append({
                        "question": q,
                        "error": f"JSON Decode Error: {json_err}",
                        "raw_content": response.text[:500],
                        "status": "FAIL"
                    })
            else:
                results.append({
                    "question": q,
                    "error": f"HTTP {response.status_code}",
                    "raw_content": response.text[:500],
                    "status": "FAIL"
                })
        except Exception as e:
            results.append({
                "question": q,
                "error": str(e),
                "status": "ERROR"
            })
    
    with open("retrieval_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    print("\nTest Complete. Results saved to retrieval_test_results.json")

if __name__ == "__main__":
    test_retrieval()
