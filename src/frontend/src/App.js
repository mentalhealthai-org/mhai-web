// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import NotFound from './pages/NotFound/NotFound';
import Home from './pages/home/home';
import About from './pages/about/about';
import UserProfileBio from './pages/user_profile/bio';
import UserProfileEmotions from './pages/user_profile/emotions';
import UserProfileGeneral from './pages/user_profile/general';
import UserProfileInterests from './pages/user_profile/interests';


function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="*" element={<NotFound />} /> */}
				<Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
				<Route path="/profile" element={<UserProfileGeneral />} />
				<Route path="/profile/bio" element={<UserProfileBio />} />
				<Route path="/profile/emotions" element={<UserProfileEmotions />} />
				<Route path="/profile/interests" element={<UserProfileInterests />} />
      </Routes>
    </Router>
  );
}

export default App;
