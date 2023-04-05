import React, {Component} from "../../../../../../../../node_modules/react";
import {bindActionCreators} from "../../../../../../../../node_modules/redux"
import {connect} from "../../../../../../../../node_modules/react-redux";
import {Link, Navigate} from "../../../../../../../../node_modules/react-router-dom";
import {removeToken} from "../../../lib/auth_token_util";
import {changeMainMenu, changeUserAuthentication} from "../../../store/actions/generalActions";
import {getFetchHeaders} from "../../../lib/doxHelper";
import store from "../../../store/store";

class LoginField extends Component {

    /** Ссылки неавторизованного пользователя */
    getNotAuth() {
        return (
            <React.Fragment>
                <Link to="/login">Войти</Link> /&nbsp;
                <Link to="/signup">Зарегистрироваться</Link>
            </React.Fragment>
        )
    }

    /** Форма выхода авторизованного пользователя */
    getAuth() {
        return (
            <Link to="/logout" >Выход ({this.props.userAuthentication.username})</Link>
        )
    }

    render() {
        const isAuth = this.props.userAuthentication.username != null && this.props.userAuthentication.username;
        return (
            <div className="float-end login">
                {isAuth ? this.getAuth() : this.getNotAuth()}
            </div>
        )
    }
}

function mapStatToProps(state) {
    return {
        userAuthentication: state.hasOwnProperty("general") ? state.general.userAuthentication : state.userAuthentication
    }
}

export default connect(mapStatToProps, null)(LoginField);