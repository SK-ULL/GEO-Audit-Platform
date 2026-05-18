import requests

def scrape_company_website(url: str) -> str:
    """
    Attempts to scrape the URL. Includes fallbacks for timeouts, 
    blocks, and websites with insufficient text.
    """
    jina_url = f"https://r.jina.ai/{url}"
    
    try:
        # Added a 10-second timeout so the API doesn't hang forever
        response = requests.get(jina_url, timeout=10)
        response.raise_for_status() # Catches 404s, 403s, etc.
        
        content = response.text
        
        # SENSE CHECK: Did we actually get enough data?
        if len(content.split()) < 50:
            print(f"Warning: Scraped content for {url} is too short. Using fallback.")
            return _get_fallback_company_data(url)
            
        return content

    except requests.exceptions.Timeout:
        print(f"Error: Scraping timed out for {url}.")
        return _get_fallback_company_data(url)
        
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