"""
The Backend Application package
"""

import json
import logging

from flask import Flask, request

from app.google_search import custom_search
from app.scraping import MyContentScraper
from app.output_generator import extract_information_from_html
from app.llm import analyse_user_query
from app.utils.logger import get_logger

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)

def create_app(name: str = __name__) -> Flask:
    """
    Creates a new flask app for our backend application
    """
    app = Flask(name)

    my_scraper = MyContentScraper()

    # setup routes
    @app.route('/status')
    def status():
        return "App running and live"

    @app.route('/fetch_news', methods=['POST'])
    def fetch_news():
        user_query = request.args.get("query")
        if not user_query:
            return {"error": "No query provided"}, 400

        try:
            logger.info("New request to fetch news with query: %s", user_query)
            result = analyse_user_query(user_query)
            json_result = json.loads(result)
            # print(json_result)
            google_query = custom_search(json_result["google_search"])
            output = my_scraper.fetch_websites(google_query)
            useful_content = ""
            for _, value in output.items():
                useful_content += value
            result = extract_information_from_html(useful_content, user_query)

            return {"message": useful_content, "status": "success"}, 201
        except Exception as e:
            return {"error": str(e), "status": "error"}, 500

    return app

