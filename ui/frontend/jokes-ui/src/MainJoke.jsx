import { useState } from 'react';
import { Button, Card, Form } from "react-bootstrap";

function MainJoke(props) {
    const [rating, set_rating] = useState(0);
    const joke_text = props.main_joke[1];
    return (
        <>
            <Card border="0" className="mt-2">
                <Card.Body>
                    <Card.Text className="fs-2">
                        {joke_text}
                    </Card.Text>
                </Card.Body>
            </Card>
            <Form.Label>Rating: {rating}</Form.Label>
            <Form.Range
                min={-10}
                max={10}
                step={1}
                value={rating}
                onChange={(e) => set_rating(e.target.value)}
            />
            <Button>
                Submit rating
            </Button>
        </>
    )
}

export default MainJoke