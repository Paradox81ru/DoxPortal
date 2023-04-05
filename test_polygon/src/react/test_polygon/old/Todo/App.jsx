// import React from "../../../../../../../../node_modules/react";
import React, {Component} from "../../../../../../../../node_modules/react";
import Footer from "./Components/Footer";
import Header from "./Components/Header";
import MainContent from "components/Todo/Components/MainContent";
import TodoItem from "./Components/TodoItem";
import "./src/todosData";
import "./style/index.css";
import todosData from "components/Todo/src/todosData";

class App extends Component {
    constructor() {
        super();
        this.state = {
            todos: todosData
        }
    }

    handleChange = (id) => {
        this.setState(prevState => {
            const updatedTodos = prevState.todos.map(todo => {
                if (todo.id === id) {
                    todo.completed = !todo.completed;
                }
                return todo;
            });
            return {
                todos: updatedTodos
            }
        })
    }

    render() {
        const todoItems = this.state.todos.map(item => <TodoItem key={item.id} item={item} handleChange={this.handleChange} />);

        return (
        <div className="todo-list">
            <React.StrictMode>
            {todoItems}
            </React.StrictMode>
        </div>
        )
    }
}

// function App() {
//     const todoItems = todosData.map(item => <TodoItem key={item.id} item={item} />)
//
//     return (
//         <div className="todo-list">
//             {todoItems}
//         </div>
//     )
// }

export default App;