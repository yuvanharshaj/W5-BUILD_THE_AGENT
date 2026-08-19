import sys
import json
import urllib.request
import urllib.parse

def search_wikipedia(query):
    """Searches Wikipedia and returns the first paragraph of the result."""
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        search_results = data.get("query", {}).get("search", [])
        if not search_results:
            return "No results found for that query."
        
        # Get the pageid of the first result
        page_id = search_results[0]['pageid']
        
        # Fetch the extract for the first result
        extract_url = f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&pageids={page_id}"
        ext_req = urllib.request.Request(extract_url, headers={'User-Agent': 'Mozilla/5.0'})
        ext_response = urllib.request.urlopen(ext_req)
        ext_data = json.loads(ext_response.read())
        
        pages = ext_data.get("query", {}).get("pages", {})
        for pid, pdata in pages.items():
            return pdata.get("extract", "No extract found.")
            
    except Exception as e:
        return f"Error connecting to Wikipedia API: {e}"

def main():
    print("==========================================")
    print("  Welcome to the Wikipedia Summarizer!    ")
    print("==========================================")
    print("This agent uses the Wikipedia API (live tool) to fetch summaries.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        try:
            query = input("User: ")
            if query.lower() in ['exit', 'quit']:
                print("Agent: Goodbye!")
                break
                
            if not query.strip():
                continue
                
            print(f"Agent: Let me look up '{query}' on Wikipedia...")
            summary = search_wikipedia(query)
            
            print(f"\nAgent: Here is what I found:\n{summary}\n")
            
        except KeyboardInterrupt:
            print("\nAgent: Goodbye!")
            break

if __name__ == "__main__":
    main()
