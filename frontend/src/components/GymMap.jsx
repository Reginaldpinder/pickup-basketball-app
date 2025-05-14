import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import axios from 'axios';

const GymMap = () => {
  const [gyms, setGyms] = useState([]);
  const [userLocation, setUserLocation] = useState(null);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const coords = {
          lat: position.coords.latitude,
          lon: position.coords.longitude,
        };
        setUserLocation([coords.lat, coords.lon]);

        axios.get(`http://localhost:8000/api/gyms/nearby/?lat=${coords.lat}&lon=${coords.lon}&radius=50`)
          .then((res) => {
            setGyms(res.data);
          })
          .catch((err) => {
            console.error("Error fetching gyms:", err);
          });
      },
      (err) => {
        console.error("Location error:", err);
        setUserLocation([37.7749, -122.4194]); // fallback: San Francisco
      }
    );
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Gyms Near You</h2>
      {userLocation ? (
        <MapContainer center={userLocation} zoom={13} style={{ height: '500px', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={userLocation}>
            <Popup>You are here</Popup>
          </Marker>
          {gyms.map((gym) => (
            <Marker key={gym.id} position={[gym.latitude, gym.longitude]}>
              <Popup>
                <strong>{gym.name}</strong><br />
                {gym.location}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      ) : (
        <p>Fetching your location...</p>
      )}
    </div>
  );
};

export default GymMap;
