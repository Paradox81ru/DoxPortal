// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import Header from "components/tasks/components/Header";
import Conditional from "./Conditional";

class Task3 extends Component {
    constructor() {
        super();
        this.state = {
            isLoading: true
        };
    }

    componentDidMount() {
        // загрузить данные, необходимые для корректного отображения компонента
        setTimeout(() => {
            this.setState({
                isLoading: false
            })
        }, 1500)
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        // вернуть true если компонент нуждается в обновлении
        // вернуть false в противном случае
        return true
    }

    componentWillUnmount() {
        // навести порядок после удаления компонента
        // (например - убрать прослушиватели событий)
    }

    render() {
        return (
            <div className="task task3">
                <Header title="Тестовое задание 3" />
                <div>
                    <Conditional isLoading={this.state.isLoading} />
                </div>
            </div>
        )
    }
}

export default Task3