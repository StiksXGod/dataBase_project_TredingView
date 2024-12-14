import React, { useState } from 'react';
import { deleteUser } from '../api/user';

function DeleteUserPage() {
  const [username, setUsername] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  const handleDelete = async (e) => {
    e.preventDefault();
    setStatusMessage('');
    try {
      const result = await deleteUser(username);
      setStatusMessage(`User with ID ${result.id} was deleted successfully.`);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  return (
    <div className="container" style={{ marginTop: '40px', maxWidth: '400px' }}>
      <h1 className="title">Delete User</h1>
      {statusMessage && <div className="notification is-info">{statusMessage}</div>}
      <form onSubmit={handleDelete}>
        <div className="field">
          <label className="label">Username to delete</label>
          <div className="control">
            <input
              className="input"
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
        </div>
        <div className="control">
          <button className="button is-danger" type="submit">Delete</button>
        </div>
      </form>
    </div>
  );
}

export default DeleteUserPage;
