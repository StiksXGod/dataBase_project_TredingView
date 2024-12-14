import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../api/auth';

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

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

    const validationError = validateInput();
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      // loginUser должен возвращать user_id или декодированный токен, из которого вы можете получить user_id.
      const data = await loginUser(username, password);
      // Предположим, что ответ при логине содержит user_id:
      const userId = data.user_id; 
      if (!userId) {
        throw new Error('User ID not found in login response');
      }

      // Сохраняем user_id
      localStorage.setItem('user_id', userId);

      // Перенаправляем на /id/{userId}
      navigate(`/id/${userId}`);
    } catch (err) {
      console.error('Login error:', err);
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
                    Login to Your Account
                  </p>
                </header>
                <div className="card-content">
                  {error && <div className="notification is-danger is-light">{error}</div>}
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
                    </div>

                    <div className="field is-grouped is-grouped-centered">
                      <div className="control">
                        <button className="button is-primary is-rounded" type="submit">
                          <span className="icon is-small">
                            <i className="fas fa-sign-in-alt"></i>
                          </span>
                          <span>Login</span>
                        </button>
                      </div>
                    </div>
                  </form>
                </div>
                <footer className="card-footer" style={{ justifyContent: 'center' }}>
                  <p className="card-footer-item">
                    <span className="has-text-grey-dark">
                      Don’t have an account? <a href="/register" className="has-text-link">Register here</a>
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

export default LoginForm;
