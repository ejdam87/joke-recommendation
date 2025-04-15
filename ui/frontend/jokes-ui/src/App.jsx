import { useState, useEffect } from 'react';
import { HashRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Navbar, Nav, Container } from "react-bootstrap";

import JokeShow from './JokeShow';
import Profile from './Profile';

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
        const file = event.target.files[0];

        const reader = new FileReader();
        reader.onload = (inner_event) => {
            try
            {
                const parsed = JSON.parse(inner_event.target.result);
                set_profile(parsed);
            }
            catch (err)
            {
                console.error('JSON parse error:', err);
            }
        };
    
        reader.readAsText(file);
    };

    useEffect(()=> {get_jokes();}, []);
    useEffect(()=> {get_recommendation();}, [jokes]);
    useEffect(()=> {get_recommendation();}, [profile]);

    return (
        <Router>
            <Navbar sticky="top">
                <Container>
                    <Nav>
                        <Nav.Link as={Link} to="/"> Department of Fun </Nav.Link>
                    </Nav>
                    <Nav>
                        <Nav.Link as={Link} to="/profile"> Profile </Nav.Link>
                    </Nav>
                </Container>
            </Navbar>
            <Routes>
                <Route path="/" element={
                    <JokeShow
                        visible_jokes={visible_jokes}
                    />
                    } />
                <Route path="/profile" element={
                    <Profile
                        profile={profile}
                        handle_profile_change={handle_profile_change}
                    />
                    } />
            </Routes>
    </Router>
    )
}

export default App
