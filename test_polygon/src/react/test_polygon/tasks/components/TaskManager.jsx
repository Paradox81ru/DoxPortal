// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import Task1 from './Task1/Task1'
import Task2 from "./Task2/Task2";
import Task3 from "./Task3/Task3";
import Task4 from "./Task4/Task4";
import Task5 from "./Task5/Task5";

class TaskManager extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentTask: 0
        }
    }

    handleChecked = (event) => {
        const {name, value} = event.target;
        this.setState({
            currentTask: Number(value)
        })
    }

    /**
     * Возвращает кнопку бутстрап-радиобаттон
     * @param taskName
     * @param taskNum
     * @return {JSX.Element[]}
     */
    getButton(taskName, taskNum) {
        const btnName = "btnradio";
        const id =`${btnName}${taskNum}`;
        return (
            <React.Fragment key={taskNum}>
            <input
                type="radio"
                className="btn-check"
                name={btnName}
                value={taskNum}
                id={id}
                autoComplete="off"
                checked={this.state.currentTask === taskNum}
                onChange={this.handleChecked}
            />
            <label className="btn btn-outline-primary" htmlFor={id}>{taskName}</label>
            </React.Fragment>
        )
    }

    render() {
        const taskArray = [
            ["Task1", <Task1 /> ],
            ["Task2", <Task2 /> ],
            ["Task3", <Task3 /> ],
            ["Task4", <Task4 /> ],
            ["Task5", <Task5 /> ],
        ];
        const taskList = taskArray.map((item, index) => this.getButton(item[0], index));
        return (
            <div>
            <div className="btn-group" role="group" aria-label="Basic radio toggle button group">
                {taskList}
            </div>
            {taskArray[this.state.currentTask][1]}
            </div>
        )
    }
}

export default TaskManager