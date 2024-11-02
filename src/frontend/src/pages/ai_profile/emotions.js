import React, { useState, useEffect } from 'react';
import axios from 'axios';

import getCSRFToken from '../../libs/csrf';
import getContext from '../../libs/context';
import AIProfileSideBar from '../../components/ai_profile/side_bar_menu';

function AIProfileEmotions() {
  const csrftoken = getCSRFToken();
  const context = getContext();
  const profile_id = context['profile_id'];
  const api_url = '/api/ai-profile/emotions/' + profile_id + '/';

  const [emotions, setEmotions] = useState('');
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
        setEmotions(response.data.emotions || '');
        setLoading(false);
      })
      .catch((error) => {
        setError('Failed to fetch emotions.');
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    setEmotions(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    axios
      .put(
        api_url,
        { emotions: emotions },
        {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrftoken,
          },
        }
      )
      .then((response) => {
        setSuccess('Emotions updated successfully.');
      })
      .catch((error) => {
        setError('Failed to update emotions.');
      });
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container mt-4">
      <div className="row">
        {/* Sidebar */}
        <div className="col-md-3">
          <AIProfileSideBar active="emotions" />
        </div>
        {/* Main Content */}
        <div className="col-md-9">
          <h2>Emotional Status</h2>
          {success && <div className="alert alert-success">{success}</div>}
          <form onSubmit={handleSubmit}>
            {/* Emotional Profile Textarea */}
            <div className="mb-3">
              <label htmlFor="emotions" className="form-label">
                Your Emotional Profile
              </label>
              <textarea
                className="form-control"
                id="emotions"
                name="emotions"
                rows="5"
                value={emotions}
                onChange={handleChange}
                required
              ></textarea>
            </div>

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary">
              Save Emotional Status
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default AIProfileEmotions;
