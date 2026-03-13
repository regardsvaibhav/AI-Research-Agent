import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def plan_research(user_query: str) -> dict:
    """Break down a research query into structured search and analysis tasks."""

    prompt = f"""You are an expert research planner. A researcher has asked:

"{user_query}"

Your job is to create a structured research plan.

Respond ONLY in this exact JSON format, nothing else:
{{
    "main_topic": "core topic in 5 words or less",
    "search_queries": [
        "specific arxiv search query 1",
        "specific arxiv search query 2",
        "specific arxiv search query 3"
    ],
    "key_aspects": [
        "aspect 1 to focus on",
        "aspect 2 to focus on",
        "aspect 3 to focus on"
    ],
    "expected_outcome": "what this research should produce in one sentence"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )

    content = response.choices[0].message.content

    # Parse JSON response
    try:
        # Clean response in case model adds extra text
        start = content.find("{")
        end = content.rfind("}") + 1
        json_str = content[start:end]
        plan = json.loads(json_str)
    except Exception:
        # Fallback if JSON parsing fails
        plan = {
            "main_topic": user_query[:50],
            "search_queries": [user_query],
            "key_aspects": ["methodology", "results", "applications"],
            "expected_outcome": "Research ideas and experiment plans"
        }

    return plan


if __name__ == "__main__":
    query = "How can federated learning be applied to EV battery monitoring?"
    
    print("🧠 Planning research...")
    plan = plan_research(query)
    
    print(f"\n📋 RESEARCH PLAN")
    print(f"{'='*50}")
    print(f"Topic: {plan['main_topic']}")
    print(f"\n🔍 Search Queries:")
    for q in plan['search_queries']:
        print(f"  • {q}")
    print(f"\n🎯 Key Aspects:")
    for a in plan['key_aspects']:
        print(f"  • {a}")
    print(f"\n🎯 Expected Outcome: {plan['expected_outcome']}")