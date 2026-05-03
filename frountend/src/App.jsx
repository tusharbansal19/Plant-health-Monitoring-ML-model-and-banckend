import { useEffect, useState } from 'react';
import './App.css';


function App() {
  const [ws, setWs] = useState(null);
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("Disconnected");

  useEffect(() => {
    let wsUrl;
   
      wsUrl = 'wss://plant-health-monitor-banckend.onrender.com/ws';
      // Local development - connect to local backend
   
    
    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      setStatus("Connected ✅");
      
      const testData = {
        Soil_Moisture: 50,
        Ambient_Temperature: 25,
        Humidity: 60,
      };
      socket.send(JSON.stringify(testData));
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, data]);
      } catch (e) {
        setMessages((prev) => [...prev, event.data]);
      }
    };

    socket.onerror = (error) => {
      setStatus("Error ❌");
    };

    socket.onclose = (event) => {
      setStatus("Disconnected ❌");
    };

    setWs(socket);

    return () => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
  }, []);

  const sendAgain = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      const data = {
        Soil_Moisture: Math.random() * 100,
        Ambient_Temperature: 20 + Math.random() * 10,
        Humidity: 40 + Math.random() * 20,
      };
      ws.send(JSON.stringify(data));
    } else {
      setStatus("Not Connected");
    }
  };
   

  return (
    <div style={{ padding: 20 }}>
      <h2>WebSocket Test</h2>
      <p>Status: <strong>{status}</strong></p>

      <button onClick={sendAgain} style={{ padding: '10px 20px', fontSize: '16px' }}>
        Send Data
      </button>

      <div style={{ marginTop: 20 }}>
        <h4>Messages ({messages.length}):</h4>
        <div style={{ maxHeight: '400px', overflowY: 'auto', border: '1px solid #ccc', padding: '10px' }}>
          {messages.map((msg, i) => (
            <div key={i} style={{ marginBottom: '10px', padding: '10px', backgroundColor: '#f5f5f5', borderRadius: '5px' }}>
              <pre>{typeof msg === 'string' ? msg : JSON.stringify(msg, null, 2)}</pre>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}



export default App
