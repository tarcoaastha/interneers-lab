
import ProductList from './components/ProductList';
import Header from './components/Header'; 
//commenting out old code for reference. We will be replacing it with a more structured layout using Header and ProductList components.

// function App() {
//   return (
//     <div style={{ padding: '40px' }}>
//       <h1>My Tech Store</h1>
//       <div style={{ display: 'flex', gap: '20px' }}>
        
//         <ProductCard 
//           title="Gaming Mouse" 
//           brand="Logitech" 
//           price={59.99} 
//           description="Very fast mouse." 
//         />

//         <ProductCard 
//           title="Mechanical Keyboard" 
//           brand="Razer" 
//           price={129.99} 
//           description="Clicky and tactile." 
//         />

//         <ProductCard 
//           title="Noise Cancelling Headphones" 
//           brand="Sony" 
//           price={349.99} 
//           description="Pure silence." 
//         />

//       </div>
//     </div>
//   );
// }






// function App() {
//   return (
//     <div style={{ 
//       padding: '40px', 
//       backgroundColor: '#f8f9fa', 
//       minHeight: '100vh',
//       fontFamily: 'sans-serif'
//     }}>
//       <h1 style={{ textAlign: 'center', color: '#333', marginBottom: '40px' }}>
//         Inventory Dashboard (React + TS)
//       </h1>
      
//       <div style={{ 
//         display: 'flex', 
//         gap: '20px', 
//         justifyContent: 'center', 
//         flexWrap: 'wrap' 
//       }}>
        
//         <ProductCard 
//           title="Gaming Mouse" 
//           brand="Logitech" 
//           price={59.99} 
//           description="A high-precision wireless mouse with customizable RGB lighting and 25k DPI sensor." 
//         />

//         <ProductCard 
//           title="Mechanical Keyboard" 
//           brand="Razer" 
//           price={129.99} 
//           description="Tactile and clicky switches with individual per-key lighting and a durable aluminum frame." 
//         />

//         <ProductCard 
//           title="Noise Cancelling Headphones" 
//           brand="Sony" 
//           price={349.99} 
//           description="Industry-leading noise cancellation with 30 hours of battery life and touch sensor controls." 
//         />

//       </div>
//     </div>
//   );
// }




function App() {
  return (
    <div style={{ backgroundColor: '#f4f7f6', minHeight: '100vh' }}>
      <Header />
      
      <main style={{ padding: '20px' }}>
        <h1 style={{ 
          textAlign: 'center', 
          color: '#2c3e50', 
          margin: '30px 0' 
        }}>
          Product Inventory
        </h1>
        <ProductList />
      </main>

      <footer style={{ textAlign: 'center', padding: '40px', color: '#999', fontSize: '0.8rem' }}>
        &copy; 2026 Interneer's Lab Inventory Management
      </footer>
    </div>
  );
}

export default App;