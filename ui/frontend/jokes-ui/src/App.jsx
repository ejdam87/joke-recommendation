import { useState } from 'react';
import Button from 'react-bootstrap/Button';


function App() {
    const [jokes, set_jokes] = useState({});

    const get_jokes = async () => {
        const response = await fetch("http://127.0.0.1:5000/get_jokes");
        if (!response.ok) {
            return null;
        }

        const data = await response.json();
        set_jokes(data["data"]);
    }

    return (
        <>
            <Button
                variant="primary"
                onClick={get_jokes}
            >
                Send request!
            </Button>

            {Object.entries(jokes).map(([key, value]) => (
                <div> {key} - {value} </div>
            ))}
        </>
    )
}

export default App
