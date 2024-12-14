import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getUserInfo } from '../api/user';

function formatDate(isoDateString) {
  const date = new Date(isoDateString);
  const options = {
    year: 'numeric',
    month: 'long', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZoneName: 'short',
  };
  return date.toLocaleString(undefined, options);
}

function UserProfilePage() {
  const { id } = useParams();
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getUserInfo(id);
        setUserData(data);
      } catch (err) {
        setError(err.message);
      }
    }
    if (id) fetchData();
  }, [id]);

  if (error) {
    return (
      <div className="container" style={{ marginTop: '40px' }}>
        <div className="notification is-danger">{error}</div>
        <button className="button" onClick={() => navigate('/login')}>Go to Login</button>
      </div>
    );
  }

  if (!userData) {
    return (
      <div className="container" style={{ marginTop: '40px' }}>
        <progress className="progress is-small is-primary" max="100">Loading</progress>
      </div>
    );
  }

  return (
    <div className="container" style={{ marginTop: '40px', maxWidth: '500px' }}>
      <div className="box" style={{ borderRadius: '8px' }}>
        <h1 className="title has-text-centered">User Profile</h1>
        <p><strong>ID:</strong> {userData.id}</p>
        <p><strong>Username:</strong> {userData.username}</p>
        <p><strong>Role:</strong> {userData.role}</p>
        <p><strong>Created At:</strong> {formatDate(userData.created_at)}</p>
        <p className="has-text-success"><strong>{userData.message}</strong></p>
        
        <div className="field is-grouped is-grouped-centered" style={{ marginTop: '20px' }}>
          <div className="control">
            <Link className="button is-link" to={`/id/${id}/add`}>Add Asset</Link>
          </div>
          <div className="control">
            <Link className="button is-info" to="/assets">View All Assets</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserProfilePage;
