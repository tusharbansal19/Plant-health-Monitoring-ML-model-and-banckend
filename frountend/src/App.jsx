import { useState,useEffect  } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'


function App() {
  const [ws, setWs] = useState(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const socket = new WebSocket("wss://plant-health-monitor-banckend.onrender.com/ws");

    socket.onopen = () => {
      console.log("✅ Connected to server");

      // Send dummy correct data
      socket.send(
        JSON.stringify({
          Soil_Moisture: 50,
          Ambient_Temperature: 25,
          Humidity: 60,
        })
      );
    };

    socket.onmessage = (event) => {
      console.log("📩 Message:", event.data);
      setMessages((prev) => [...prev, event.data]);
    };

    socket.onerror = (error) => {
      console.error("❌ Error:", error);
    };

    socket.onclose = () => {
      console.log("🔌 Disconnected");
    };

    setWs(socket);

    return () => {
      socket.close();
    };
  }, []);

  const sendAgain = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(
        JSON.stringify({
          Soil_Moisture: Math.random() * 100,
          Ambient_Temperature: 20 + Math.random() * 10,
          Humidity: 40 + Math.random() * 20,
        })
      );
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>WebSocket Test</h2>

      <button onClick={sendAgain}>Send Data</button>

      <div style={{ marginTop: 20 }}>
        <h4>Messages:</h4>
        {messages.map((msg, i) => (
          <div key={i}>{msg}</div>
        ))}
      </div>
    </div>
  );
}



export default App
