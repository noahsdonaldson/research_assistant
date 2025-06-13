import os
import time
import re
from dotenv import load_dotenv
from openai import AzureOpenAI
from auth import get_access_token
from tavily import TavilyClient

load_dotenv()

def initialize_clients():
    try:
        app_key = os.getenv('APP_KEY')
        api_key = get_access_token()
        tavily_api_key = os.getenv('TAVILY_API_KEY')
        client = AzureOpenAI(
            azure_endpoint='endpoint url',
            api_key=api_key,
            api_version="2024-08-01-preview"
        )
        tavily_client = TavilyClient(api_key=tavily_api_key)
        return client, tavily_client, app_key
    except Exception as e:
        raise RuntimeError(f"Failed to initialize API clients: {e}")

def to_list(text):
    quotes = re.findall(r'"([^"]*)"', text)
    return quotes

def generate_search_queries(company_name, client, app_key):
    """Generate relevant search queries using ChatGPT"""
    messages = [
        {
            "role": "system",
            "content": 
            """
            You are a research assistant that generates relevant search queries based on the company name provided.
            Here are the requirements:
            1. Generate a list of search queries that will help gather information about the company.
            2. It is ok to only generate one search query for simple or basic requests.
            3. The search queries should be relevant to the company and should not be too broad or too narrow.
            4. The search queries should be in the form of a list of strings, each string representing a search query.
            5. The search queries should be enclosed in double quotes.
            6. Do not include any additional text or explanations, just return the list of search queries.
            """
        },
        {
            "role": "user",
            "content": f"""
                Detail the following aspects of the company {company_name}:
                1. What AI or LLM projects have been announced or are under development?
                2. What are the use cases associated with these projects (concrete examples of applications)?
                3. Who are the partners involved (technology suppliers, research labs, startups, etc.)?
                4. What are the main benefits expected (performance, time savings, cost reductions, etc.)?
                5. What risks have been identified concerning the use of LLMs (ethical issues, security, reliability, confidentiality, etc.)?
                6. What internal tasks or activities does the company plan to automate using LLMs?
                7. What returns on investment (ROI) are expected or have already been measured?
                8. What governance and CSR programs are in place around AI?
                9. What IT, GPU, server, network, storage and software architectures are being used? Name the publishers and companies involved.
                10. What security and observability architectures and solutions have been implemented as part of these AI projects? Name the publishers and companies involved.
                11. What are the main AI-related challenges the company is currently facing?
                12. What are other companies in the same industry doing with AI? Provide a comparative analysis.
                13. Who are the technical managers or members of the management team involved, and what is their role in the company? Give the names and their roles.
            """
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            user=f'{{"appkey": "{app_key}"}}'
        )
        content = response.choices[0].message.content
        queries = to_list(content)
        return queries
    except Exception as e:
        raise RuntimeError(f"Error generating search queries: {e}")

def search_web(query, tavily_client):
    """Search the web using Tavily API"""
    payload = {
        "query": query,
        "topic": "general",
        "search_depth": "basic",
        "chunks_per_source": 3,
        "max_results": 10,
        "time_range": "year",
        "days": 90,
        "include_answer": True,
        "include_raw_content": True,
        "include_images": False,
        "include_image_descriptions": False,
        "include_domains": [],
        "exclude_domains": [],
        "country": "united states"
    }
    
    try:
        response = tavily_client.search(**payload)
        formatted_results = []
        
        for result in response['results']:
            formatted_result = f"Title: {result['title']}\nContent: {result['content']}\nURL: {result['url']}\n"
            formatted_results.append(formatted_result)
        
        return "\n---\n".join(formatted_results)
    except Exception as e:
        raise RuntimeError(f"Error searching for query '{query}': {e}")

def analyze_company_data(company_name, search_data, client, app_key):
    """Analyze the collected search data and generate a comprehensive report"""
    try:
        messages = [
            {
                "role": "system",
                "content": 
                """
                You are a research assistant that generates detailed and structured information about companies, 
                particularly focusing on their AI and LLM projects.

                You will be given data from the internet that you can use for your responses.
                Please structure your response as a comprehensive markdown report with appropriate headings and sections.
                """
            },
            {
                "role": "user",
                "content": f"""
                I have gathered the latest information about the company from various sources.
                Please provide a detailed summary of the company's AI and LLM projects, including any recent developments, partnerships, or notable achievements.
                If the company is not known for AI or LLM projects, please state that clearly but also provide information about any technology initiatives they may have.
                
                Structure your response as a comprehensive markdown report with the following sections:
                1. Executive Summary
                2. AI/LLM Projects and Initiatives
                3. Use Cases and Applications - Identify which use cases could make sense to run on premisis in the data center or at the edge based on cost, performance, and security.
                4. Technology Partners and Vendors
                5. Expected Benefits and ROI
                6. Risks and Challenges
                7. Internal Automation Plans
                8. Governance and CSR Programs
                9. Technical Architecture and Infrastructure
                10. Security and Observability Solutions
                11. Current AI-Related Challenges
                12. Industry Comparison
                13. Key Personnel and Leadership
                14. Sources and References

                Company Name: {company_name}
                
                Search Data:
                {search_data}
                
                Please cite specific sources (URLs) when making claims and provide a comprehensive analysis.
                If you cannot find information for a particular section, please state that clearly.
                """
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            user=f'{{"appkey": "{app_key}"}}'
        )

        content = response.choices[0].message.content
        return content if content else "No information found or error in response."
    except Exception as e:
        raise RuntimeError(f"Error analyzing information for {company_name}: {e}")

def research_company(company_name, progress_callback=None, status_callback=None, search_callback=None):
    """Complete research workflow for a single company.
    Optionally accepts callbacks for progress/status updates (for frontend use).
    """
    client, tavily_client, app_key = initialize_clients()
    if not all([client, tavily_client, app_key]):
        raise RuntimeError("Failed to initialize API clients.")

    try:
        # Step 1: Generate search queries
        if status_callback:
            status_callback("🔍 Generating search queries...")
        if progress_callback:
            progress_callback(10)
        search_queries = generate_search_queries(company_name, client, app_key)
        
        if search_callback:
            search_callback(search_queries)
        
        # Step 2: Collect search data
        if status_callback:
            status_callback("📊 Collecting search data...")
        if progress_callback:
            progress_callback(30)
        
        all_search_data = []
        for i, query in enumerate(search_queries):
            if status_callback:
                status_callback(f"Searching ({i+1}/{len(search_queries)}): {query[:50]}...")
            search_results = search_web(query, tavily_client)
            all_search_data.append(f"=== Search Query: {query} ===\n{search_results}")
            if progress_callback:
                progress_callback(30 + int(40 * (i + 1) / len(search_queries)))
            time.sleep(1)  # Rate limiting
        
        # Combine all search data
        combined_search_data = "\n\n".join(all_search_data)
        if progress_callback:
            progress_callback(70)
        
        # Step 3: Analyze the data
        if status_callback:
            status_callback("🤖 Analyzing collected data...")
        if progress_callback:
            progress_callback(80)
        analysis_report = analyze_company_data(company_name, combined_search_data, client, app_key)
        
        if progress_callback:
            progress_callback(100)
        if status_callback:
            status_callback("✅ Research completed!")
        
        return analysis_report
        
    except Exception as e:
        raise RuntimeError(f"Error during research: {e}")
