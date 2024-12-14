import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function RegisterForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('user');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_';
  const USERNAME_MIN_LEN = 5;
  const USERNAME_MAX_LEN = 18;
  const PASSWORD_MIN_LEN = 8;
  const PASSWORD_MAX_LEN = 22;

  const validateInput = () => {
    if (username.length < USERNAME_MIN_LEN || username.length > USERNAME_MAX_LEN) {
      return `Username length must be between ${USERNAME_MIN_LEN} and ${USERNAME_MAX_LEN} characters.`;
    }
    if (![...username].every(char => ALLOWED_CHARACTERS.includes(char))) {
      return 'Username contains invalid characters.';
    }

    if (password.length < PASSWORD_MIN_LEN || password.length > PASSWORD_MAX_LEN) {
      return `Password length must be between ${PASSWORD_MIN_LEN} and ${PASSWORD_MAX_LEN} characters.`;
    }
    if (![...password].every(char => ALLOWED_CHARACTERS.includes(char))) {
      return 'Password contains invalid characters.';
    }

    return '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    const validationError = validateInput();
    if (validationError) {
      setError(validationError);
      return;
    }

    const payload = { username, password, role };

    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Registration failed.');
      }

      const data = await response.json();
      setSuccessMessage(data.message || 'User created successfully.');
      setUsername('');
      setPassword('');
      setRole('user');
      
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <section className="hero is-fullheight is-primary is-bold" style={{ background: 'linear-gradient(141deg, #667eea 0%, #764ba2 100%)' }}>
      <div className="hero-body">
        <div className="container">
          <div className="columns is-centered">
            <div className="column is-5-tablet is-4-desktop is-4-widescreen">
              <div className="card" style={{ borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.2)' }}>
                <header className="card-header">
                  <p className="card-header-title has-text-centered is-size-4" style={{ width: '100%', justifyContent: 'center' }}>
                    Register Your Account
                  </p>
                </header>
                <div className="card-content">
                  {error && <div className="notification is-danger is-light">{error}</div>}
                  {successMessage && <div className="notification is-success is-light">{successMessage}</div>}

                  <form onSubmit={handleSubmit}>
                    <div className="field">
                      <label className="label has-text-grey-darker">Username</label>
                      <div className="control has-icons-left">
                        <input
                          className="input is-rounded"
                          type="text"
                          placeholder="e.g. johndoe"
                          value={username}
                          onChange={(e) => setUsername(e.target.value)}
                          required
                          style={{ borderColor: '#ccc' }}
                        />
                        <span className="icon is-small is-left">
                          <i className="fas fa-user"></i>
                        </span>
                      </div>
                      <p className="help">
                        Length: {USERNAME_MIN_LEN}-{USERNAME_MAX_LEN}, allowed: letters, digits, underscore.
                      </p>
                    </div>

                    <div className="field">
                      <label className="label has-text-grey-darker">Password</label>
                      <div className="control has-icons-left">
                        <input
                          className="input is-rounded"
                          type="password"
                          placeholder="Your secure password"
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          required
                          style={{ borderColor: '#ccc' }}
                        />
                        <span className="icon is-small is-left">
                          <i className="fas fa-lock"></i>
                        </span>
                      </div>
                      <p className="help">
                        Length: {PASSWORD_MIN_LEN}-{PASSWORD_MAX_LEN}, allowed: letters, digits, underscore.
                      </p>
                    </div>

                    <div className="field">
                      <label className="label has-text-grey-darker">Role</label>
                      <div className="control has-icons-left">
                        <div className="select is-fullwidth is-rounded">
                          <select value={role} onChange={(e) => setRole(e.target.value)}>
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                          </select>
                        </div>
                        <span className="icon is-small is-left">
                          <i className="fas fa-user-shield"></i>
                        </span>
                      </div>
                      <p className="help">Choose an appropriate role.</p>
                    </div>

                    <div className="field is-grouped is-grouped-centered">
                      <div className="control">
                        <button className="button is-primary is-rounded" type="submit">
                          <span className="icon is-small">
                            <i className="fas fa-check"></i>
                          </span>
                          <span>Register</span>
                        </button>
                      </div>
                    </div>
                  </form>
                </div>
                <footer className="card-footer" style={{ justifyContent: 'center' }}>
                  <p className="card-footer-item">
                    <span className="has-text-grey-dark">
                      Already have an account? <Link to="/login" className="has-text-link">Login here</Link>
                    </span>
                  </p>
                </footer>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default RegisterForm;
