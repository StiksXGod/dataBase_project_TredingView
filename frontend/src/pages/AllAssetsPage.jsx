import React, { useEffect, useState } from 'react';
import { getAllAssets } from '../api/asset';

function AllAssetsPage() {
  const [assets, setAssets] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchAssets() {
      try {
        const data = await getAllAssets();
        setAssets(data.assets || []);
      } catch (err) {
        setError(err.message);
      }
    }
    fetchAssets();
  }, []);

  if (error) {
    return <div className="notification is-danger">{error}</div>;
  }

  if (!assets.length) {
    return <div>No assets found.</div>;
  }

  return (
    <div className="container" style={{ marginTop: '40px' }}>
      <h1 className="title">All Assets</h1>
      <table className="table is-fullwidth is-striped">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Name</th>
            <th>Image</th>
          </tr>
        </thead>
        <tbody>
          {assets.map((asset, i) => (
            <tr key={i}>
              <td>{asset.ticker}</td>
              <td>{asset.name}</td>
              <td>
                {asset.image_url ? <img src={asset.image_url} alt={asset.name} width="50" /> : 'No Image'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AllAssetsPage;
