import React, {Component} from "../../../../../../../../../../node_modules/react";


class App extends Component {
    constructor() {
        super()
        this.state = {
            isLoading: false,
            character: {}
        }
    }

    componentDidMount() {
        this.setState({isLoading: true});
        const heroNumber = DoxHelper.randomInteger(1, 83)
        fetch(`https://swapi.dev/api/people/${heroNumber}`)
            .then(response => response.json())
            .then(data => {
                this.setState({
                    isLoading: false,
                    character: data
                })
            });
    }

    render() {
        const text = this.state.isLoading ? "loading..." : this.state.character.name;
        return (
            <div>
                {text}
            </div>
        )
    }
}

export default App