import { useState } from 'react';

//commented this because I am using a new version of ProductCard with state and interactivity as mentioned in further task.
// interface ProductProps {
//   title: string;
//   brand: string;
//   price: number;
//   description: string;
// }

// const ProductCard = ({ title, brand, price, description }: ProductProps) => {
//   return (
//     <div style={{ 
//       border: '1px solid #ddd', 
//       padding: '20px', 
//       borderRadius: '8px', 
//       width: '280px',
//       boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
//     }}>
//       <h3>{title}</h3>
//       <p style={{ color: '#777', fontSize: '0.9rem' }}>{brand}</p>
//       <p>{description}</p>
//       <p style={{ fontWeight: 'bold' }}>${price}</p>
//     </div>
//   );
// };

// export default ProductCard;


interface ProductProps {
  title: string;
  brand: string;
  price: number;
  description: string;
}

const ProductCard = ({ title, brand, price, description }: ProductProps) => {
  // STATE DEFINITION
  // 'isExpanded' is the variable, 'setIsExpanded' is the function to change it.
  // It starts as 'false' (collapsed).
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div 
      // EVENT HANDLER
      // When the user clicks anywhere on the card, toggle the state.
      onClick={() => setIsExpanded(!isExpanded)} 
      style={{ 
        border: '2px solid',
        // 3. DYNAMIC STYLING
        // If isExpanded is true, use blue. If false, use light grey.
        borderColor: isExpanded ? '#3498db' : '#ddd', 
        padding: '20px', 
        borderRadius: '12px', 
        width: '300px',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        backgroundColor: 'white',
        boxShadow: isExpanded ? '0 10px 20px rgba(0,0,0,0.1)' : '0 4px 6px rgba(0,0,0,0.05)'
      }}
    >
      <h3 style={{ margin: '0 0 5px 0', color: '#2c3e50' }}>{title}</h3>
      <p style={{ color: '#777', fontSize: '0.9rem', marginBottom: '10px' }}>{brand}</p>
      
      {/* CONDITIONAL RENDERING
          This part only appears in the HTML if isExpanded is TRUE. */}
      {isExpanded && (
        <div style={{ 
          marginTop: '15px', 
          borderTop: '1px solid #eee', 
          paddingTop: '15px' 
        }}>
          <p style={{ fontSize: '0.95rem', color: '#555', lineHeight: '1.4' }}>
            {description}
          </p>
          <p style={{ 
            fontWeight: 'bold', 
            color: '#2c3e50', 
            marginTop: '15px',
            fontSize: '1.1rem' 
          }}>
            Price: ${price}
          </p>
        </div>
      )}

      <p style={{ 
        fontSize: '0.75rem', 
        color: '#3498db', 
        marginTop: '15px',
        fontWeight: 'bold',
        textAlign: 'right'
      }}>
        {isExpanded ? 'Click to collapse ▲' : 'Click for details ▼'}
      </p>
    </div>
  );
};

export default ProductCard;