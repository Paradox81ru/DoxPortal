import React, {Component, useState} from "../../../../../../../../../../node_modules/react";
import {useParams} from "../../../../../../../../../../node_modules/react-router-dom";
import {Navigate} from "../../../../../../../../../../node_modules/react-router-dom";
import {bindActionCreators} from "../../../../../../../../../../node_modules/redux"
import {connect} from "../../../../../../../../../../node_modules/react-redux";

import {getFetchHeaders} from "../../../../../lib/send_request_util";
import {addSystemMessage} from "../../../../../store/actions/generalActions";
import {UnauthorizedError} from "../../../../../lib/errors";

function ConfirmAccount(props) {
    const { token } = useParams();
    return (
        <_ConfirmAccount token={token} handleAddSystemMessage={props.handleAddSystemMessage} />
    )
}

class _ConfirmAccount extends Component {
    constructor(props) {
        super(props);
        this.state = {
            element: <p>Подтверждение аккаунта</p>
        }
    }

    componentDidMount() {
        this.handleConfirmAccount();
    }

    /** Отправляет запрос на подтверждение аккаунта */
    handleConfirmAccount = () => {
        let headers = getFetchHeaders();
        let options = {headers: headers};
        options["method"] = "POST";
        options["body"] = JSON.stringify({token: this.props.token});
        const path = "/api/auth/confirm-account";
        fetch(path, options)
            .then(response => {
                if (response.status === 200)
                    return response.json();
                if (response.status === 401)
                    throw new UnauthorizedError(`Путь ${path} ошибочно не разрешён.`);
            })
            .then(data => {
                if (data.hasOwnProperty("success")) {
                    this.setState({element: <Navigate replace to="/site-message/confirm_account-success" username={data["username"]} />});
                } else if (data.hasOwnProperty("error")) {
                    this.setState({element: <Navigate replace to="/site-message/confirm_account-invalid" username={data["username"]} />});
                } else {
                    throw new Error("Вернулись некорректные данные.");
                }
            })
            .catch(error => {
                if (error.name === "UnauthorizedError")
                    this.props.handleAddSystemMessage("danger", "Ошибка: " + error.message);
                else
                    this.props.handleAddSystemMessage("danger", "Неизвестная ошибка: " + error);
            });
    }

    render() {
        return ( this.state.element );
    }
}

function mapDispatchToProps(dispatch) {
    return {
        handleAddSystemMessage: bindActionCreators(addSystemMessage, dispatch)
    }
}

export default connect(null, mapDispatchToProps)(ConfirmAccount);