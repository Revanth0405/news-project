import axios from "axios";

const news_api_key: string = import.meta.env.VITE_NEWS_API_KEY || "";

const news_api = axios.create({
  baseURL: "https://newsapi.org/v2/everything",
  params: {
    "language": "en",
    "pageSize": "5",
    "sortBy": "publishedAt",
    "apiKey": news_api_key,
  }
});

export default news_api;
