import React from "../../../../../node_modules/react";
import ReactDOM from '../../../../../node_modules/react-dom'
import App from "./components/App"

ReactDOM.render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>,
    document.getElementById('react'));
// ReactDOM.render(<App/>, document.getElementsByTagName("body")[0]);