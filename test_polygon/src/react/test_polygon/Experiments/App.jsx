import React from "../../../../../../../../node_modules/react";
import TaskManager from "./TaskManager";
import Footer from "components/tasks/components/Footer";

export default function App() {
    return (
        <div className="App">
            <h2>Эксперименты</h2>
            <React.StrictMode>
                <TaskManager/>
            </React.StrictMode>
            <Footer/>
        </div>
    )

}