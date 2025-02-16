from core.research.schemas import SearchResponse


def pretty_print_search_results(search_results: list[SearchResponse]) -> str:
    return "\n\n".join(
        [
            f"Search result {idx + 1}\n: Source: {result.domain} - Published: {result.published_date}\n\n Content: {result.content}"
            for idx, result in enumerate(search_results)
        ]
    )
