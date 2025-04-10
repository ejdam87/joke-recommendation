import { useState } from 'react';
import Button from 'react-bootstrap/Button';


function App() {
    const [data, set_data] = useState("");

    const send_request = async () => {
        const response = await fetch("http://127.0.0.1:5000/example");
        if (!response.ok) {
            return null;
        }

        const data = await response.json();
        set_data(data["data"]);
    }

    return (
        <>
            <Button
                variant="primary"
                onClick={send_request}
            >
                Send request!
            </Button>

            <div>Data from the server: {data}</div>
        </>
    )
}

export default App
