import React from "../../../../../../../../../node_modules/react";

function TodoItem(props) {
    const style = {};
    if (props.item.completed) {
        style["textDecoration"] = "line-through";
    }

    return (
        <div className="todo-item">
            <input
                type="checkbox"
                checked={props.item.completed}
                onChange={() => props.handleChange(props.item.id)}
            />
            <p style={style}>{props.item.text}</p>
        </div>
    )
}

export default TodoItem;