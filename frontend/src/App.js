import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <main className="min-h-screen">
          <Routes>
            <Route path="/" element={<Home />} />
            {/* Additional routes will be added for other pages */}
            <Route path="/about" element={<div className="p-8 text-center">About page coming soon...</div>} />
            <Route path="/products" element={<div className="p-8 text-center">Products page coming soon...</div>} />
            <Route path="/why-choose-us" element={<div className="p-8 text-center">Why Choose Us page coming soon...</div>} />
            <Route path="/contact" element={<div className="p-8 text-center">Contact page coming soon...</div>} />
          </Routes>
        </main>
        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;