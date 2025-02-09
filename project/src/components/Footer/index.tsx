export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h4 className="text-lg font-bold text-white">Our Work</h4>
            <p className="text-sm">
              We provide AI-driven news insights to help you stay informed and
              make informed decisions.
            </p>
          </div>
          <div className="mb-4 md:mb-0">
            <h4 className="text-lg font-bold text-white">Query Details</h4>
            <p className="text-sm">For any queries, please contact us at:</p>
            <p className="text-sm">Email: newsai@gmail.com</p>
            <p className="text-sm">Phone: +91 1234567890</p>
          </div>
          <div>
            <h4 className="text-lg font-bold text-white">Contact Us</h4>
            <p className="text-sm">
              Feel free to reach out for more information.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
