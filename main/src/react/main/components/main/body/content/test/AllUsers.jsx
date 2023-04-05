import React, {Component} from "../../../../../../../../../../node_modules/react";
import {sendRequest} from "../../../../../lib/send_request_util";

export default class AllUsers extends Component {
    constructor(props) {
        super(props);
        this.state = {
            users: []
        }
    }

    componentDidMount() {
        sendRequest("/api/get-all-users", "GET")
            .then(response => {
                this.setState({
                    users: response
                })
            }).catch(err => console.log("Ошибка get-all-users " + err.message));
    }

    render() {
        if (this.state.users === undefined) {
            return(<>
                <h3>Все пользователи</h3>
                <p>Ошибка запроса всех пользователей</p>
            </>)
        } else {
            const users = this.state.users.map((user, index) => <li key={index}>{user.username}</li>);
            return (
                <>
                    <h3>Все пользователи</h3>
                    <ul>
                        {users}
                    </ul>
                </>
            )
        }
    }
}