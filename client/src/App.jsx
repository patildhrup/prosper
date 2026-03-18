import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [balance, setBalance] = useState({ balance: '0.00', availableBalance: '0.00' });
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('offline');
  const [order, setOrder] = useState({
    symbol: 'BTCUSDT',
    quantity: '0.1',
    type: 'MARKET',
    price: '',
    stop: ''
  });

  const fetchBalance = async () => {
    try {
      const res = await fetch(`${API_BASE}/balance`);
      const data = await res.json();
      if (res.ok) {
        setBalance(data);
        setStatus('online');
      } else {
        setStatus('offline');
      }
    } catch (err) {
      console.error("Balance fetch failed", err);
      setStatus('offline');
    }
  };

  const fetchLogs = async () => {
    try {
      const res = await fetch(`${API_BASE}/logs`);
      const data = await res.json();
      if (res.ok) setLogs(data);
    } catch (err) {
      console.error("Logs fetch failed", err);
    }
  };

  useEffect(() => {
    fetchBalance();
    fetchLogs();
    const interval = setInterval(() => {
      fetchBalance();
      fetchLogs();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleOrder = async (side) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: order.symbol,
          side: side,
          order_type: order.type,
          quantity: parseFloat(order.quantity),
          price: order.price ? parseFloat(order.price) : null,
          stop_price: order.stop ? parseFloat(order.stop) : null
        })
      });
      const data = await res.json();
      if (res.ok) {
        alert("Order Placed Successfully!");
        fetchBalance();
        fetchLogs();
      } else {
        alert(`Error: ${data.detail}`);
      }
    } catch (err) {
      alert("Execution failed script error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <header>
        <div className="logo">
          <div className="logo-icon">💠</div>
          PROSPER <span style={{fontSize: '14px', fontWeight: '400', color: '#666'}}>TRADING BOT</span>
          <span className={`status-dot ${status}`}></span>
        </div>
        <div className="balance-card">
          <div className="balance-label">USDT BALANCE</div>
          <div className="balance-value">{balance.balance}</div>
          <div className="balance-label" style={{fontSize: '11px'}}>Available: {balance.availableBalance}</div>
        </div>
      </header>

      <div className="main-content">
        <div className="panel">
          <h2 className="panel-title">⚡ PLACE ORDER</h2>
          
          <div className="form-group">
            <label>Symbol</label>
            <input 
              type="text" 
              value={order.symbol} 
              onChange={(e) => setOrder({...order, symbol: e.target.value})}
              placeholder="BTCUSDT"
            />
          </div>

          <div className="form-group">
            <label>Order Type</label>
            <select value={order.type} onChange={(e) => setOrder({...order, type: e.target.value})}>
              <option value="MARKET">MARKET</option>
              <option value="LIMIT">LIMIT</option>
              <option value="STOP_MARKET">STOP_MARKET</option>
            </select>
          </div>

          <div className="form-group">
            <label>Quantity</label>
            <input 
              type="text" 
              value={order.quantity} 
              onChange={(e) => setOrder({...order, quantity: e.target.value})}
              placeholder="0.1"
            />
          </div>

          {order.type === 'LIMIT' && (
            <div className="form-group">
              <label>Price</label>
              <input 
                type="text" 
                value={order.price} 
                onChange={(e) => setOrder({...order, price: e.target.value})}
                placeholder="60000"
              />
            </div>
          )}

          {order.type === 'STOP_MARKET' && (
            <div className="form-group">
              <label>Stop Price</label>
              <input 
                type="text" 
                value={order.stop} 
                onChange={(e) => setOrder({...order, stop: e.target.value})}
                placeholder="55000"
              />
            </div>
          )}

          <div className="button-group">
            <button 
              className="btn btn-buy" 
              onClick={() => handleOrder('BUY')}
              disabled={loading}
            >
              {loading ? 'Executing...' : 'BUY / LONG'}
            </button>
            <button 
              className="btn btn-sell" 
              onClick={() => handleOrder('SELL')}
              disabled={loading}
            >
              {loading ? 'Executing...' : 'SELL / SHORT'}
            </button>
          </div>
        </div>

        <div className="panel list-panel">
          <h2 className="panel-title">📜 RECENT ACTIVITY</h2>
          <div className="logs-panel">
            {logs.length === 0 ? (
              <div className="log-entry" style={{color: '#666'}}>No logs found...</div>
            ) : (
              logs.map((log, i) => (
                <div key={i} className={`log-entry ${log.includes('ERROR') ? 'error' : log.includes('Success') ? 'success' : 'info'}`}>
                  {log}
                </div>
              )).reverse()
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
