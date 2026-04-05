
const Header = () => {
  return (
    <header style={{
      backgroundColor: '#59799a',
      color: 'white',
      padding: '1rem 2rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
    }}>
      <h2 style={{ margin: 0 }}>Interneer's Lab</h2>
      
      <nav>
        <ul style={{
          display: 'flex',
          gap: '20px',
          listStyle: 'none',
          margin: 0,
          padding: 0
        }}>
          <li style={{ cursor: 'pointer', fontWeight: 'bold' }}>Dashboard</li>
          <li style={{ cursor: 'pointer', opacity: 0.8 }}>Orders</li>
          <li style={{ cursor: 'pointer', opacity: 0.8 }}>Settings</li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;