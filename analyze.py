import sqlite3
import pandas as pd
import os

DB_PATH = "feedback_log.db"

def run_analysis():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found. Please run the application and provide feedback first.")
        return

    conn = sqlite3.connect(DB_PATH)
    
    # 1. Count total responses (all entries in feedback table)
    total_query = "SELECT COUNT(*) FROM feedback"
    total_responses = pd.read_sql_query(total_query, conn).iloc[0, 0]
    
    # 2. Count negative feedback (feedback_score == -1)
    negative_query = "SELECT COUNT(*) FROM feedback WHERE feedback_score = -1"
    negative_feedback = pd.read_sql_query(negative_query, conn).iloc[0, 0]
    
    # 3. Print Top 3 failed queries (user_input where feedback_score == -1)
    failed_queries_query = "SELECT user_input, agent_response FROM feedback WHERE feedback_score = -1 LIMIT 3"
    failed_queries_df = pd.read_sql_query(failed_queries_query, conn)
    
    print("--- Part A: Drift Monitoring Analysis ---")
    print(f"Total Responses: {total_responses}")
    print(f"Negative Feedback Count: {negative_feedback}")
    print("\nTop 3 Failed Queries:")
    if failed_queries_df.empty:
        print("No failed queries found.")
    else:
        for i, row in failed_queries_df.iterrows():
            print(f"{i+1}. User Input: {row['user_input']}")
            print(f"   Agent Response: {row['agent_response'][:100]}...")
    
    conn.close()

    # Generate a simple report structure for analysis_report.md
    with open("analysis_report.md", "w") as f:
        f.write("# Part A: Analysis Report\n\n")
        f.write(f"- **Total Responses:** {total_responses}\n")
        f.write(f"- **Negative Feedbacks:** {negative_feedback}\n\n")
        f.write("## Top 3 Failed Queries\n")
        if failed_queries_df.empty:
            f.write("No failed queries recorded yet.\n")
        else:
            for i, row in failed_queries_df.iterrows():
                f.write(f"### {i+1}. Query: {row['user_input']}\n")
                f.write(f"**Response:** {row['agent_response']}\n\n")

if __name__ == "__main__":
    run_analysis()
