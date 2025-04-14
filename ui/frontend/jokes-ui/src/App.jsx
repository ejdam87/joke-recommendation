import { useState, useEffect } from 'react';
import { Form, Button } from "react-bootstrap";

import Joke from "./Joke.jsx";

function App() {
    const [visible_jokes, set_visible_jokes] = useState({});
    const [jokes, set_jokes] = useState({});
    const [profile, set_profile] = useState({});

    const get_jokes = async () => {
        const response = await fetch("http://127.0.0.1:5000/get_jokes");
        if (!response.ok) {
            return null;
        }

        const data = await response.json();
        set_jokes(data["data"]);
    }

    const get_recommendation = async () => {
        const response = await fetch("http://127.0.0.1:5000/get_recommendation", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"profile": profile})
        })
        if (!response.ok) {
            return null;
        }

        const data = await response.json();
        let to_show = {};
        for (let id of data["data"])
        {
            to_show[id] = jokes[id];
        }
        set_visible_jokes(to_show);
    }

    const handle_profile_change = (event) => {
        const new_profile = event.target.files[0];
        console.log(new_profile);
    };

    useEffect(()=> {get_jokes();}, []);

    return (
        <>
            <Button
                variant="primary"
                onClick={get_recommendation}
            >
                Send request!
            </Button>
            <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Choose a text file</Form.Label>
                <Form.Control type="file" accept=".txt" onChange={handle_profile_change} />
            </Form.Group>

            {Object.entries(visible_jokes).map(([key, value]) => (
                <Joke id={key} text={value} />
            ))}
        </>
    )
}

export default App
