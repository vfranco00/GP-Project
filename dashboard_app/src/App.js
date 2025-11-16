import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Monitor from './pages/Monitor';
import Infra from './pages/Infra';

const styles = {
  nav: { 
    display: 'flex', justifyContent: 'center', gap: '20px', padding: '20px', 
    backgroundColor: '#121212', borderBottom: '1px solid #333' 
  },
  link: { 
    color: '#fff', textDecoration: 'none', fontSize: '1.1rem', fontWeight: 'bold', 
    padding: '10px 20px', borderRadius: '5px', backgroundColor: '#2c3e50' 
  },
  activeLink: { backgroundColor: '#3498db' }, // Opcional para melhorar visual depois
  main: { maxWidth: '1200px', margin: '0 auto' }
};

function App() {
  return (
    <Router>
      <div>
        {/* Menu de Navegação */}
        <nav style={styles.nav}>
          <Link to="/" style={styles.link}>🏠 Home</Link>
          <Link to="/monitor" style={styles.link}>🏎️ Monitoramento</Link>
          <Link to="/infra" style={styles.link}>📊 Infraestrutura</Link>
        </nav>

        {/* Área onde as páginas aparecem */}
        <div style={styles.main}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/monitor" element={<Monitor />} />
            <Route path="/infra" element={<Infra />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;