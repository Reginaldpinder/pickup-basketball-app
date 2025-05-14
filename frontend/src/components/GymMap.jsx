import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import axios from 'axios';

// Custom icons
const userIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  shadowSize: [41, 41],
});

const courtIcon = L.icon({
  iconUrl: '/icons/basketball.png',
  iconSize: [30, 30],
  iconAnchor: [15, 50],
  popupAnchor: [0, -50],
});

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

        axios
          .get(`http://localhost:8000/api/gyms/external/?lat=${coords.lat}&lon=${coords.lon}&radius=5000`)
          .then((res) => {
            setGyms(res.data);
          })
          .catch((err) => {
            console.error("Error fetching gyms:", err);
          });
      },
      (err) => {
        console.error("Location error:", err);
        setUserLocation([37.7749, -122.4194]); // Fallback
      }
    );
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Gyms Near You</h2>
      {userLocation ? (
        <MapContainer center={userLocation} zoom={13} style={{ height: '500px', width: '600%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={userLocation} icon={userIcon}>
            <Popup>You are here</Popup>
          </Marker>
          {gyms.map((gym, i) => (
            <Marker key={i} position={[gym.latitude, gym.longitude]} icon={courtIcon}>
              <Popup>{gym.name}</Popup>
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
