import { Container, Row, Col } from "react-bootstrap";

import MainJoke from "./MainJoke.jsx";
import SideJokes from "./SideJokes.jsx";


function JokeShow(props) {
    const main_joke = props.visible_jokes[0];
    const side_jokes = props.visible_jokes.slice(1);
    return (
        <Container>
            <Row>
                <Col xs={12} sm={12} md={8} lg={8}>
                    <MainJoke
                        main_joke={main_joke}
                        profile={props.profile}
                        set_profile={props.set_profile}
                    />
                </Col>
                <Col xs={12} sm={12} md={4} lg={4}>
                    <SideJokes side_jokes={side_jokes} />
                </Col>
            </Row>
        </Container>
    )
}

export default JokeShow
