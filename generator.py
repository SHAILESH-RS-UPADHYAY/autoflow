import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from rag_engine import get_rag_context
from analytics import get_kpis

load_dotenv()

def generate_report():
    """Generates the final markdown report using KPIs, RAG context, and LLM."""
    print("Gathering KPIs...")
    kpis = get_kpis()
    
    print("Retrieving company guidelines from RAG...")
    # Query ChromaDB for relevant company guidelines regarding reports, tone, and goals
    rag_context = get_rag_context("What are the quarterly goals, tone, and guidelines for executive reports?")
    
    print("Generating LLM summary...")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior data analyst and Chief of Staff. Write a concise, actionable executive summary based on the provided data. STRICTLY adhere to the Company Guidelines provided via RAG."),
        ("user", """
Company Guidelines & Past Context (From RAG):
{rag_context}

This Week's KPIs (JSON):
{kpi_data}

Instructions:
1. Output in clean Markdown formatting.
2. Start with a brief high-level overview.
3. Highlight the biggest wins and any red flags according to the company guidelines.
4. Conclude with 1-2 actionable recommendations.
5. Keep the tone professional but actionable.
        """)
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({
        "rag_context": rag_context,
        "kpi_data": kpis
    })
    
    return response.content

if __name__ == "__main__":
    report = generate_report()
    print("\n--- GENERATED REPORT ---\n")
    print(report)
