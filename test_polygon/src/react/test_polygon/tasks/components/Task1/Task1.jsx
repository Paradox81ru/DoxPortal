// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import Header from "components/tasks/components/Header";
import Hello from "./Hello";

function Task1() {
    const [firstName, lastName] = ["Юрий", "Пугач"];
    const styles = {
        color: "red",
        backgroundColor: "blue"
    }

    return (
        <div className="task task1">
            <Header title="Тестовое задание 1" />
            <div>
              <Hello firstName={firstName} lastName={lastName} />
              <p style={styles}>Этот параграф обо мне...</p>
              <ul style={{color: "#8af1e5", backgroundColor: "#e9b727"}}>
                <li>Тайланд</li>
                <li>Япония</li>
                <li>Северные страны</li>
              </ul>
            </div>
        </div>
    )
}

export default Task1