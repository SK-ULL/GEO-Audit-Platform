import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_geo_audit(company_name: str, scraped_text: str) -> str:
    """
    Uses Groq API for lightning-fast, free AI analysis.
    """
    # Initialize the Groq client
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Using Llama 3.3 70B (High performance, Free Tier)
    model_id = "llama-3.3-70b-versatile"

    prompt = f"""
    You are a Senior AI Strategy Consultant. 
    Analyze the following website content for the company '{company_name}':
    {scraped_text[:5000]} 
    
    TASK: Generate a professional GEO (Generative Engine Optimization) Audit.
    STRICT INSTRUCTIONS:
    1. Your analysis must be based EXCLUSIVELY on the 'SCRAPED CONTENT' provided above.
    2. If the 'SCRAPED CONTENT' appears to be an error page, a "domain for sale" page, or does not mention '{company_name}', you MUST begin your report with a 'Data Integrity Warning' stating that the URL provided may be incorrect.
    3. Do not use your internal knowledge about '{company_name}' if it contradicts the provided content.
    
    INSTRUCTIONS:
    1. Deduce the core industry/domain of the company based on the content.
    2. Identify a top-tier, highest-GEO-rated competitor website in that exact domain.
    3. Compare '{company_name}' against this competitor across key GEO metrics.
    4. If the provided content is insufficient, provide a general baseline audit for the deduced domain.
    
    FORMATTING RULES:
    - Use clean, professional formatting. 
    - DO NOT use extensive hashtags or asterisks. 
    - Ensure headings are professional and engage the reader directly (e.g., "Your Competitive Landscape").
    - DO NOT attempt to draw graphs or charts. Use structured text or simple comparisons instead.
    
    REQUIRED SECTIONS:
    
    Executive Summary
    [A brief, direct assessment of their AI-readiness]
    
    Competitive Analysis: {company_name} vs. [Insert Competitor Name]
    [Provide insightful comparative text]
    
    Metric Breakdown (Score out of 100)
    - AI Citation Frequency: [Score] 
    - Semantic Authority Score: [Score]
    - AI Extractability / Answerability: [Score]
    - Entity Trust & Knowledge Graph Presence: [Score]
    - RAG Retrieval Performance: [Score]
    
    Insights & Recommendations
    [Bullet points detailing exactly how they can close the gap with the competitor]
    """

    try:
        completion = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        # We catch the exact error, log it, and return a rule-based template!
        print(f"CRITICAL: AI Generation Failed. Reason: {e}")
        print("Falling back to Rule-Based GEO Audit Template...")
        
        return f"""# Automated GEO Audit for {company_name}
        
## ⚠️ AI Analysis Temporarily Unavailable
*Our cognitive engines are currently experiencing high load. Below is your structural audit based on standard GEO heuristics.*

Baseline Generative Engine Optimization (GEO) Checklist:
1. Semantic HTML: Ensure you are using H1/H2 tags formatted as natural language questions.
2. Entity Recognition: Explicitly define your core services so AI models (like ChatGPT/Gemini) can categorize you.
3. Information Density: Increase the depth of your content. Thin pages are ignored by LLMs.
"""