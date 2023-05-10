import React, {Component} from "../../../../../../../../../../node_modules/react";
import {bindActionCreators} from "../../../../../../../../../../node_modules/redux"
import {connect} from "../../../../../../../../../../node_modules/react-redux";

import Row from '../../../../../../../../../../node_modules/react-bootstrap/Row';
import Col from '../../../../../../../../../../node_modules/react-bootstrap/Col';
import Form from '../../../../../../../../../../node_modules/react-bootstrap/Form';
import Button from '../../../../../../../../../../node_modules/react-bootstrap/Button';
import {Navigate} from "../../../../../../../../../../node_modules/react-router-dom";
import FormGroup from "../../../../widgets/form/FormGroup";
import NonFieldError from "../../../../widgets/form/NonFieldError";

import {getFetchHeaders} from "../../../../../lib/send_request_util";
import {handleSimpleFieldValueChange} from "../../../../../lib/FormUtils";
import {addSystemMessage} from "../../../../../store/actions/generalActions";

import {
    setFieldsError,
    removeAllFieldsErrors
}
    from "../../../../../lib/FormUtils";

const SUCCESS_REDIRECT = "signup-success";
const INVALID_REDIRECT = "signup-invalid";

class Register extends Component {
    constructor() {
        super();
        this.state = {
            redirectTo: "",
            dataForm: [],
            fields: {
                username: "",
                email: "",
                password: "",
                passwordConfirm: ""
            },
            errors: {
                _ : [],
                username: [],
                email: [],
                password: [],
                passwordConfirm: []
            }
        }
    }

    /** Обрабатывает сабмит формы */
    handleSubmit = (event) => {
        event.preventDefault();
        this.handleRegister(this.state.fields);
    }

    handleRegister = (fields) => {
        let headers = getFetchHeaders();
        let options = {headers: headers};
        options["method"] = "POST";
        options["body"] = JSON.stringify(fields);

        fetch("/api/auth/signup", options)
            .then(response => {
                if (response.status === 200)
                    return response.json();
            })
            .then(response => {
                // Если данные формы успешно отправлены,
                if (response.hasOwnProperty("success")) {
                    // // то удаляю все ошибки,
                    // removeAllFieldsErrors(this);
                    // // очищаю поля
                    // clearAllFieldsValue(this);
                    // и отображаю сообщение об успешной регистрации нового пользователя.
                    this.setRedirect(SUCCESS_REDIRECT)
                    // this.props.handleAddSystemMessage("success", response['message']);
                } else if (response.hasOwnProperty("error")) {
                    removeAllFieldsErrors(this);
                    // Если это ошибка проверки полей,
                    if (response["error"] === "FieldValidateError") {
                        // то отображу ошибки около полей.
                        setFieldsError(response["data"], this);
                    } else if (response["error"] === "MessagingError") {
                        // А если это ошибка отправки сообщения по почте, то перенаправлю на страницу сообщения.
                        this.setRedirect(INVALID_REDIRECT);
                    }
                }
            })
            .catch(error => {
                this.props.handleAddSystemMessage("danger", "Неизвестная ошибка: " + error);
            });
    }

    /**
     * Устанавливает перенаправление
     * @param redirect путь перенаправления
     */
    setRedirect(redirect) {
        this.setState({
            ...this.state,
            redirectTo: redirect
        });
    }

    setDataForm = () => {
        fetch("/api/get-register-form-data")
            .then(response => response.json())
            .then(data => {
                this.setState({
                    ...this.state,
                    dataForm: data
                })
            })
    }

    /** Обрабатывает изменения ввода в поля */
    handleChange = handleSimpleFieldValueChange(this);

    componentDidMount() {
        // Устанавливает стили для страницы
        this.props.setStyle(["common/css/form"]);
        this.setDataForm();
    }

    componentWillUnmount() {
        // Удаляет стили страницы
        this.props.clearStyle();
    }

    render() {
        if (this.state.redirectTo) {
            return (<Navigate replace to={"/site-message/" + this.state.redirectTo}/>);
        }

        const formGroups = this.state.dataForm
            .map(data =>
                <FormGroup key={data.fieldName} value={this.state.fields[data.fieldName]}
                           errors={this.state.errors[data.fieldName]}
                           handleChange={this.handleChange} dataField={data}
                           extraClass={["mb-3"]}/>);
        return (
        <div className="account-signup">
            <h1 className="title">Регистрация</h1>
            <p>Пожалуйста, заполните следующие поля, чтобы зарегистрироваться:</p>
            <Row>
                <Col lg={6}>
                    <Form onSubmit={this.handleSubmit}>
                        {formGroups}
                        {this.state.errors._.length > 0 && <NonFieldError errors={this.state.errors._}/>}
                        <Button variant="primary" type="submit" name="signup-button">Зарегистрироваться</Button>
                    </Form>
                </Col>
            </Row>
        </div>
        )
    }
}

function mapDispatchToProps(dispatch) {
    return {
        handleAddSystemMessage: bindActionCreators(addSystemMessage, dispatch)
    }
}

export default connect(null, mapDispatchToProps)(Register);