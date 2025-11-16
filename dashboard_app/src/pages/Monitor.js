import React, { useState, useEffect } from 'react';
import axios from 'axios';

const styles = {
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', padding: '20px' },
  card: { backgroundColor: '#1e1e1e', borderRadius: '10px', padding: '20px', boxShadow: '0 4px 6px rgba(0,0,0,0.3)' },
  carTitle: { color: '#f1c40f', margin: '0 0 15px 0', borderBottom: '1px solid #333', paddingBottom: '10px' },
  tireGrid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' },
  tireBox: { backgroundColor: '#2c3e50', padding: '8px', borderRadius: '5px', textAlign: 'center' },
  tireValue: { fontSize: '1.1rem', fontWeight: 'bold' },
  tempHot: { color: '#e74c3c' },
  tempOk: { color: '#2ecc71' }
};

function Monitor() {
  const [cars, setCars] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8001/dashboard/all');
        setCars(response.data);
      } catch (error) { console.error("Erro API", error); }
    };
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  if (cars.length === 0) return <h2 style={{textAlign:'center', marginTop:'50px'}}>Aguardando telemetria...</h2>;

  return (
    <div style={styles.grid}>
      {cars.map((car) => (
        <div key={car.car_id} style={styles.card}>
          <h2 style={styles.carTitle}>{car.car_id.toUpperCase()}</h2>
          <div style={styles.tireGrid}>
            {Object.entries(car.tires).map(([position, data]) => (
              <div key={position} style={styles.tireBox}>
                <div style={{fontSize:'0.8rem', color:'#bdc3c7'}}>{position}</div>
                <div style={styles.tireValue}>
                  <span style={data.temp > 100 ? styles.tempHot : styles.tempOk}>{data.temp}°C</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Monitor;