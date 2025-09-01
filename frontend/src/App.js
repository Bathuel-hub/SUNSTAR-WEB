import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./contexts/ThemeContext";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import About from "./pages/About";
import Products from "./pages/Products";
import Store from "./pages/Store";
import WhyChooseUs from "./pages/WhyChooseUs";
import Contact from "./pages/Contact";
import AdminManager from "./pages/AdminManager";

function App() {
  return (
    <div className="App">
      <ThemeProvider>
        <BrowserRouter>
          <div className="min-h-screen bg-background text-foreground">
            <Header />
            <main className="min-h-screen">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/products" element={<Products />} />
                <Route path="/gallery" element={<Gallery />} />
                <Route path="/why-choose-us" element={<WhyChooseUs />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/manage-7hs82ns8xq0" element={<AdminManager />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </BrowserRouter>
      </ThemeProvider>
    </div>
  );
}

export default App;