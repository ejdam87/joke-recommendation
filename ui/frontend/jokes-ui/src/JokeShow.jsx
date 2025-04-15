import { Container } from "react-bootstrap";

import MainJoke from "./MainJoke.jsx";
import SideJokes from "./SideJokes.jsx";
import Joke from "./Joke.jsx";


function JokeShow(props) {
    console.log(props.visible_jokes);
    const main_joke = props.visible_jokes[0];
    const side_jokes = props.visible_jokes.slice(1);
    return (
        <Container>
            <MainJoke main_joke={main_joke}/>
            {props.visible_jokes.map(([key, value]) => (
                <Joke key={key} id={key} text={value} />
            ))}
        </Container>
    )
}

export default JokeShow
