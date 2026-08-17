from ddgs import DDGS


def search(query):
    results = DDGS().text(
        query,
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
        "query": query,
        "results": clean_results
    }