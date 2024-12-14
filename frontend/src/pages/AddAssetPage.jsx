import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { addAsset } from '../api/asset'; // Импортируйте свою функцию добавления ассета

function AddAssetPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  // Состояния для всех полей ассета
  const [ticker, setTicker] = useState('');
  const [name, setName] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [typeId, setTypeId] = useState('');
  const [exchangeId, setExchangeId] = useState('');
  const [descriptions, setDescriptions] = useState('');

  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleAddAsset = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    // Приводим поля с числовыми значениями к числу
    const payload = {
      ticker: ticker.trim(),
      name: name.trim(),
      image_url: imageUrl.trim(),
      type_id: parseInt(typeId, 10),
      exchange_id: parseInt(exchangeId, 10),
      descriptions: descriptions.trim()
    };

    // Валидация полей, если нужно
    if (!payload.ticker || !payload.name || !payload.image_url || isNaN(payload.type_id) || isNaN(payload.exchange_id) || !payload.descriptions) {
      setError('All fields are required and must be valid.');
      return;
    }

    try {
      const data = await addAsset(payload);
      setMessage(`Asset added successfully with ID: ${data.id}`);
      // Можно вернуться к профилю пользователя при необходимости:
      // navigate(`/id/${id}`)
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container" style={{ marginTop: '40px', maxWidth: '500px' }}>
      <div className="box" style={{ borderRadius: '8px' }}>
        <h1 className="title has-text-centered">Add Asset</h1>
        {error && <div className="notification is-danger">{error}</div>}
        {message && <div className="notification is-success">{message}</div>}
        <form onSubmit={handleAddAsset}>
          <div className="field">
            <label className="label">Ticker</label>
            <div className="control">
              <input
                className="input"
                type="text"
                placeholder="Enter ticker"
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="field">
            <label className="label">Name</label>
            <div className="control">
              <input
                className="input"
                type="text"
                placeholder="Enter asset name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="field">
            <label className="label">Image URL</label>
            <div className="control">
              <input
                className="input"
                type="url"
                placeholder="Enter image URL"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="field">
            <label className="label">Type ID</label>
            <div className="control">
              <input
                className="input"
                type="number"
                placeholder="Enter type ID"
                value={typeId}
                onChange={(e) => setTypeId(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="field">
            <label className="label">Exchange ID</label>
            <div className="control">
              <input
                className="input"
                type="number"
                placeholder="Enter exchange ID"
                value={exchangeId}
                onChange={(e) => setExchangeId(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="field">
            <label className="label">Descriptions</label>
            <div className="control">
              <textarea
                className="textarea"
                placeholder="Enter descriptions"
                value={descriptions}
                onChange={(e) => setDescriptions(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="field is-grouped is-grouped-centered" style={{ marginTop: '20px' }}>
            <div className="control">
              <button className="button is-primary" type="submit">Add</button>
            </div>
            <div className="control">
              <button
                className="button is-light"
                type="button"
                onClick={() => navigate(`/id/${id}`)}
              >
                Back to Profile
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddAssetPage;
