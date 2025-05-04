import { useState, useEffect } from 'react';
import { HashRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Navbar, Nav, Spinner, Row, Col, Container } from "react-bootstrap";


import EvalShow from './EvalShow';
import JokeShow from './JokeShow';
import Profile from './Profile';

function App() {
    const [visible_jokes_cb, set_visible_jokes_cb] = useState([]); // list to preserve order
    const [visible_jokes_svd, set_visible_jokes_svd] = useState([]); // list to preserve order
    const [visible_jokes_random, set_visible_jokes_random] = useState([]); // list to preserve order

    const [jokes, set_jokes] = useState({}); // object since we do not care about the order
    const [profile, set_profile] = useState({});
    const [uid, set_uid] = useState(-1);
    const [loading, set_loading] = useState(true);

    const get_jokes = async () => {
        set_loading(true);
        const response = await fetch("http://127.0.0.1:5000/get_jokes");
        if (!response.ok) {
            set_loading(false);
            return null;
        }

        const data = await response.json();
        set_jokes(data["data"]);
        set_loading(false);
    }

    const get_recommendation = async () => {
        for (let recommender of ["cb", "svd", "random"])
        {
            set_loading(true);
            const response = await fetch(`http://127.0.0.1:5000/get_recommendation_${recommender}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"uid": uid})
            })
            if (!response.ok) {
                set_loading(false);
                return null;
            }
    
            const data = await response.json();
            let to_show = [];
            for (let id of data["recommendation"])
            {
                to_show.push( [id, jokes[id]] );
            }

            if (recommender == "cb")
            {
                set_visible_jokes_cb(to_show);
            }
            else if (recommender == "svd")
            {
                set_visible_jokes_svd(to_show);
            }
            else
            {
                set_visible_jokes_random(to_show);
            }

            set_loading(false);
        }
    }

    const handle_uid_create = async () => {
        const response = await fetch("http://127.0.0.1:5000/new_profile")

        const data = await response.json();
        set_uid( data["uid"] );
        set_profile( {} );
        return data["uid"];
    };

    useEffect(()=> {get_jokes();}, []);
    useEffect(()=> {get_recommendation();}, [jokes]);
    useEffect(()=> {get_recommendation();}, [profile]);

    return (
        <Router>
            <Navbar>
                <Container>
                    <Nav>
                        <Nav.Link as={Link} to="/"> Department of Fun </Nav.Link>
                    </Nav>
                    <Nav>
                        <Nav.Link as={Link} to="/profile"> Profile (UID = {uid == -1 ? "Unknown" : uid}) </Nav.Link>
                    </Nav>
                </Container>
            </Navbar>
            <Routes>
                <Route path="/" element={loading ?
                    <Container>
                        <Row className="align-items-center">
                            <Col className="text-center">
                                <Spinner className="mt-3" animation="grow" size="xl" />
                            </Col>
                        </Row>
                    </Container>
                    :
                    <EvalShow
                        visible_jokes_cb={visible_jokes_cb}
                        visible_jokes_svd={visible_jokes_svd}
                        visible_jokes_random={visible_jokes_random}
                        uid={uid}
                        profile={profile}
                        set_profile={set_profile}
                        handle_uid_create={handle_uid_create}
                    />
                    } />
                <Route path="/profile" element={
                    <Profile
                        profile={profile}
                        uid={uid}
                        set_uid={set_uid}
                        set_profile={set_profile}
                        handle_uid_create={handle_uid_create}
                    />
                    } />
            </Routes>
    </Router>
    )
}

export default App
