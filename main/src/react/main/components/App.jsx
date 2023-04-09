import React, {Component} from "../../../../../../node_modules/react";
import {Provider} from "../../../../../../node_modules/react-redux";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
} from "../../../../../../node_modules/react-router-dom"
import {setDynamicStyles, clearDynamicStyles} from "../lib/stylesheet_util";
import {whereRememberToken, REMEMBER_LOCAL, REMEMBER_SESSION} from "../lib/auth_token_util";
import store from "../store/store";

import Header from "./main/header/Header";
import UnderHeader from "./main/under_header/UnderHeader";
import Body from "./main/body/Body";
import Login_W from "./main/body/content/Auth/Login";
import Logout_W from "./main/body/content/Auth/Logout";
import AllUsers from "./main/body/content/test/AllUsers";
import {getFetchHeaders, resolveBeginData} from "../lib/send_request_util";
import {changeMainMenu, changeUserAuthentication} from "../store/actions/generalActions";
import {sendRequest} from "../lib/send_request_util";
import {setHeaderDate} from "../store/actions/cachePagesActions";
import {addSystemMessage} from "../store/actions/generalActions";
import {removeToken} from "../lib/auth_token_util";

export default class App extends Component{
        constructor() {
        super();
        this.state = {
            isShowCaptcha: false,
            isLoading: true,
            whereRememberToken: null,
            currentYear: 1900,
            siteDomainName: "www.dox-portal.local",
        };

        this.handleChangeWhereRememberToken = this.handleChangeWhereRememberToken.bind(this);
    }

        /** Изменяет состояние "Remember my" */
    handleChangeWhereRememberToken(isRememberMy) {
        this.setState({
            ...this.state,
            whereRememberToken: isRememberMy ? REMEMBER_LOCAL : REMEMBER_SESSION
        })
    }

    /** Устанавливает параметр надо ли отображать каптчу */
    setShowCaptcha = (isShowCaptcha) => {
        this.setState({
            ...this.state,
            isShowCaptcha: isShowCaptcha
        });
    }

    /**
     * Добавляет системное сообщение
     * @param type
     * @param message
     */
    _addSystemMessage(type, message) {
        store.dispatch(addSystemMessage(type, message));
    }

    /** Для формы логина передаёт параметр "remember my" */
    getRememberMy() {
        return this.state.whereRememberToken === REMEMBER_LOCAL
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
        // this.setState({
        //     whereRememberToken: whereRememberToken()
        // });
        // Защита от бесконечного цикла.
        let block = false;
        this.sendBeginDataRequest()
           .then(resp => {
               if (!resp && !block) {
                   // Прежде чем запустить рекурсию, инициализирую блок от бе конечного цикла.
                   block = true;
                   this.sendBeginDataRequest();
                   this._addSystemMessage("warning", "Токен доступа истёк");
               }
           })
    }

    /** Отправляет запрос на получение начальных данных */
    sendBeginDataRequest = () => {
        // let options = {headers: getFetchHeaders()};
        // fetch("/api/begin-data", options)
        //     .then(response => {
        //         if (response.status === 200)
        //         // Если ответ корректный, то просто преобразую его в JSON и возвращаю дальше.
        //         return response.json();
        //     })
       return sendRequest("/api/begin-data", "GET")
            .then(data => {
                store.dispatch(setHeaderDate(data));
                store.dispatch(changeUserAuthentication(data));
                store.dispatch(changeMainMenu(data));
                this.setState({
                    isShowCaptcha: data.isShowCaptcha,
                    currentYear: data.currentYear,
                    siteDomainName: data.siteDomainName,
                    isLoading: false,
                })
                return true
            })
            .catch(error => {
                if (error.name === "TokenAccessExpired") {
                    removeToken();
                    return false
                }
                return true
            })

        // fetch("/api/begin-data/1", options)
        //     .then(resolveBeginData("/api/begin-data"))
        //     .then(data => {
        //         // store.dispatch(setHeaderDate(data));
        //         // store.dispatch(changeUserAuthentication(data));
        //         store.dispatch(changeMainMenu(data));
        //         this.setState({
        //             isShowCaptcha: data.isShowCaptcha,
        //             currentYear: data.currentYear,
        //             siteDomainName: data.siteDomainName,
        //             isLoading: false,
        //         })
        //     })
    }

    /** Возвращает основное содержимое через маршрутизацию */
    getRouter() {
        return(
            <Router>
                <Provider store={store}>
                    <Header />
                    <UnderHeader isAdmin={false} />
                    <Routes>
                        <Route element={<Body />} >
                            <Route path="/" element={<p>Главная</p>} />
                            <Route path="/login" element={
                                <Login_W setStyle={this.setListStyles} clearStyle={this.clearListStyles}
                                             onChangeIsRememberMe={this.handleChangeWhereRememberToken}
                                         isShowCaptcha={this.state.isShowCaptcha} setShowCaptcha={this.setShowCaptcha}
                                             isRememberMy={this.getRememberMy()} />} />
                            <Route path="/logout" element={<Logout_W />} />
                            <Route path="/about" element={<p>О сайте</p>} />
                            <Route path="/copyright" element={<p>Права на сайт</p> } />
                            <Route path="/contact" element={<p>Контакты</p>} />
                            <Route path="/signup" element={<p>Регистрация</p>} />
                            <Route path="/get-all-users" element={<AllUsers />} />
                            <Route path="*" element="Not found" />
                        </Route>
                    </Routes>
                </Provider>
            </Router>
        );
    }

    render() {
        return(
            <div className="wrap">
                {this.state.isLoading ? <p>Загрузка...</p> : this.getRouter()}
            </div>
        )
    }
}
