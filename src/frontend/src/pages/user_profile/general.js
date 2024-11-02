import React, { useState, useEffect } from 'react';
import axios from 'axios';
import getCSRFToken from '../../libs/csrf';
import getContext from '../../libs/context';
import ProfileSideBar from '../../components/user_profile/side_bar_menu';

function UserProfileGeneral() {
  const csrftoken = getCSRFToken();
  const context = getContext();
  const profile_id = context['profile_id'];
  const api_url = '/api/profile/' + profile_id + '/';

  const [profile, setProfile] = useState({
    name: '',
    age: '',
    gender: '',
    gender_custom: '',
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
        setProfile({
          name: response.data.name,
          age: response.data.age,
          gender: response.data.gender,
          gender_custom: response.data.gender_custom,
        });
        setLoading(false);
      })
      .catch((error) => {
        setError('Failed to fetch profile data.');
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    axios
      .put(api_url, profile, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrftoken,
        },
      })
      .then((response) => {
        setSuccess('Profile updated successfully.');
      })
      .catch((error) => {
        setError('Failed to update profile.');
      });
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container mt-4">
      <div className="row">
        {/* Sidebar */}
        <div className="col-md-3">
          <ProfileSideBar active="general" />
        </div>
        {/* Main Content */}
        <div className="col-md-9">
          <h2>Personal General Information</h2>
          {success && <div className="alert alert-success">{success}</div>}
          <form onSubmit={handleSubmit}>
            {/* Name */}
            <div className="mb-3">
              <label htmlFor="name" className="form-label">
                Name
              </label>
              <input
                type="text"
                className="form-control"
                id="name"
                name="name"
                value={profile.name}
                onChange={handleChange}
                required
              />
            </div>

            {/* Age */}
            <div className="mb-3">
              <label htmlFor="age" className="form-label">
                Age
              </label>
              <input
                type="number"
                className="form-control"
                id="age"
                name="age"
                value={profile.age}
                onChange={handleChange}
                required
              />
            </div>

            {/* Gender */}
            <div className="mb-3">
              <label htmlFor="gender" className="form-label">
                Gender
              </label>
              <select
                className="form-select"
                id="gender"
                name="gender"
                value={profile.gender}
                onChange={handleChange}
              >
                <option value="">Select Gender</option>
                <option value="M">Male</option>
                <option value="F">Female</option>
                <option value="NB">Non-Binary</option>
                <option value="O">Other</option>
                <option value="C">Custom</option>
              </select>
            </div>

            {/* Custom Gender */}
            {profile.gender === 'C' && (
              <div className="mb-3">
                <label htmlFor="gender_custom" className="form-label">
                  Custom Gender
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="gender_custom"
                  name="gender_custom"
                  value={profile.gender_custom}
                  onChange={handleChange}
                  required
                />
              </div>
            )}

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary">
              Save Changes
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default UserProfileGeneral;
