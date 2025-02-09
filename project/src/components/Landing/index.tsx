import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  MessageSquare,
  Brain,
  Trophy,
  Clapperboard,
  Building2,
} from "lucide-react";

import { NewsArticleObject } from "../../types";
import news_api from "../../utils/api";

export default function LandingPage() {
  const [sportsNews, setSportsNews] = useState<NewsArticleObject[]>([]);
  const [technologyNews, setTechnologyNews] = useState<NewsArticleObject[]>([]);
  const [businessNews, setBusinessNews] = useState<NewsArticleObject[]>([]);
  const [movieNews, setMovieNews] = useState<NewsArticleObject[]>([]);
  const [locationNews, setLocationNews] = useState<NewsArticleObject[]>([]);
  const [district, setDistrict] = useState(""); // State to store district

  useEffect(() => {
    // Fetch different News from NewsAPI
    (async () => {
      {
        const { data } = await news_api.get("/", {
          params: {
            q: "india sports",
          },
        });
        setSportsNews(data.articles || []);
      }

      {
        const { data } = await news_api.get("/", {
          params: {
            q: "india technology",
          },
        });
        setTechnologyNews(data.articles || []);
      }

      {
        const { data } = await news_api.get("/", {
          params: {
            q: "india business",
          },
        });
        setBusinessNews(data.articles || []);
      }

      {
        const { data } = await news_api.get("/", {
          params: {
            q: "india movie",
          },
        });
        setMovieNews(data.articles || []);
      }

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords;
            // Use a service to convert lat/lng to district
            fetch(
              `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`
            )
              .then((response) => response.json())
              .then((data) => {
                console.log(data);
                const detectedDistrict =
                  data.locality ||
                  data.principalSubdivision ||
                  "Unknown District";
                setDistrict(detectedDistrict);
                fetchDistrictNews(detectedDistrict);
                console.log(detectedDistrict);
              });
          },
          () => {
            // Fallback to default district
            setDistrict("Visakhapatnam");
            fetchDistrictNews("visakhapatnam");
          }
        );
      } else {
        // Fallback to default district if geolocation is not supported
        setDistrict("vishakhapatnam");
        fetchDistrictNews("vishakhapatnam");
      }
    })();
  }, []);

  const fetchDistrictNews = async (district: string) => {
    const query = `${district} news`;
    const { data } = await news_api.get("/", {
      params: {
        q: query,
        pageSize: 5,
      },
    });
    console.log(JSON.stringify(data));
    setLocationNews(data.articles || []);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-5xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
            Transform News Understanding with AI
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Advanced AI technology powered by Gemini and Llama models that
            summarizes news with ethical analysis and key insights, helping you
            make informed decisions in today's fast-paced world.
          </p>
          <Link
            to="/chat"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg inline-flex items-center gap-2 transition-colors"
          >
            <MessageSquare className="w-5 h-5" />
            Try It Now
          </Link>
        </motion.div>
      </div>

      {/* Technology Stack */}
      <div className="container mx-auto px-4 py-16 border-t border-gray-800">
        <h2 className="text-3xl font-bold text-center mb-12">
          Latest News In India
        </h2>
        <div className="grid md:grid-cols-4 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-gray-800/50 p-6 rounded-lg shadow-lg"
          >
            <Trophy className="w-12 h-12 text-blue-400 mb-4" />
            <h3 className="text-xl font-bold mb-4">Sports News</h3>
            <ul className="text-gray-300 space-y-2">
              {sportsNews.map((article, index) => (
                <li
                  key={index}
                  className="bg-gray-700 p-2 rounded hover:bg-gray-600 transition-colors"
                >
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:underline"
                  >
                    {article.title}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-gray-800/50 p-6 rounded-lg shadow-lg"
          >
            <Brain className="w-12 h-12 text-purple-400 mb-4" />
            <h3 className="text-xl font-bold mb-4">Technology News</h3>
            <ul className="text-gray-300 space-y-2">
              {technologyNews.map((article, index) => (
                <li
                  key={index}
                  className="bg-gray-700 p-2 rounded hover:bg-gray-600 transition-colors"
                >
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:underline"
                  >
                    {article.title}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-gray-800/50 p-6 rounded-lg shadow-lg"
          >
            <Building2 className="w-12 h-12 text-emerald-400 mb-4" />
            <h3 className="text-xl font-bold mb-4">Business News</h3>
            <ul className="text-gray-300 space-y-2">
              {businessNews.map((article, index) => (
                <li
                  key={index}
                  className="bg-gray-700 p-2 rounded hover:bg-gray-600 transition-colors"
                >
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:underline"
                  >
                    {article.title}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-gray-800/50 p-6 rounded-lg shadow-lg"
          >
            <Clapperboard className="w-12 h-12 text-yellow-400 mb-4" />
            <h3 className="text-xl font-bold mb-4">Movie News</h3>
            <ul className="text-gray-300 space-y-2">
              {movieNews.map((article, index) => (
                <li
                  key={index}
                  className="bg-gray-700 p-2 rounded hover:bg-gray-600 transition-colors"
                >
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:underline"
                  >
                    {article.title}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>
      </div>

      {/* Location-Based News Section */}
      <div className="container mx-auto px-4 py-16 border-t border-gray-800">
        <h2 className="text-3xl font-bold text-center mb-12">
          Location-Based News
        </h2>
        <p className="text-center text-gray-400 mb-8">
          Detected District: {district}
        </p>
        <div className="grid md:grid-cols-3 gap-8">
          {locationNews.map((article, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 * index }}
              className="bg-gray-800/50 p-6 rounded-lg shadow-lg"
            >
              <h3 className="text-xl font-bold mb-2">{article.title}</h3>
              <p className="text-gray-300 mb-4">{article.description}</p>
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:underline"
              >
                Read more
              </a>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
