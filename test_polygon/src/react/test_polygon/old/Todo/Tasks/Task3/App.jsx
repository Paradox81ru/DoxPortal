import React, {Component} from "../../../../../../../../../../node_modules/react";
import Conditional from "./Conditional";

class App extends Component {
    constructor() {
        super()
        this.state = {
            isLoading: true
        }
    }

    componentDidMount() {
        setTimeout(() => {
            this.setState(
                {isLoading: false}
            )
        }, 1500)
    }

    render() {
        return (
            <div>
                <Conditional isLoading={this.state.isLoading}/>
            </div>
        )
    }
}

export default App