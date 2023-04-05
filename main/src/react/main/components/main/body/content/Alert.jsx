import React, {Component} from "../../../../../../../../../node_modules/react";
import CloseButton from "../../../../../../../../../node_modules/react-bootstrap/CloseButton"
import Fade from '../../../../../../../../../node_modules/react-bootstrap/Fade';

export default class Alert extends Component{
    constructor() {
        super();
        // При создании сообщение должно отображаться (isShow: true), но за счет свойства Fade appear оно появиться плавно.
        this.state = {
            messageId: 0,
            isShow: true
        };
    }

    componentDidMount() {
        this.setState({
            ...this.state,
            messageId: this.props.messageId
        });
    }

    /** Обрабатывает событие закрытия сообщения */
    handleCloseMessage = (e) => {
        // Обработчик закрытия сообщения только скрывает сообщение, но за счёт события Fade onExited
        // передан обработчик события удаления сообщения (this.props.onCloseMessage()).
        this.setState({
            ...this.state,
            isShow: false
        });
    }

    getClass() {
        let cls = "alert alert-" + this.props.type;
        if (this.props.isClose)
            cls += " alert-dismissible";
        if (this.props.isAnimation)
            cls += " fade";
        return cls;
    }

    render() {
        return (
            <Fade appear in={this.state.isShow} onExited={() => this.props.onCloseMessage(this.state.messageId)}>
                <div className={this.getClass()}
                     role="alert">
                    {this.props.message}
                    {this.props.isClose &&
                        <CloseButton aria-label="Close" data-bs-dismiss="alert" onClick={this.handleCloseMessage} />}
                </div>
            </Fade>
        )
    }
}
