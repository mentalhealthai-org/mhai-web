// src/pages/userprofile/AIProfileBio.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';

import getCSRFToken from '../../libs/csrf';
import getContext from '../../libs/context';
import AIProfileSideBar from '../../components/ai_profile/side_bar_menu';

function AIProfileBio() {
  const csrftoken = getCSRFToken();
  const context = getContext();
  const ai_profile_id = context['ai_profile_id'];
  const api_url = '/api/ai-profile/bio/' + ai_profile_id + '/';

  const [bio, setBio] = useState({
    bio_life: '',
    bio_education: '',
    bio_work: '',
    bio_family: '',
    bio_friends: '',
    bio_pets: '',
    bio_health: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    axios
      .get(api_url, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrftoken,
        },
      })
      .then((response) => {
        setBio({
          bio_life: response.data.bio_life,
          bio_education: response.data.bio_education,
          bio_work: response.data.bio_work,
          bio_family: response.data.bio_family,
          bio_friends: response.data.bio_friends,
          bio_pets: response.data.bio_pets,
          bio_health: response.data.bio_health,
        });
        setLoading(false);
      })
      .catch((error) => {
        setError('Failed to fetch bio information.');
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    setBio({ ...bio, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    axios
      .put(api_url, bio, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrftoken,
        },
      })
      .then((response) => {
        setSuccess('Bio information updated successfully.');
      })
      .catch((error) => {
        setError('Failed to update bio information.');
      });
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container mt-4">
      <div className="row">
        {/* Sidebar */}
        <div className="col-md-3">
          <AIProfileSideBar active="bio" />
        </div>
        {/* Main Content */}
        <div className="col-md-9">
          <h2>Mhai Bio</h2>
          {success && <div className="alert alert-success">{success}</div>}
          <form onSubmit={handleSubmit}>
            {/* Life */}
            <div className="mb-3">
              <label htmlFor="bio_life" className="form-label">Life</label>
              <textarea
                className="form-control"
                id="bio_life"
                name="bio_life"
                rows="3"
                value={bio.bio_life}
                onChange={handleChange}
              ></textarea>
            </div>

            {/* Education */}
            <div className="mb-3">
              <label htmlFor="bio_education" className="form-label">Education</label>
              <textarea
                className="form-control"
                id="bio_education"
                name="bio_education"
                rows="3"
                value={bio.bio_education}
                onChange={handleChange}
              ></textarea>
            </div>

            {/* Work */}
            <div className="mb-3">
              <label htmlFor="bio_work" className="form-label">Work</label>
              <textarea
                className="form-control"
                id="bio_work"
                name="bio_work"
                rows="3"
                value={bio.bio_work}
                onChange={handleChange}
              ></textarea>
            </div>

            {/* Family */}
            <div className="mb-3">
              <label htmlFor="bio_family" className="form-label">Family</label>
              <textarea
                className="form-control"
                id="bio_family"
                name="bio_family"
                rows="3"
                value={bio.bio_family}
                onChange={handleChange}
              ></textarea>
            </div>

            {/* Friends */}
            <div className="mb-3">
              <label htmlFor="bio_friends" className="form-label">Friends</label>
              <textarea
                className="form-control"
                id="bio_friends"
                name="bio_friends"
                rows="3"
                value={bio.bio_friends}
                onChange={handleChange}
              ></textarea>
            </div>

            {/* Pets */}
            <div className="mb-3">
              <label htmlFor="bio_pets" className="form-label">Pets</label>
              <textarea
                className="form-control"
                id="bio_pets"
                name="bio_pets"
                rows="3"
                value={bio.bio_pets}
                onChange={handleChange}
              ></textarea>
            </div>

            {/* Health */}
            <div className="mb-3">
              <label htmlFor="bio_health" className="form-label">Health</label>
              <textarea
                className="form-control"
                id="bio_health"
                name="bio_health"
                rows="3"
                value={bio.bio_health}
                onChange={handleChange}
              ></textarea>
            </div>

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary">Save Bio</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default AIProfileBio;
