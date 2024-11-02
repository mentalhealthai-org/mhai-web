import React, { useState, useEffect } from 'react';
import axios from 'axios';

import getCSRFToken from '../../libs/csrf';
import getContext from '../../libs/context';
import AIProfileSideBar from '../../components/ai_profile/side_bar_menu';

function AIProfileInterests() {
  const csrftoken = getCSRFToken();
  const context = getContext();
  const profile_id = context['profile_id'];
  const api_url = '/api/ai-profile/interests/' + profile_id + '/';

  const [interests, setInterests] = useState('');
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
        setInterests(response.data.interests || '');
        setLoading(false);
      })
      .catch((error) => {
        setError('Failed to fetch interests.');
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    setInterests(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    axios
      .put(
        api_url,
        { interests },
        {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrftoken,
          },
        }
      )
      .then((response) => {
        setSuccess('Interests updated successfully.');
      })
      .catch((error) => {
        setError('Failed to update interests.');
      });
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container mt-4">
      <div className="row">
        {/* Sidebar */}
        <div className="col-md-3">
          <AIProfileSideBar active="interests" />
        </div>
        {/* Main Content */}
        <div className="col-md-9">
          <h2>Interests</h2>
          {success && <div className="alert alert-success">{success}</div>}
          <form onSubmit={handleSubmit}>
            {/* Interests Textarea */}
            <div className="mb-3">
              <label htmlFor="interests" className="form-label">
                Your Interests
              </label>
              <textarea
                className="form-control"
                id="interests"
                name="interests"
                rows="5"
                value={interests}
                onChange={handleChange}
                required
              ></textarea>
            </div>

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary">
              Save Interests
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default AIProfileInterests;
