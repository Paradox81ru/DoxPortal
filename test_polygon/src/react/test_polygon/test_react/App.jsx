// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import SimpleForm from "./components/SimpleForm"


const App = () => (
    <div className="App">
        <header className="App-header">
            <h2 className="App-title">Тестовая страница React</h2>
        </header>
        <p className="App-intro">
            To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <SimpleForm />
    </div>
);


export default App;

/*
class App extends Component {
    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <h2 className="App-title">Welcome to React</h2>
                </header>
                <p className="App-intro">
                    To get started, edit <code>src/App.js</code> and save to reload.
                </p>
            </div>
        );
    }
}
*/
