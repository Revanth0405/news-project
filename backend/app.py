from flask import Flask, request
import llm_helper
import google_search
import json
import re
import scraping.scraping_llm
import scraping.scrape_helper

app = Flask(__name__)


@app.route("/fetch_news", methods=["POST"])
def user_prompt():
    user_query = request.args.get("query")
    if not user_query:
        return {"error": "No query provided"}, 400

    try:
        result = llm_helper.user_query_analysis(user_query)
        json_result = json.loads(result)
        # print(json_result)
        google_query = google_search.custom_search(json_result['google_search'])
        for query in google_query:
            query = str(query)
            match = re.search(r"https://[^\s]+", query)
            if match:
                link = match.group(0)
                useful_content = scraping.scrape_helper.scrape_website(link)
                print(useful_content)
                print("??????????????????????????????????????????")
            else:
                print("No match found")

        return {"message": useful_content, "status": "success"}, 201
    except Exception as e:
        return {"error": str(e), "status": "error"}, 500


if __name__ == "__main__":
    app.run(debug=True)
