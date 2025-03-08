import { Link } from "react-router-dom";
import { Newspaper, MessageSquare } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="bg-black/30 backdrop-blur-sm fixed w-full z-10">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <Newspaper className="w-8 h-8 text-blue-400" />
            <span className="font-bold text-xl">NewsAI</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link
              to="/"
              className="text-gray-300 hover:text-white transition-colors"
            >
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
