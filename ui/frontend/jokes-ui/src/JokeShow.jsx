import Joke from "./Joke.jsx";


function JokeShow(props) {
    console.log(props.visible_jokes);
    return (
        <>
            {Object.entries(props.visible_jokes).map(([key, value]) => (
                <Joke key={key} id={key} text={value} />
            ))}
        </>
    )
}

export default JokeShow
