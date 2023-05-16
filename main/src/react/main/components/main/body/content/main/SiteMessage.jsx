import React, {Component} from "../../../../../../../../../../node_modules/react";
import {useParams} from "../../../../../../../../../../node_modules/react-router-dom";

/** Обёртка для класса страницы сообщения для получения параметра пути */
export default function SiteMessage(props) {
    const {messageView} = useParams();
    console.log(props);
    return (
        <_SiteMessage messageView={messageView} />
    )
}

/** Класс страницы сообщения */
class _SiteMessage extends Component{
    constructor(props) {
        super(props);
        this.state = {
            title: "",
            message: ""
        }
    }

    componentDidMount() {
        this.setMessage();
    }

    /** В соответствии с типом сообщения отображает нужное сообщение */
    setMessage() {
        let title, message;
        switch (this.props.messageView) {
            case "signup-success":
                title = "Спасибо";
                message = "Спасибо за регистрацию. На Ваш почтовый ящик выслано письмо с подтверждением учётной записи.";
                break;
            case "signup-invalid":
                title = "Ошибка";
                message = "Приносим свои извинения, но при регистрации вашей учётной записи возникли проблемы. " +
                    "Пожалуйста попробуйте пройти процедуру регистрации позже.";
                break;
            case "confirm_account-success":
                title = "Подтверждение учётной записи";
                message = "На Ваш почтовый ящик было выслано повторное письмо с подтверждением учётной записи.";
                break;
            case "confirm_account-invalid":
                title = "Ошибка";
                message = "При отправке по электронной почте уведомления о подтверждении аккаунта, произошла ошибка. " +
                    "Попробуйте воспользоваться сервисом подтверждения учетной записи.";
                break;
            default:
                title = "";
                message = "";
        }

        this.setState({
            title: title,
            message: message
        })
    }

    render() {
        return (
            <div className="site-message">
                <h2>{this.state.title}</h2>
                <p>{this.state.message}</p>
            </div>
        )
    }
}