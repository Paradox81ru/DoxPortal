import React, {Component} from "../../../../../../node_modules/react";
import {Provider} from "../../../../../../node_modules/react-redux";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
} from "../../../../../../node_modules/react-router-dom";
import store from "../store/store";
import setBreadcrumb from "../store/actions/setBreadcrumb";
import changeUserAuthentication from "../store/actions/changeUserAuthentication";
import {setDynamicStyles, clearDynamicStyles} from "../../../../../main/src/react/main/lib/stylesheet_util";
import {whereRememberToken, REMEMBER_LOCAL} from "../../../../../main/src/react/main/lib/auth_token_util";
import {getFetchHeaders, requestNewTokenAccess, resolveBeginData} from "../../../../../main/src/react/main/lib/send_request_util";

import {Navigate} from "../../../../../../node_modules/react-router-dom";

import Header from "./main/header/Header";
import UnderHeader from "../../../../../main/src/react/main/components/main/under_header/UnderHeader";
import Body from "./main/body/Body";
import Error from "../../../../../main/src/react/main/components/main/body/content/main/Error";
import Logout_W from "../../../../../main/src/react/main/components/main/body/content/Auth/Logout";

export default class App extends Component {
    constructor() {
        super();
        this.state = {
            isLoading: true,
            whereRememberTokens: null,
            error: {}
        }
    }

    /** Для формы логина передаёт параметр "remember my" */
    getRememberMy() {
        return this.state.whereRememberTokens === REMEMBER_LOCAL
    }

    /** Устанавливает список динамичных стилей */
    setListStyles = (list) => {
        setDynamicStyles(list);
    }

    /** Очищает список динамичных стилей */
    clearListStyles = () => {
        clearDynamicStyles();
    }

    componentDidMount() {
        this.setState({
            whereRememberTokens: whereRememberToken()
        });
        this.sendBeginDataRequest();
    }

    /** Отправляет запрос на получение начальных данных */
    sendBeginDataRequest = () => {
        let options = {headers: getFetchHeaders()};
        fetch("/api/my-admin/begin-data", options)
            .then(resolveBeginData("/api/admin/begin-data", true))
            .then(data => {
                store.dispatch(setBreadcrumb(data.breadcrumbList));
                store.dispatch(changeUserAuthentication(data.userAuthentication));
                this.setState({
                    ...this.state,
                    isLoading: false
                })
            })
            .catch((error) => {
                this.setState({
                    ...this.state,
                    error: {code: error.code, message: error.message}
                })
            })
    }

    getRouter() {
        return(
            <Router>
                <Provider store={store}>
                    <Header />
                    <UnderHeader isAdmin={true} />
                    <Routes>
                        <Route element={<Body />}>
                            <Route path="/dox-admin" element={<h2>Главная</h2>} />
                            <Route path="/logout" element={<Logout_W />} />
                            <Route path="/dox-admin/edit-profile" element={<h2>Редактирование профилей</h2>} />
                            <Route path="/dox-admin/manage-temp-user" element={<h2>Редактирование временных пользователей</h2>} />
                            <Route path="*" element="Not found" />
                        </Route>
                    </Routes>
                </Provider>
            </Router>
        )
    }

    render() {
        return (
            <div className="wrap">
                {this.state.error.hasOwnProperty("message") && this.state.error["message"]
                    ? <Error code={this.state.error.code} message={this.state.error.message} />
                    : this.state.isLoading ? <p>Загрузка...</p> : this.getRouter()}
            </div>
        );
    }
}