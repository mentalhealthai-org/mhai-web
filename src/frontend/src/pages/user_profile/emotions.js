import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserProfileEmotions() {
  const [emotionalProfile, setEmotionalProfile] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    axios.get('/api/userprofile/')
      .then(response => {
        setEmotionalProfile(response.data.emotional_profile);
        setLoading(false);
      })
      .catch(error => {
        setError('Failed to fetch emotional status.');
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    setEmotionalProfile(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    axios.put('/api/userprofile/', { emotional_profile: emotionalProfile })
      .then(response => {
        setSuccess('Emotional status updated successfully.');
      })
      .catch(error => {
        setError('Failed to update emotional status.');
      });
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container mt-4">
      <h2>Emotional Status</h2>
      {success && <div className="alert alert-success">{success}</div>}
      <form onSubmit={handleSubmit}>
        {/* Emotional Profile Textarea */}
        <div className="mb-3">
          <label htmlFor="emotional_profile" className="form-label">Your Emotional Profile</label>
          <textarea
            className="form-control"
            id="emotional_profile"
            name="emotional_profile"
            rows="5"
            value={emotionalProfile}
            onChange={handleChange}
            required
          ></textarea>
        </div>

        {/* Submit Button */}
        <button type="submit" className="btn btn-primary">Save Emotional Status</button>
      </form>
    </div>
  );
}

export default UserProfileEmotions;
