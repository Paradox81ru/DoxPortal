import React, {Component} from "../../../../../../../../../../node_modules/react";
import {bindActionCreators} from "../../../../../../../../../../node_modules/redux"
import {connect} from "../../../../../../../../../../node_modules/react-redux";
import {removeToken} from "../../../../../lib/auth_token_util";
import {getFetchHeaders} from "../../../../../lib/send_request_util";
import {changeMainMenu, changeUserAuthentication} from "../../../../../store/actions/generalActions";
import {sendRequest} from "../../../../../lib/send_request_util";
import {getToken} from "../../../../../lib/auth_token_util";

class Logout extends Component {

    componentDidMount() {
        this.logout();
    }

    /** Производит разлогирование */
    logout = () => {
        // Делаю запрос на удаление токена обновления на сервере.
        sendRequest("/api/auth/logout", "POST", {token: getToken()})
            .then(() => {
                // После этого удаляю токен из локального хранилища,
                removeToken();
                // и делаю запрос на получение начальных данных, чтобы сбросить интерфейс до неавторизованного пользователя.
                this.getBeginData();
            })
            .catch((error) => {
                // Отображаю ошибку,
                console.log("Ошибка удаления токена обновления на сервере: " + error.message);
                // после чего удаляю токен из локального хранилища,
                removeToken();
                // и делаю запрос на получение начальных данных, чтобы сбросить интерфейс до неавторизованного пользователя.
                this.getBeginData();
            })
    }

    /** После разлогирования надо вернуть меню по умолчанию и убрать пользователя */
    getBeginData() {
        let options = {headers: getFetchHeaders()};
        fetch("/api/begin-data/0", options)
            .then(response => response.json())
            .then(data => {
                this.props.handleChangeUserAuthentication(data);
                this.props.handleChangeMainMenu(data);
            })
    }

    render() {
        return (
            <p>Вы вышли</p>
        )
    }
}

function mapDispatchToProps(dispatch) {
    return {
        handleChangeMainMenu: bindActionCreators(changeMainMenu, dispatch),
        handleChangeUserAuthentication: bindActionCreators(changeUserAuthentication, dispatch)
    }
}

export default connect(null, mapDispatchToProps)(Logout);