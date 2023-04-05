// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import Header from "components/tasks/components/Header";
import Conditional from "components/tasks/components/Task3/Conditional";

class Task4 extends Component {
    constructor() {
        super();
        this.state = {
            loading: false,
            character: {}
        }
    }

    componentDidMount() {
        this.setState({
            loading: true
        })
        const heroNumber = DoxHelper.randomInteger(1, 83)
        fetch(`https://swapi.dev/api/people/${heroNumber}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.setState({
                    loading: false,
                    character: data
                    }
                )
            });
    }

    render() {
        const text = this.state.loading ? "loading..." : this.state.character.name
        return (
            <div className="task task4">
                <Header title="Тестовое задание 4" />
                <div>
                    {text}
                </div>
            </div>
        )
    }
}

export default Task4