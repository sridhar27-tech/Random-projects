'use client'
import { useState } from 'react'

export default function Cart() {
  const [cart, setCart] = useState([
    { id: '1', name: 'Aura Glow Watch', price: 199.99, quantity: 1 },
    { id: '2', name: 'Nebula Headphones', price: 299.99, quantity: 1 },
  ])

  const total = cart.reduce((acc, item) => acc + item.price * item.quantity, 0)

  return (
    <div className="container" style={{ marginTop: '4rem' }}>
      <h1 className="gradient-text" style={{ fontSize: '3rem', marginBottom: '2rem' }}>Your Bag.</h1>
      
      <div className="glass" style={{ padding: '2rem' }}>
        {cart.length === 0 ? (
          <p>Your cart is looking a bit empty.</p>
        ) : (
          <div>
            {cart.map(item => (
              <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 0', borderBottom: '1px solid var(--glass-border)' }}>
                <div>
                  <h3 style={{ fontSize: '1.5rem' }}>{item.name}</h3>
                  <p style={{ color: 'var(--text-muted)' }}>Quantity: {item.quantity}</p>
                </div>
                <p style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--primary)' }}>${item.price}</p>
              </div>
            ))}
            
            <div style={{ marginTop: '2rem', textAlign: 'right' }}>
              <h2 style={{ fontSize: '2rem' }}>Total: <span className="gradient-text">${total.toFixed(2)}</span></h2>
              <button className="btn btn-primary" style={{ marginTop: '2rem', padding: '1.2rem 3rem', fontSize: '1.2rem' }}>
                Secure Checkout
              </button>
            </div>
          </div>
        )}
      </div>

      <section style={{ marginTop: '4rem' }}>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>You might also like...</h2>
        <div className="product-grid">
           {/* Recs would go here */}
           <div className="product-card glass" style={{ opacity: 0.7 }}>
             <p>Analyzing behavior...</p>
           </div>
        </div>
      </section>
    </div>
  )
}
