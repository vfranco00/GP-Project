import React, { useState, useEffect } from 'react';
import axios from 'axios';

const styles = {
  container: { padding: '20px', color: '#fff' },
  flexBox: { display: 'flex', gap: '20px', flexWrap: 'wrap', marginTop: '20px' },
  tableBox: { flex: 1, backgroundColor: '#1e1e1e', padding: '20px', borderRadius: '10px', minWidth: '300px' },
  table: { width: '100%', borderCollapse: 'collapse' },
  th: { textAlign: 'left', borderBottom: '1px solid #555', padding: '10px', color: '#3498db' },
  td: { borderBottom: '1px solid #333', padding: '10px' },
  barContainer: { backgroundColor: '#333', height: '8px', borderRadius: '4px', marginTop: '5px' },
  barFill: { height: '100%', backgroundColor: '#2ecc71', borderRadius: '4px' }
};

function Infra() {
  const [infra, setInfra] = useState({ isccp: [], ssacp: [] });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8001/system/stats');
        setInfra(response.data);
      } catch (error) { console.error("Erro API Infra", error); }
    };
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  const renderBar = (count) => {
    const width = Math.min((count / 50) * 100, 100) + '%';
    return <div style={styles.barContainer}><div style={{...styles.barFill, width}}></div></div>;
  };

  return (
    <div style={styles.container}>
      <h2 style={{textAlign: 'center'}}>Status da Infraestrutura Distribuída</h2>
      <div style={styles.flexBox}>
        
        {/* Tabela ISCCP */}
        <div style={styles.tableBox}>
          <h3>ISCCP (Gateways)</h3>
          <table style={styles.table}>
            <thead><tr><th style={styles.th}>ID</th><th style={styles.th}>Pacotes Processados</th></tr></thead>
            <tbody>
              {infra.isccp?.map((item) => (
                <tr key={item._id}>
                  <td style={styles.td}>{item._id}</td>
                  <td style={styles.td}>{item.count}{renderBar(item.count)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Tabela SSACP */}
        <div style={styles.tableBox}>
          <h3>SSACP (Storage Nodes)</h3>
          <table style={styles.table}>
            <thead><tr><th style={styles.th}>Node ID</th><th style={styles.th}>Dados Persistidos</th></tr></thead>
            <tbody>
              {infra.ssacp?.map((item) => (
                <tr key={item._id}>
                  <td style={styles.td}>{item._id}</td>
                  <td style={styles.td}>{item.count}{renderBar(item.count)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
}

export default Infra;