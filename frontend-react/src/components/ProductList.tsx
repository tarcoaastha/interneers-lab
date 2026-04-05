import ProductCard from './ProductCard';

interface Product {
  id: number;
  title: string;
  brand: string;
  price: number;
  description: string;
}

const ProductList = () => {
  const products: Product[] = [
    { id: 1, title: "Gaming Mouse", brand: "Logitech", price: 59.99, description: "Wireless RGB mouse." },
    { id: 2, title: "Mechanical Keyboard", brand: "Razer", price: 129.99, description: "Clicky green switches." },
    { id: 3, title: "Noise Cancelling Headphones", brand: "Sony", price: 349.99, description: "Best-in-class ANC." },
    { id: 4, title: "Curved Monitor", brand: "Samsung", price: 499.99, description: "144Hz 4K Display." }
  ];

  return (
    <div style={{ 
      display: 'flex', 
      gap: '20px', 
      flexWrap: 'wrap', 
      justifyContent: 'center',
      padding: '20px'
    }}>
      {products.map((item) => (
        <ProductCard 
          key={item.id}
          title={item.title}
          brand={item.brand}
          price={item.price}
          description={item.description}
        />
      ))}
    </div>
  );
};

export default ProductList;