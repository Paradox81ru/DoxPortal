// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import Header from "components/tasks/components/Header";
import Form from "./FormContainer";

class Task5 extends Component {
    render() {
        return (
            <div className="task task5">
                <Header title="Тестовое задание 5" />
                <Form />
            </div>
        )
    }
}

export default Task5