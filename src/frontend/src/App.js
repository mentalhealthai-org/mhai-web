// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import NotFound from './pages/NotFound/NotFound';
import Home from './pages/home/home';
import About from './pages/about/about';
import AIProfileBio from './pages/ai_profile/bio';
import AIProfileEmotions from './pages/ai_profile/emotions';
import AIProfileGeneral from './pages/ai_profile/general';
import AIProfileInterests from './pages/ai_profile/interests';
import UserProfileBio from './pages/user_profile/bio';
import UserProfileEmotions from './pages/user_profile/emotions';
import UserProfileGeneral from './pages/user_profile/general';
import UserProfileInterests from './pages/user_profile/interests';
import UserProfileCriticalEvents from './pages/user_profile/critical_events';


function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="*" element={<NotFound />} /> */}
				<Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
				<Route path="/ai-profile" element={<AIProfileGeneral />} />
				<Route path="/ai-profile/bio" element={<AIProfileBio />} />
				<Route path="/ai-profile/emotions" element={<AIProfileEmotions />} />
				<Route path="/ai-profile/interests" element={<AIProfileInterests />} />
				<Route path="/profile" element={<UserProfileGeneral />} />
				<Route path="/profile/bio" element={<UserProfileBio />} />
				<Route path="/profile/emotions" element={<UserProfileEmotions />} />
				<Route path="/profile/interests" element={<UserProfileInterests />} />
				<Route path="/profile/critical-events" element={<UserProfileCriticalEvents />} />
      </Routes>
    </Router>
  );
}

export default App;
