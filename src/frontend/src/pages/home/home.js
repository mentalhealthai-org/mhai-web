// src/App.js
import React from 'react';
import ReactDOM from 'react-dom';

import './home.css';

function Home() {
  return (
    <div className="App font-sans text-gray-900">

      {/* About Section */}
      <section className="py-20">
        <div className="mx-auto px-6 flex flex-col md:flex-row items-center">
          {/* Text Content */}
          <div className="md:w-1/2 md:pl-12">
            <h2 className="text-3xl font-semibold mb-4">About Mhai</h2>
            <p className="text-gray-700 mb-4">
              At Mhai, we believe that mental health support should be accessible, immediate, and personalized. Leveraging cutting-edge AI technology, our platform offers early intervention tools to help individuals navigate mental health challenges before they escalate.
            </p>
            <p className="text-gray-700 mb-4">
              Our mission is to provide a seamless blend of technology and human empathy, ensuring that everyone has the resources they need to maintain their mental well-being. Whether you're seeking companionship through AI interactions or professional assistance, Mhai is here to support you every step of the way.
            </p>
            <a href="#cta" className="inline-block bg-blue-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-blue-700 transition">
              Get Started
            </a>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-100">
        <div className="mx-auto px-6">
          <h2 className="text-3xl font-semibold text-center mb-12">Our Features</h2>
          <div className="flex flex-wrap -mx-4">
            {/* Feature 1 */}
            <div className="w-full md:w-1/3 px-4 mb-8">
              <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition">
                <div className="mb-4">
                  <img src="static/images/home/ai-driven.jpg" className="w-100" />
                </div>
                <h3 className="text-xl font-semibold text-center mb-2">AI-Driven Chat</h3>
                <p className="text-center text-gray-600">
                  Engage with a compassionate AI companion that understands and supports your
                  mental well-being.
                </p>
                <p className="text-center text-gray-600">
                  Our AI-driven chat provides a safe and non-judgmental space where you can
                  freely express your thoughts and feelings. Leveraging advanced natural
                  language processing, the AI listens attentively, offers personalized
                  insights, and delivers tailored coping strategies to help you navigate
                  through challenging emotions. Whether you're seeking someone to talk to during
                  difficult times or looking for guidance to manage stress and anxiety, our
                  intelligent chatbot is available around the clock to support your mental
                  health journey.
                </p>
              </div>
            </div>

            {/* Feature 2 */}
            <div className="w-full md:w-1/3 px-4 mb-8">
              <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition">
                <div className="mb-4">
                <img src="static/images/home/survey.jpg" className="w-100" />
                </div>
                <h3 className="text-xl font-semibold text-center mb-2">Surveys & Assessments</h3>
                <p className="text-center text-gray-600">
                Regular check-ins through personalized surveys to monitor and assess your
                mental health. Our platform offers thoughtfully designed surveys that adapt
                to your unique experiences and needs. These assessments provide a comprehensive
                overview of your emotional and psychological state over time, enabling you to
                track your progress and identify patterns or triggers that may affect your
                well-being. By engaging in consistent self-reflection, you gain valuable
                insights into your mental health, empowering you to make informed decisions
                and seek support when necessary. Additionally, the data collected from these
                surveys helps our AI algorithms to better understand your condition, allowing for
                more accurate predictions and tailored interventions. Whether you're managing stress,
                anxiety, or other mental health challenges, our Surveys & Assessments feature serves
                as a vital tool in your journey towards sustained mental wellness.
                </p>
              </div>
            </div>

            {/* Feature 3 */}
            <div className="w-full md:w-1/3 px-4 mb-8">
              <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition">
                <div className="mb-4">
                <img src="static/images/home/support.jpg" className="w-100" />
                </div>
                <h3 className="text-xl font-semibold text-center mb-2">Professional Support</h3>
                <p className="text-center text-gray-600">
                  Access to licensed mental health professionals for personalized guidance and
                  crisis intervention. Our platform connects you with certified therapists and
                  counselors who are dedicated to supporting your mental well-being. Whether
                  you're navigating through daily stresses or facing significant emotional
                  challenges, our professionals provide tailored advice and evidence-based
                  strategies to help you manage and overcome obstacles. In moments of crisis,
                  immediate intervention is available to ensure you receive the urgent support
                  you need. Through secure and confidential consultations, you can engage in
                  meaningful conversations, set achievable goals, and develop resilience to
                  foster long-term mental health. Empower yourself with the expertise of our
                  licensed professionals, who are committed to guiding you towards a healthier,
                  more balanced life.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section id="cta" className="py-20">
        <div className="mx-auto px-6 text-center">
          <h2 className="text-3xl font-semibold mb-4">Join the Mhai Community</h2>
          <p className="text-gray-700 mb-8">
            Take the first step towards better mental health. Sign up today and start your journey with Mhai.
          </p>
          <a href="#signup" className="bg-blue-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-blue-700 transition">
            Get Started
          </a>
        </div>
      </section>

    </div>
  );
}

export default Home;

// ReactDOM.render(<Home />, document.getElementById('home-root'));
