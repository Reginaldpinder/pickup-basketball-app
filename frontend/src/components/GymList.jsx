import React, { useState } from 'react';
import axios from 'axios';

const GymList= () => {
  const [gyms, setGyms] = useState([]);
  const [zip, setZip] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const searchByLocation = () => {
    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        axios.get(`http://localhost:8000/api/gyms/nearby/?lat=${latitude}&lon=${longitude}&radius=25`)
          .then(res => {
            setGyms(res.data);
            setLoading(false);
          })
          .catch(() => {
            setError('Failed to fetch gyms by location.');
            setLoading(false);
          });
      },
      () => {
        setError('Location permission denied.');
        setLoading(false);
      }
    );
  };

  const searchByZip = () => {
    setLoading(true);
    axios.get(`http://localhost:8000/api/gyms/nearby/?zip=${zip}`)
      .then(res => {
        setGyms(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError('Invalid zip code.');
        setLoading(false);
      });
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-2">Find Nearby Gyms</h1>

      <div className="flex space-x-2 mb-4">
        <input
          type="text"
          placeholder="Enter ZIP code"
          value={zip}
          onChange={(e) => setZip(e.target.value)}
          className="border rounded p-2"
        />
        <button onClick={searchByZip} className="bg-blue-500 text-white px-4 py-2 rounded">
          Search by ZIP
        </button>
        <button onClick={searchByLocation} className="bg-green-500 text-white px-4 py-2 rounded">
          Use My Location
        </button>
      </div>

      {loading && <p>Loading gyms...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <ul className="space-y-2">
        {gyms.map(gym => (
          <li key={gym.id} className="bg-gray-100 p-2 rounded shadow">
            <strong>{gym.name}</strong><br />
            {gym.location}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GymList;

