// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import TaskManager from "./components/TaskManager";
import Task1 from './components/Task1/Task1'
import Task2 from "./components/Task2/Task2";
import Task3 from "./components/Task3/Task3";
import Task4 from "./components/Task4/Task4";
import Task5 from "./components/Task5/Task5";
import Footer from "./components/Footer";

const App = () => (
    <div className="App">
        <TaskManager />
        <Footer />
    </div>
)

export default App