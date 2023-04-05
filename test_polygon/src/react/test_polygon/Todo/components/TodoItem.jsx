// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';

function TodoItem(props) {
    const completedStyle = {
        fontStyle: "italic",
        color: "#cdcdcd",
        textDecoration: "line-through"
    }
    const todoItemClass = "todo-item" + (props.item.completed ? " completed" : "");
    return (
        <div className={todoItemClass}>
            <input type="checkbox"
                   checked={props.item.completed}
                   onChange={() => props.handleChange(props.item.id)}
            />
            <div>{props.item.text}</div>
        </div>
    )
}

export default TodoItem;