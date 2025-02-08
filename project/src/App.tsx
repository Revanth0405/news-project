import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Newspaper, MessageSquare, Sparkles, Shield, Brain, Zap, Code, Target, Globe, Trophy, Clapperboard, Building2 } from 'lucide-react';
// import { BriefcaseBusiness } from 'lucide-react';
import Chat from './components/Chat';
import { motion } from 'framer-motion';

function LandingPage() {
  const [sportsNews, setSportsNews] = useState([]);
  const [technologyNews, setTechnologyNews] = useState([]);
  const [businessNews, setBusinessNews] = useState([]);
  const [movieNews, setMovieNews] = useState([]);
  const [locationNews, setLocationNews] = useState([]);
  const [district, setDistrict] = useState(''); // State to store district

  useEffect(() => {
    // Fetch Sports News from NewsAPI
    fetch('https://newsapi.org/v2/everything?q=india%20sports&language=en&sortBy=publishedAt&pageSize=5&apiKey=8fe0758a08174b84b16ef95e0efb0014')
      .then(response => response.json())
      .then(data => setSportsNews(data.articles || []));

    // Fetch Technology News from NewsAPI
    fetch('https://newsapi.org/v2/everything?q=india%20technology&language=en&sortBy=publishedAt&pageSize=5&apiKey=8fe0758a08174b84b16ef95e0efb0014')
      .then(response => response.json())
      .then(data => setTechnologyNews(data.articles || []));

    // Fetch Business News from NewsAPI
    fetch('https://newsapi.org/v2/everything?q=india%20business&language=en&sortBy=publishedAt&pageSize=5&apiKey=8fe0758a08174b84b16ef95e0efb0014')
      .then(response => response.json())
      .then(data => setBusinessNews(data.articles || []));

    // Fetch Movie News from NewsAPI
    fetch('https://newsapi.org/v2/everything?q=india%20movie&language=en&sortBy=publishedAt&pageSize=5&apiKey=8fe0758a08174b84b16ef95e0efb0014')
      .then(response => response.json())
      .then(data => setMovieNews(data.articles || []));

    // Detect location and fetch location-based news
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        // Use a service to convert lat/lng to district
        fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`)
          .then(response => response.json())
          .then(data => {
            const detectedDistrict = data.locality || data.principalSubdivision || 'Unknown District';
            setDistrict(detectedDistrict);
            fetchDistrictNews(detectedDistrict);
            console.log(detectedDistrict);
          });
      });
    } else {
      // Fallback to default district
      fetchDistrictNews('visakhapatnam');
    }
  }, []);

  const fetchDistrictNews = (district) => {
    const query = encodeURIComponent(district + ' news');
    fetch(`https://newsapi.org/v2/everything?q=${query}&language=en&sortBy=publishedAt&pageSize=6&apiKey=8fe0758a08174b84b16ef95e0efb0014`)
      .then(response => response.json())
      .then(data => {
        if (data.articles && data.articles.length > 0) {
          setLocationNews(data.articles);
        } else {
          // Fallback to Visakhapatnam news if no articles found
          fetchVisakhapatnamNews();
        }
      });
  };

  const fetchVisakhapatnamNews = () => {
    fetch('https://newsapi.org/v2/everything?q=visakhapatnam%20news&language=en&sortBy=publishedAt&pageSize=5&apiKey=8fe0758a08174b84b16ef95e0efb0014')
      .then(response => response.json())
      .then(data => setLocationNews(data.articles || []));
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
            Advanced AI technology powered by Gemini and Llama models that summarizes news with ethical analysis and key insights, 
            helping you make informed decisions in today's fast-paced world.
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
        <h2 className="text-3xl font-bold text-center mb-12">Latest News In India</h2>
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
                <li key={index} className="bg-gray-700 p-2 rounded hover:bg-gray-600 transition-colors">
                  <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
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
                <li key={index} className="bg-gray-700 p-2 rounded hover:bg-gray-600 transition-colors">
                  <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
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
                <li key={index} className="bg-gray-700 p-2 rounded hover:bg-gray-600 transition-colors">
                  <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
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
                <li key={index} className="bg-gray-700 p-2 rounded hover:bg-gray-600 transition-colors">
                  <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
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
        <h2 className="text-3xl font-bold text-center mb-12">Location-Based News</h2>
        <p className="text-center text-gray-400 mb-8">Detected District: {district}</p>
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
              <a href={article.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
                Read more
              </a>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Footer Section */}
      <Footer />
    </div>
  );
}

function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h4 className="text-lg font-bold text-white">Our Work</h4>
            <p className="text-sm">We provide AI-driven news insights to help you stay informed and make informed decisions.</p>
          </div>
          <div className="mb-4 md:mb-0">
            <h4 className="text-lg font-bold text-white">Query Details</h4>
            <p className="text-sm">For any queries, please contact us at:</p>
            <p className="text-sm">Email: newsai@gmail.com</p>
            <p className="text-sm">Phone: +91 1234567890</p>
          </div>
          <div>
            <h4 className="text-lg font-bold text-white">Contact Us</h4>
            <p className="text-sm">Feel free to reach out for more information.</p>
          </div>
        </div>
      </div>
    </footer>
  );
}

function Navbar() {
  return (
    <nav className="bg-black/30 backdrop-blur-sm fixed w-full z-10">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <Newspaper className="w-8 h-8 text-blue-400" />
            <span className="font-bold text-xl">NewsAI</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link to="/" className="text-gray-300 hover:text-white transition-colors">
              Home
            </Link>
            <Link
              to="/chat"
              className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
            >
              <MessageSquare className="w-4 h-4" />
              Chat
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;