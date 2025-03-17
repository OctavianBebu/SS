import { useState, useEffect } from "react";

function App() {
    const [message, setMessage] = useState("");

    useEffect(() => {
        fetch("http://127.0.0.1:8000/")
            .then(response => response.json())
            .then(data => setMessage(data.message))
            .catch(error => console.error("Error:", error));
    }, []);

    return (
        <div>
            <h1>React + FastAPI</h1>
            <p>{message}</p>
        </div>
    );
}

export default App;
