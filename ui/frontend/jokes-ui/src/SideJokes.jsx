import { Card } from "react-bootstrap";

function SideJokes(props) {
    return (
        <Card border="0" className="mt-2 d-flex flex-column align-items-center">
            <Card.Header>
                <Card.Title>Similar jokes you might like</Card.Title>
            </Card.Header>
            <Card.Body>
                {
                    props.side_jokes.map( ([id, joke]) => (
                        <Card className="mt-3">
                            <Card.Body>
                                <Card.Text className="fs-6">
                                    {joke}
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    ) )
                }
            </Card.Body>
        </Card>
    )
}

export default SideJokes