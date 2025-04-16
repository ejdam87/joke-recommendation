import { useState } from 'react';
import { Container, Button, Card, Form } from "react-bootstrap";

function MainJoke(props) {
    const [rating, set_rating] = useState(0);

    const handle_rating_submit = () => {
        props.profile[ props.main_joke[0] ] = Number(rating);
        props.set_profile(props.profile);
    }

    const joke_text = props.main_joke ? props.main_joke[1] : "";
    return (
        <Container className="d-flex flex-column vh-100 justify-content-center align-items-center">
            <Card border="0" className="mt-2">
                <Card.Body>
                    <Card.Text className="fs-2">
                        {joke_text}
                    </Card.Text>
                </Card.Body>
            </Card>
            <Container className="d-flex flex-column align-items-center mt-5">
                <Form.Label>Rating: {rating}</Form.Label>
                <Form.Range
                    min={-10}
                    max={10}
                    step={1}
                    value={rating}
                    onChange={(e) => set_rating(e.target.value)}
                />
                <Button
                    className="mt-3"
                    onClick={handle_rating_submit}
                >
                    Submit rating
                </Button>
            </Container>
        </ Container>
    )
}

export default MainJoke