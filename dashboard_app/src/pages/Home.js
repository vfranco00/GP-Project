import React from 'react';

const styles = {
  container: { padding: '40px', textAlign: 'center', color: '#fff' },
  title: { fontSize: '3rem', color: '#f1c40f', marginBottom: '20px' },
  infoBox: { backgroundColor: '#1e1e1e', padding: '20px', borderRadius: '10px', maxWidth: '800px', margin: '0 auto', border: '1px solid #333' },
  text: { fontSize: '1.2rem', lineHeight: '1.8', color: '#bdc3c7' },
  highlight: { color: '#3498db', fontWeight: 'bold' }
};

function Home() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Grande Prêmio F1 Brasil 🇧🇷</h1>
      <div style={styles.infoBox}>
        <h2>Circuito de Interlagos</h2>
        <p style={styles.text}>
          Bem-vindo ao sistema oficial de monitoramento de pneus.
          <br/><br/>
          📏 <strong>Extensão da Pista:</strong> <span style={styles.highlight}>4.309 km</span>
          <br/>
          🏎️ <strong>Carros na Pista:</strong> <span style={styles.highlight}>24 (2 por equipe)</span>
          <br/>
          ⚡ <strong>Velocidade Média Histórica:</strong> <span style={styles.highlight}>~216 km/h</span>
        </p>
        <p style={{marginTop: '20px', fontSize: '0.9rem', color: '#7f8c8d'}}>
          Utilize o menu acima para navegar entre o monitoramento em tempo real e o status da infraestrutura distribuída.
        </p>
      </div>
    </div>
  );
}

export default Home;