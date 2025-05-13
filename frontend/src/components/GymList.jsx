import React, { useEffect, useState } from 'react';
import axios from 'axios';

const GymList = () => {
  const [gyms, setGyms] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/gyms/')
      .then(response => {
        setGyms(response.data);
      })
      .catch(error => {
        console.error('Error fetching gyms:', error);
      });
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Available Gyms</h1>
      {gyms.length === 0 ? (
        <p>No gyms available.</p>
      ) : (
        <ul className="space-y-2">
          {gyms.map(gym => (
            <li key={gym.id} className="bg-gray-100 p-2 rounded shadow">
              <strong>{gym.name}</strong> — {gym.location}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default GymList;
