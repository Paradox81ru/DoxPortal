import React, {Component} from "../../../../../../../../../../node_modules/react";
import {bindActionCreators} from "../../../../../../../../../../node_modules/redux"
import {connect} from "../../../../../../../../../../node_modules/react-redux";

import {setContactForm} from "../../../../../store/actions/cachePagesActions";

import Row from '../../../../../../../../../../node_modules/react-bootstrap/Row';
import Col from '../../../../../../../../../../node_modules/react-bootstrap/Col';
import Form from '../../../../../../../../../../node_modules/react-bootstrap/Form';
import Button from '../../../../../../../../../../node_modules/react-bootstrap/Button';

import FormGroup from "../../../../widgets/form/FormGroup";
import Captcha from "../../../../widgets/form/Captcha";
import NonFieldError from "../../../../widgets/form/NonFieldError";
import {addSystemMessage} from "../../../../../store/actions/generalActions";
import {getFetchHeaders} from "../../../../../lib/send_request_util";
import {
    handleFieldValueChange,
    clearAllFieldsValue,
    setFieldsError,
    setNonFieldError,
    removeAllFieldsErrors
}
    from "../../../../../lib/FormUtils";
import {FieldValidateError} from "../../../../../lib/errors";

class Contact extends Component {
    constructor() {
        super();
        this.captchaRef = React.createRef();
        this.state = {
            fields: {
                username: "",
                email: "",
                subject: "",
                message: "",
                verifyCaptcha: ""
            },
            errors: {
                _ : [],
                username: [],
                email: [],
                subject: [],
                message: [],
                verifyCaptcha: []
            }
        }
    }

    /** Обрабатывает изменения ввода в поля */
    handleChange = handleFieldValueChange(this);

    /** Обрабатывает сабмит формы */
    handleSubmit = (event) => {
        event.preventDefault();
        this.handleContact(this.state.fields);
    }

    /** Обрабатывает отправку данных формы */
    handleContact = (fields) => {
        let headers = getFetchHeaders();
        let options = {headers: headers};
        options["method"] = "POST";
        options["body"] = JSON.stringify(fields);

        fetch("/api/contact", options)
            .then(response => {
                if (response.status === 200)
                    return response.json();
            })
            .then(response => {
                // Если данные формы успешно отправлены,
                if (response.hasOwnProperty("success")) {
                    // то удаляю все ошибки,
                    removeAllFieldsErrors(this);
                    // очищаю поля
                    clearAllFieldsValue(this);
                    this.props.handleAddSystemMessage("success", "Данные обратной связи успешно отправлены.");
                    // и обновляю рекаптчу.
                    this.captchaRef.current.reloadCaptcha();
                } else if (response.hasOwnProperty("error")) {
                    removeAllFieldsErrors(this);
                    if (response["error"] === "FieldValidateError") {
                        setFieldsError(response["data"], this);
                    } else if (response["error"] === "SendEmailError") {
                        this.props.handleAddSystemMessage("danger", response["message"]);
                        // setNonFieldError(response["message"], this);
                    }
                }
            })
            .catch(error => {
                this.props.handleAddSystemMessage("danger", "Неизвестная ошибка: " + error);
            });
    }

    setDataForm = () => {
        if (!this.props.dataForm.length) {
            fetch("/api/get-contact-form-data")
                .then(response => response.json())
                .then(data => {
                    this.props.handleSetContactFormCache(data)
                });
        }
    }

    componentDidMount() {
        // Устанавливает стили для страницы
        this.props.setStyle(["common/css/form"]);
        this.setDataForm()
    }

    componentWillUnmount() {
        // Удаляет стили страницы
        this.props.clearStyle();
    }

    render() {
        const formGroups = this.props.dataForm
            .map(data =>
                <FormGroup key={data.fieldName} value={this.state.fields[data.fieldName]}
                           errors={this.state.errors[data.fieldName]}
                           handleChange={this.handleChange} dataField={data}
                           extraClass={["mb-3"]}/>);

        return (
            <div className="main-contact">
                <h1 className="title">Обратная связь</h1>
                <p>Если у вас есть вопросы или предложения, пожалуйста заполните следующую форму для связи с нами.
                    Спасибо.</p>
                <Row>
                    <Col lg={6}>
                        <Form onSubmit={this.handleSubmit}>
                            {formGroups}
                            <Captcha ref={this.captchaRef}/>
                            {this.state.errors._.length > 0 && <NonFieldError errors={this.state.errors._}/>}
                            <Button variant="primary" type="submit" name="contact-button">Отправить</Button>
                        </Form>
                    </Col>
                </Row>
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        dataForm: state.cachePage.contactForm
    }
}

function mapDispatchToProps(dispatch) {
    return {
        handleSetContactFormCache: bindActionCreators(setContactForm, dispatch),
        handleAddSystemMessage: bindActionCreators(addSystemMessage, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Contact);