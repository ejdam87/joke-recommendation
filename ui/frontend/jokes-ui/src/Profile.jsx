import { useState } from 'react';
import { Form, Button, Container, Card, Row, Col, Table } from "react-bootstrap";

function Profile(props) {

    const [current_uid, set_current_uid] = useState(0);

    const handle_uid_change = (e) => {
        set_current_uid(e.target.value);
    };

    const handle_uid_create = async () => {
        const response = await fetch("http://127.0.0.1:5000/new_profile")

        const data = await response.json();
        props.set_uid( data["uid"] );
    };

    const handle_uid_submit = async () => {
        const n_uid = Number(current_uid);
        const response = await fetch("http://127.0.0.1:5000/get_profile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"uid": n_uid })
        })

        props.set_uid(n_uid);
        const data = await response.json();
        props.set_profile( data["profile"] );
    }

    const download_profile = () => {
        const file_name = `profile_${props.uid}`;
        const json = JSON.stringify(props.profile, null, 4);
        const blob = new Blob([json], { type: "application/json" });
        const href = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = href;
        link.download = file_name + ".json";
        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        URL.revokeObjectURL(href);
    }

    return (
        <Container className="mt-5">
            <Card>
                <Card.Header className="d-flex flex-column align-items-center">
                    <Card.Title>Your profile (UID={props.uid})</Card.Title>
                </Card.Header>
                <Card.Body>
                    <Row>
                        <Col xs={12} sm={12} md={{ span: 3, offset: 2 }} lg={{ span: 3, offset: 2 }} className="d-flex flex-column align-items-center mb-5">
                            <Form.Group controlId="formFile" className="mb-3">
                                <Form.Label>Type your UID:</Form.Label>
                                <Form.Control
                                    className="mb-3"
                                    type="number"
                                    onChange={handle_uid_change}
                                />
                                <Button
                                    className="mb-3"
                                    onClick={handle_uid_submit}
                                >
                                    Submit UID
                                </Button>
                                <p>Or</p>
                                <Button onClick={handle_uid_create} >
                                    Create new UID
                                </Button>
                            </Form.Group>

                        </Col>

                        <Col xs={12} sm={12} md={{ span: 3, offset: 2 }} lg={{ span: 3, offset: 2 }} className="d-flex flex-column align-items-center">
                            <Table size="md" responsive="md">
                                <thead>
                                    <tr>
                                        <th>Joke ID</th>
                                        <th>Rating</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {
                                        Object.entries(props.profile).map(([id, rating]) => (
                                            <tr key={id}>
                                                <td>{id}</td>
                                                <td>{rating}</td>
                                            </tr>
                                        ))
                                    }
                                </tbody>
                            </Table>

                            <Button onClick={download_profile} >
                                Download your current profile
                            </Button>
                        </Col>
                    </Row>
                </Card.Body>
            </Card>
        </Container>
    )
}

export default Profile
