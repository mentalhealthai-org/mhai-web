import React from 'react';
import './home.css'; // Keep this if you have custom styles
import aiDrivenImg from '../../assets/images/home/ai-driven.jpg';
import surveyImg from '../../assets/images/home/survey.jpg';
import supportImg from '../../assets/images/home/support.jpg';

function Home() {
  return (
    <div className="container my-5">

      {/* About Section */}
      <section className="mb-5">
        <div className="row align-items-center">
          {/* Text Content */}
          <div className="col-md-6">
            <h2 className="mb-4">About Mhai</h2>
            <p>
              At Mhai, we believe that mental health support should be accessible, immediate, and personalized. Leveraging cutting-edge AI technology, our platform offers early intervention tools to help individuals navigate mental health challenges before they escalate.
            </p>
            <p>
              Our mission is to provide a seamless blend of technology and human empathy, ensuring that everyone has the resources they need to maintain their mental well-being. Whether you're seeking companionship through AI interactions or professional assistance, Mhai is here to support you every step of the way.
            </p>
            <a href="#cta" className="btn btn-primary">
              Get Started
            </a>
          </div>
          <div className="col-md-6">
            <img src="static/images/logo-big.png" alt="logo"/>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="mb-5">
        <h2 className="text-center mb-4">Our Features</h2>
        <div className="row g-4">

          {/* Feature 1 */}
          <div className="col-md-4">
            <div className="card h-100 shadow-sm">
              <img src={aiDrivenImg} className="card-img-top" alt="AI-Driven Chat" />
              <div className="card-body">
                <h5 className="card-title text-center">AI-Driven Chat</h5>
                <p className="card-text">
                  Engage with a compassionate AI companion that understands and supports
                  your mental well-being. Our AI-driven chat provides a safe and non-judgmental
                  space where you can freely express your thoughts and feelings. Leveraging
                  advanced natural language processing, the AI listens attentively, offers
                  personalized insights, and delivers tailored coping strategies to help you
                  navigate through challenging emotions. Whether you're seeking someone to talk
                  to during difficult times or looking for guidance to manage stress and anxiety,
                  our intelligent chatbot is available around the clock to support your mental
                  health journey.
                </p>
              </div>
            </div>
          </div>

          {/* Feature 2 */}
          <div className="col-md-4">
            <div className="card h-100 shadow-sm">
              <img src={surveyImg} className="card-img-top" alt="Surveys & Assessments" />
              <div className="card-body">
                <h5 className="card-title text-center">Surveys & Assessments</h5>
                <p className="card-text">
                  Regular check-ins through personalized surveys to monitor and assess
                  your mental health. Our platform offers thoughtfully designed surveys
                  that adapt to your unique experiences and needs. These assessments
                  provide a comprehensive overview of your emotional and psychological
                  state over time, enabling you to track your progress and identify
                  patterns or triggers that may affect your well-being. By engaging
                  in consistent self-reflection, you gain valuable insights into your
                  mental health, empowering you to make informed decisions and seek
                  support when necessary.
                </p>
              </div>
            </div>
          </div>

          {/* Feature 3 */}
          <div className="col-md-4">
            <div className="card h-100 shadow-sm">
              <img src={supportImg} className="card-img-top" alt="Professional Support" />
              <div className="card-body">
                <h5 className="card-title text-center">Professional Support</h5>
                <p className="card-text">
                  Access to licensed mental health professionals for personalized guidance
                  and crisis intervention. Our platform connects you with certified
                  therapists and counselors who are dedicated to supporting your mental
                  well-being. Whether you're navigating through daily stresses or facing
                  significant emotional challenges, our professionals provide tailored
                  advice and evidence-based strategies to help you manage and overcome
                  obstacles. In moments of crisis, immediate intervention is available to
                  ensure you receive the urgent support you need.
                </p>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* Call to Action Section */}
      <section id="cta" className="text-center">
        <h2 className="mb-4">Join the Mhai Community</h2>
        <p className="mb-4">
          Take the first step towards better mental health. Sign up today and start your journey with Mhai.
        </p>
        <a href="#signup" className="btn btn-primary btn-lg">
          Get Started
        </a>
      </section>

    </div>
  );
}

export default Home;
