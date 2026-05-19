import requests

def scrape_company_website(url: str) -> str:
    jina_url = f"https://r.jina.ai/{url}"
    
    # 1. Look for the API key in the environment variables
    jina_api_key = os.getenv("JINA_API_KEY")
    
    # 2. Build the headers
    headers = {}
    if jina_api_key:
        headers["Authorization"] = f"Bearer {jina_api_key}"
    
    try:
        # 3. Pass the headers into the request
        response = requests.get(jina_url, headers=headers, timeout=15)
        response.raise_for_status() 
        
        content = response.text
        
        if len(content.split()) < 50:
            print(f"Warning: Scraped content for {url} is too short.")
            return _get_fallback_company_data(url)
            
        return content

    except requests.exceptions.RequestException as e:
        print(f"Error: Scraping failed for {url} - {str(e)}")
        return _get_fallback_company_data(url)

def _get_fallback_company_data(url: str) -> str:
    """Sensible Fallback: Returns basic assumptions if scraping fails entirely."""
    return f"""
    Company URL: {url}
    Note: Direct website scraping was restricted or unavailable.
    Assumption based on standard modern web structures:
    - The company likely has a landing page, an about section, and contact info.
    - SEO metadata might be present but unverified.
    - Generative AI readiness cannot be deeply assessed without raw text.
    """