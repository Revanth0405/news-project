"""
Flask application which serves as the backend for the project, serving the api
which enables users to post data and get results from the model itself
"""

import json
import re
from logging import getLogger

from flask import Flask, request

import llm_helper
import google_search
from scraping.scrape_helper import ContentScraper
from app_logging import setup_logging

setup_logging()
logger = getLogger("root")

app = Flask(__name__)


my_scraper = ContentScraper()


@app.route("/fetch_news", methods=["POST"])
def user_prompt():
    user_query = request.args.get("query")
    if not user_query:
        return {"error": "No query provided"}, 400

    try:
        result = llm_helper.analyse_query(user_query)
        json_result = json.loads(result)
        # print(json_result)
        google_query = google_search.custom_search(json_result["google_search"])
        for query in google_query:
            query = str(query)
            match = re.search(r"https://[^\s]+", query)
            if match:
                link = match.group(0)
                useful_content = my_scraper.__fetch_website_content(link)
                print(useful_content)
                print("??????????????????????????????????????????")
            else:
                print("No match found")

        return {"message": useful_content, "status": "success"}, 201
    except Exception as e:
        return {"error": str(e), "status": "error"}, 500


if __name__ == "__main__":
    app.run(debug=True)
