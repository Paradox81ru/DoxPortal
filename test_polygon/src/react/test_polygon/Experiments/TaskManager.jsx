// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import ReactState from "./TestReactState/ReactState";
import ReduxSingleStore from "./TestReduxSingleStore/ReduxSingleStore";
import ReduxDistributedStore from "./TestReduxDistributedStore/ReduxDistributedStore";

const expArray = [
    ["Эксперимент 1", <ReactState/> ],
    ["Эксперимент 2", <ReduxSingleStore />],
    ["Эксперимент 3", <ReduxDistributedStore />],
    ["Эксперимент 4", <div >Эксперимент 4</div>],
    ["Эксперимент 5", <div >Эксперимент 5</div>],
];

export default class TaskManager extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentExp: 0
        }
    }

    handleChecked = (event) => {
        const {value} = event.target;
        this.setState({
            currentExp: Number(value)
        })
    }

    /**
     * Возвращает кнопку бутстрап-радиобаттон
     * @param {string} expName наименование эксперимента
     * @param {number} expNum номер текущего эксперимента
     * @return {JSX.Element[]}
     */
    getButton(expName, expNum) {
        const btnName = "btnradio";
        const id = `${btnName}${expName}`;
        return (
            <React.Fragment key={expNum}>
                <input
                    type="radio"
                    className="btn-check"
                    name={btnName}
                    value={expNum}
                    id={id}
                    autoComplete="off"
                    checked={this.state.currentExp === expNum}
                    onChange={this.handleChecked}
                />
                <label className="btn btn-outline-primary" htmlFor={id}>{expName}</label>
            </React.Fragment>
        )
    }

    render() {

        const taskList = expArray.map((item, index) => this.getButton(item[0], index));
        return (
            <div>
                <div className="btn-group" role="group" aria-label="Basic radio toggle button group">
                    {taskList}
                </div>
                {expArray[this.state.currentExp][1]}
            </div>
        )
    }
}