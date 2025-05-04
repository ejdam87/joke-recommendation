import { Container, Card, Form } from "react-bootstrap";

function MainJoke(props) {

    const joke_text = props.main_joke ? props.main_joke[1] : "";
    return (
        <Container className="mt-5">
            <Card border="0" className="mt-2">
                <Card.Body>
                    <Card.Text className="fs-2">
                        {joke_text}
                    </Card.Text>
                </Card.Body>
            </Card>
            <Container className="d-flex flex-column align-items-center mt-5">
                <Form.Label>Rating: {props.rating}</Form.Label>
                <Form.Range
                    min={-10}
                    max={10}
                    step={1}
                    value={props.rating}
                    onChange={(e) => props.set_rating(e.target.value)}
                />
            </Container>
        </ Container>
    )
}

export default MainJoke