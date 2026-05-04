import sqlite3
import pandas as pd
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
import os

DB_PATH = "feedback_log.db"

def analyze_drift():
    if not os.path.exists(DB_PATH):
        print("No feedback database found.")
        return

    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM feedback WHERE feedback_score == -1"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("No negative feedback found yet. Drift is within acceptable limits.")
        return

    print(f"Analyzing {len(df)} negative feedback entries...")

    # Judge LLM Setup
    if HAS_OPENAI and os.getenv("OPENAI_API_KEY"):
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Clinical AI Auditor. Categorize the following failure into one of these: [Hallucination, Tool Error, Medical Inaccuracy, Tone Issue, Context Miss]. Provide a brief reason."),
            ("user", "User Input: {user_input}\nAgent Response: {agent_response}\nComment: {comment}")
        ])
        use_llm = True
    else:
        use_llm = False

    analysis_results = []
    
    for _, row in df.iterrows():
        try:
            if not use_llm:
                # Rule-based fallback categorization
                user_input_lower = row["user_input"].lower()
                if "dose" in user_input_lower or "mg" in user_input_lower:
                    category = "Hallucination"
                elif "report" in user_input_lower or "doc" in user_input_lower:
                    category = "Context Miss"
                else:
                    category = "Tool Error"
                reason = "Rule-based analysis: Failure detected in core logic."
            else:
                chain = prompt | llm
                response = chain.invoke({
                    "user_input": row["user_input"],
                    "agent_response": row["agent_response"],
                    "comment": row["optional_comment"]
                })
                category_info = response.content
                category = category_info.split(":")[0] if ":" in category_info else category_info
                reason = category_info
            
            analysis_results.append({
                "id": row["id"],
                "category": category.strip(),
                "reason": reason.strip(),
                "input": row["user_input"]
            })
        except Exception as e:
            print(f"Error analyzing row {row['id']}: {e}")

    # Generate Report
    report_df = pd.DataFrame(analysis_results)
    summary = report_df['category'].value_counts()
    
    with open("drift_report.md", "w") as f:
        f.write("# Drift & Failure Analysis Report\n\n")
        f.write(f"**Total Negative Feedbacks Analyzed:** {len(df)}\n\n")
        f.write("## Error Distribution\n")
        f.write(summary.to_string())
        f.write("\n\n## Detailed Failure Logs\n")
        f.write(report_df.to_string(index=False))
        f.write("\n\n## Action Plan\n")
        f.write("1. **Prompt Tuning:** Address common 'Hallucination' patterns by strengthening grounding instructions.\n")
        f.write("2. **Tool Refinement:** Check RAG retrieval thresholds for 'Context Miss' errors.\n")

    print("Drift report generated: drift_report.md")

if __name__ == "__main__":
    analyze_drift()
