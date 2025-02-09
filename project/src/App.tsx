import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import LandingPage from "./components/Landing";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Chat from "./components/Chat";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
