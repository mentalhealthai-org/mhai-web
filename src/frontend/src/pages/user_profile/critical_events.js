import React, { useState, useEffect } from 'react';
import axios from 'axios';

import getCSRFToken from '../../libs/csrf';
import getContext from '../../libs/context';
import ProfileSideBar from '../../components/user_profile/side_bar_menu';

function UserProfileCriticalEvents() {
  const csrftoken = getCSRFToken();
  const context = getContext();
  const profile_id = context['profile_id'];
  const api_url = `/api/profile/critical-events/${profile_id}/`;

  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formError, setFormError] = useState('');
  const [success, setSuccess] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [currentEvent, setCurrentEvent] = useState(null);

  const [formData, setFormData] = useState({
    date: '',
    description: '',
    impact: '',
    resolved: false,
    treated: false,
  });

  useEffect(() => {
    axios
      .get(api_url, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrftoken,
        },
      })
      .then((response) => {
        setEvents(response.data);
        setLoading(false);
      })
      .catch((error) => {
        setError('Failed to fetch critical events.');
        setLoading(false);
      });
  }, [api_url, csrftoken]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    setFormError('');
    setSuccess('');

    const method = currentEvent ? 'put' : 'post';
    const url = currentEvent ? `${api_url}${currentEvent.id}/` : api_url;

    axios({
      method: method,
      url: url,
      data: formData,
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrftoken,
      },
    })
      .then((response) => {
        setSuccess(`Event ${currentEvent ? 'updated' : 'added'} successfully.`);
        setShowForm(false);
        setCurrentEvent(null);
        // Refresh the events list
        return axios.get(api_url, {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrftoken,
          },
        });
      })
      .then((response) => {
        setEvents(response.data);
      })
      .catch((error) => {
        setFormError('Failed to submit event.');
      });
  };

  const handleEdit = (event) => {
    setCurrentEvent(event);
    setFormData({
      date: event.date,
      description: event.description,
      impact: event.impact,
      resolved: event.resolved,
      treated: event.treated,
    });
    setShowForm(true);
  };

  const handleDelete = (eventId) => {
    if (window.confirm('Are you sure you want to delete this event?')) {
      axios
        .delete(`${api_url}${eventId}/`, {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrftoken,
          },
        })
        .then((response) => {
          setSuccess('Event deleted successfully.');
          // Refresh the events list
          return axios.get(api_url, {
            withCredentials: true,
            headers: {
              'X-CSRFToken': csrftoken,
            },
          });
        })
        .then((response) => {
          setEvents(response.data);
        })
        .catch((error) => {
          setError('Failed to delete event.');
        });
    }
  };

  const handleAddNew = () => {
    setCurrentEvent(null);
    setFormData({
      date: '',
      description: '',
      impact: '',
      resolved: false,
      treated: false,
    });
    setShowForm(true);
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container mt-4">
      <div className="row">
        {/* Sidebar */}
        <div className="col-md-3">
          <ProfileSideBar active="critical-events" />
        </div>
        {/* Main Content */}
        <div className="col-md-9">
          <h2>Personal Critical Events</h2>
          {success && <div className="alert alert-success">{success}</div>}
          {error && <div className="alert alert-danger">{error}</div>}
          <button className="btn btn-primary mb-3" onClick={handleAddNew}>
            Add New Event
          </button>
          {/* Events List */}
          {events.length > 0 ? (
            <div className="list-group mb-3">
              {events.map((event) => (
                <div key={event.id} className="list-group-item">
                  <h5 className="mb-1">Date: {event.date}</h5>
                  <p className="mb-1"><strong>Description:</strong> {event.description}</p>
                  <p className="mb-1"><strong>Impact:</strong> {event.impact}</p>
                  <p className="mb-1">
                    <strong>Resolved:</strong> {event.resolved ? 'Yes' : 'No'}
                  </p>
                  <p className="mb-1">
                    <strong>Treated:</strong> {event.treated ? 'Yes' : 'No'}
                  </p>
                  <button
                    className="btn btn-sm btn-secondary me-2"
                    onClick={() => handleEdit(event)}
                  >
                    Edit
                  </button>
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => handleDelete(event.id)}
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <p>No critical events found.</p>
          )}
          {/* Event Form */}
          {showForm && (
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">
                  {currentEvent ? 'Edit Event' : 'Add New Event'}
                </h5>
                {formError && <div className="alert alert-danger">{formError}</div>}
                <form onSubmit={handleFormSubmit}>
                  {/* Date */}
                  <div className="mb-3">
                    <label htmlFor="date" className="form-label">
                      Date
                    </label>
                    <input
                      type="date"
                      className="form-control"
                      id="date"
                      name="date"
                      value={formData.date}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  {/* Description */}
                  <div className="mb-3">
                    <label htmlFor="description" className="form-label">
                      Description
                    </label>
                    <textarea
                      className="form-control"
                      id="description"
                      name="description"
                      rows="3"
                      value={formData.description}
                      onChange={handleInputChange}
                      required
                    ></textarea>
                  </div>
                  {/* Impact */}
                  <div className="mb-3">
                    <label htmlFor="impact" className="form-label">
                      Impact
                    </label>
                    <textarea
                      className="form-control"
                      id="impact"
                      name="impact"
                      rows="3"
                      value={formData.impact}
                      onChange={handleInputChange}
                      required
                    ></textarea>
                  </div>
                  {/* Resolved */}
                  <div className="form-check mb-3">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      id="resolved"
                      name="resolved"
                      checked={formData.resolved}
                      onChange={handleInputChange}
                    />
                    <label className="form-check-label" htmlFor="resolved">
                      Resolved
                    </label>
                  </div>
                  {/* Treated */}
                  <div className="form-check mb-3">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      id="treated"
                      name="treated"
                      checked={formData.treated}
                      onChange={handleInputChange}
                    />
                    <label className="form-check-label" htmlFor="treated">
                      Treated
                    </label>
                  </div>
                  {/* Submit Button */}
                  <button type="submit" className="btn btn-primary me-2">
                    {currentEvent ? 'Update Event' : 'Add Event'}
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => {
                      setShowForm(false);
                      setCurrentEvent(null);
                      setFormError('');
                    }}
                  >
                    Cancel
                  </button>
                </form>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default UserProfileCriticalEvents;
