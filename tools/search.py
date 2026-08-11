from ddgs import DDGS


def search(search_query):
    results = DDGS().text(
        search_query,
        max_results=5
    )

    clean_results = []

    for result in results:
        clean_results.append({
            "title": result.get("title"),
            "url": result.get("href"),
            "snippet": result.get("body")
        })

    return {
        "query": search_query,
        "results": clean_results
    }