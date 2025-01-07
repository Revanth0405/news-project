from flask import Flask, request
import llm_helper

app = Flask(__name__)


@app.route("/fetch_news", methods=["POST"])
def user_prompt():
    user_query = request.args.get("query")
    if not user_query:
        return {"error": "No query provided"}, 400

    try:
        result = llm_helper.user_query_analysis(user_query)

        return {"message": result, "status": "success"}, 201
    except Exception as e:
        return {"error": str(e), "status": "error"}, 500


if __name__ == "__main__":
    app.run(debug=True)
