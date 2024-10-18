import React from 'react';


function About() {
  return (
    <div className="About">
      <header className="About-header">
        <h1>Mhai Project</h1>
        <section className="overview">
          <h2>Overview</h2>
          <p>
            Mhai (Mental Health AI) is an AI-driven platform designed for suicide prevention
            by providing early intervention for individuals facing mental health challenges,
            with a primary focus on anxiety and depression. The platform aims to support
            individuals by recognizing their mental health condition, predicting potential
            periods of crisis, and offering tailored interventions through its three main
            pillars:
          </p>
          <ol>
            <li><strong>AI-Driven Chat:</strong> Interaction with a virtual AI persona to provide companionship and conversation.</li>
            <li><strong>Surveys and Self-Assessments:</strong> Regular emotional and mental health check-ins through structured surveys.</li>
            <li><strong>Professional Support (Premium Tier):</strong> Direct connection with mental health professionals for deeper assistance and crisis intervention.</li>
          </ol>
        </section>

        <section className="project-scope">
          <h2>Project Scope</h2>
          <p>
            Mhai combines AI technologies, surveys, and professional support to monitor and
            assess mental health conditions, focusing on factors that increase the risk of
            suicide. It employs a combination of pre-trained models and custom analytics to
            detect patterns of distress and trigger timely interventions.
          </p>
          <p>
            The project includes the development of mobile and web applications and offers
            both free and premium services, with the premium tier providing access to direct
            mental health support.
          </p>
        </section>

        <section className="future-directions">
          <h2>Future Directions</h2>
          <p>
            The Mhai project is actively seeking grants and partnerships to expand its reach
            and continue developing its capabilities. We envision a world where mental
            health support is accessible to everyone, anywhere, through innovative AI
            technology.
          </p>
          <p>
            For more information or to collaborate, please contact our team via connect@mymhai.com.
          </p>
        </section>

      </header>
    </div>
  );
}

export default About;
