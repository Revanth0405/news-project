class CustomSearchResult:
    """
    CustomSearchResult class is a class that represents a single search result
    from the Google Custom Search API.
    """

    def __init__(self, title: str, htmlTitle: str, link: str, displayLink: str):
        self.title = title
        self.htmlTitle = htmlTitle
        self.link = link
        self.displayLink = displayLink

    def __str__(self):
        return f"{self.title} - {self.link}"
