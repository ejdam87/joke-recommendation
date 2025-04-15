import { Form, Button, Container, Card, Row, Col, Table } from "react-bootstrap";

function Profile(props) {

    const download_profile = () => {
        const file_name = "profile";
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
                    <Card.Title>Your profile</Card.Title>
                </Card.Header>
                <Card.Body>
                    <Row>
                        <Col xs={12} sm={12} md={{ span: 3, offset: 2 }} lg={{ span: 3, offset: 2 }} className="d-flex flex-column align-items-center mb-5">
                            <Form.Group controlId="formFile" className="mb-3">
                                <Form.Label>Upload your profile</Form.Label>
                                <Form.Control type="file" accept=".json" onChange={props.handle_profile_change} />
                            </Form.Group>

                            <Button onClick={download_profile} >
                                Download your profile
                            </Button>
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
                        </Col>
                    </Row>
                </Card.Body>
            </Card>
        </Container>
    )
}

export default Profile
