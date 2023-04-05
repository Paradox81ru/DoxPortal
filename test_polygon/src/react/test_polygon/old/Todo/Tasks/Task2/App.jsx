import React from "../../../../../../../../../../node_modules/react";
import Joke from "./Components/Joke";
import jokesData from "./src/jokesData";

function App() {
    const jokeComponents = jokesData.map(joke => <Joke key={joke.id} question={joke.question} punchLine={joke.punchLine} />)

    return (
        <div>
            {jokeComponents}
        </div>
    )
}

export default App;