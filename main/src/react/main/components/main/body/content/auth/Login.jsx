import React, {Component} from "../../../../../../../../../../node_modules/react";
import {bindActionCreators} from "../../../../../../../../../../node_modules/redux"
import {connect} from "../../../../../../../../../../node_modules/react-redux";
import {Navigate, Link} from "../../../../../../../../../../node_modules/react-router-dom";
import Row from '../../../../../../../../../../node_modules/react-bootstrap/Row';
import Col from '../../../../../../../../../../node_modules/react-bootstrap/Col';

import {setLoginForm} from "../../../../../store/actions/cachePagesActions";
import {changeMainMenu, changeUserAuthentication, changeUserGroups} from "../../../../../store/actions/generalActions";
import {getFetchHeaders} from "../../../../../lib/send_request_util";
import {saveToken, isRememberMiToWhereRememberToken} from "../../../../../lib/auth_token_util";
import {
    handleSimpleFieldValueChange,
    removeAllFieldsErrors,
    setFieldsError,
    setNonFieldError
} from "../../../../../lib/FormUtils";
import {UnauthorizedError} from "../../../../../lib/errors";

import FormGroup from "../../../../widgets/form/FormGroup";
import NonFieldError from "../../../../widgets/form/NonFieldError";
import Captcha from "../../../../widgets/form/Captcha";

class Login extends Component {
    constructor() {
        super();
        this.captchaRef = React.createRef();
        this.state = {
            isRedirect: false,
            fields: {
                username: "",
                password: "",
                rememberMe: false,
                verifyCaptcha: ""
            },
            errors: {
                non_field_errors: "",
                verifyCaptcha: ""
            }
        }
    }

    /** Обрабатывает изменения ввода в поля */
    handleChange = handleSimpleFieldValueChange(this);

    /** Обрабатывает сабмит формы */
    handleSubmit = (event) => {
        event.preventDefault();
        this.handleLogin(this.state.fields);
    }

    /** Обрабатывает авторизацию пользователя */
    handleLogin(fields) {
        let headers = getFetchHeaders();
        let options = {headers: headers};
        options["method"] = "POST";
        options["body"] = JSON.stringify(fields);

        fetch("/api/auth/login", options)
            .then(response => {
                if ([200, 400, 401].includes(response.status) )
                    return response.json();
                else
                    throw new Error(response.statusText)
            })
            .then(data => {
                removeAllFieldsErrors(this);
                if (data.hasOwnProperty("error")) {
                    // Если ошибка валидации полей формы, и установлена ошибка вне поля,
                    if (data["error"] === "ValidationError" ) {
                        // то показываю ошибку.
                        // setNonFieldError(data["non_field_errors"], this);
                        setFieldsError(data["fields_error"], this)
                        // и если надо, отображаю каптчу.
                        this.props.setShowCaptcha(data["isShowCaptcha"]);
                    }
                    // else if (data["error"] === "CaptchaInvalid") {
                    //     setFieldError("verifyCaptcha", data["message"], this);
                    //     this.props.setShowCaptcha(true);
                    // }
                } else {
                    this.props.setShowCaptcha(false);
                    this.setDataLogin(data);
                    this.redirect();
                }
            })
            .catch(error => {
                removeAllFieldsErrors(this);
                setNonFieldError("Неизвестная ошибка " + error.message, this);
            })
    }

    /** Переходит на другую страницу */
    redirect = () => {
        this.setState({
            ...this.state,
            isRedirect: true
        })
    }

    /** Устанавливает данные после авторизации */
    setDataLogin = (data) => {
        this.props.handleChangeMainMenu(data);
        this.props.handleChangeUserAuthentication(data);
        this.props.handleChangeUserGroups(data);
        this.props.onChangeIsRememberMe(this.state.fields.rememberMe);
        saveToken(isRememberMiToWhereRememberToken(this.state.fields.rememberMe), data.token);
    }

    /** Запрашивает и запоминает данные для формирования формы авторизации */
    setDataForm = () => {
        if (!this.props.dataForm.length) {
            fetch("/api/get-login-form-data")
                .then(response => response.json())
                .then(data => {
                    this.props.handleSetLoginFormCache(data);
                });
        }
    }

    componentDidMount() {
        // Устанавливает стили для страницы
        this.props.setStyle(["common/css/form"]);
        this.setState({
            ...this.state,
            fields: {
                ...this.state.fields,
                rememberMe: this.props.isRememberMy
            }
        })
        this.setDataForm();
    }

    componentWillUnmount() {
        // Удаляет стили страницы
        this.props.clearStyle();
    }

    render() {
        if (this.state.isRedirect) {
            return (
                <Navigate replace to="/"/>
            )
        } else {
            const formGroups = this.props.dataForm.map(data => {
                if (data.fieldName === "verifyCaptcha" && !this.props.isShowCaptcha) {
                    return null;
                }
                return (
                    <FormGroup key={data.fieldName} value={this.state.fields[data.fieldName]}
                               errors={this.state.errors[data.fieldName]}
                               handleChange={this.handleChange} dataField={data}
                               extraClass={["mb-3"]}/>)
            });
            return (
                <div className="accounts-login">
                    <h1 className="title">Вход</h1>
                    <p>Пожалуйста, заполните следующие поля для входа:</p>
                    <Row>
                        <Col lg={6}>
                            <form onSubmit={this.handleSubmit} action="/login" method="post">
                                {this.state.errors.non_field_errors.length > 0 && <NonFieldError errors={this.state.errors.non_field_errors}/>}
                                {formGroups}
                                {this.props.isShowCaptcha && <Captcha ref={this.captchaRef}/>}
                                <div style={{color: "#999", margin: "1em 0"}}>
                                    Если вы забыли свой пароль, вы можете <Link to="/accounts/request-password-reset">сбросить
                                    его</Link>.
                                </div>
                                <button type="submit" className="btn btn-primary" name="login-button">Войти</button>
                            </form>
                        </Col>
                    </Row>
                </div>
            )
        }
    }
}

function mapStateToProps(state) {
    return {
        dataForm: state.hasOwnProperty("cachePage") ? state.cachePage.loginForm : state.loginForm
    }
}

function mapDispatchToProps(dispatch) {
    return {
        handleSetLoginFormCache: bindActionCreators(setLoginForm, dispatch),
        handleChangeMainMenu: bindActionCreators(changeMainMenu, dispatch),
        handleChangeUserAuthentication: bindActionCreators(changeUserAuthentication, dispatch),
        handleChangeUserGroups: bindActionCreators(changeUserGroups, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Login);