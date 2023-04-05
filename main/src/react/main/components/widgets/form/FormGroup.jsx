import React, {Component} from "../../../../../../../../node_modules/react";
import Form from '../../../../../../../../node_modules/react-bootstrap/Form';
import OverlayTrigger from '../../../../../../../../node_modules/react-bootstrap/OverlayTrigger';
import Tooltip from '../../../../../../../../node_modules/react-bootstrap/Tooltip';
import PasswordInputField from "./PasswordInputField";
import {isString} from "../../../lib/doxHelper";

export default class FormGroup extends Component {
    /** Возвращает нужный тип поля */
    getInput() {
        const dataField = this.props.dataField;
        let attributes = {
            type: dataField.fieldType,
            name: dataField.fieldName,
            value: this.props.value,
            required: dataField.isRequired,
            onChange: this.props.handleChange,
            as: dataField.fieldType === "textarea" ? 'textarea' : "input",
            isInvalid: this.isErrors()
        }

        if (dataField.inputAttributes != null)
            attributes = Object.assign(attributes, dataField.inputAttributes);

        switch (dataField.fieldType) {
            case "password":
                return <PasswordInputField {...attributes}  />
            case "checkbox":
                return <Form.Check {...attributes} label={dataField.label} />
            default:
                return <Form.Control {...attributes} />;
        }
    }

    getFormGroupClass() {
        const dataField = this.props.dataField;

        // Если поле обязательное, то добавляю в класс "required".
        let extraClass = dataField.isRequired ? ["required"] : null;
        // Если указали дополнительные классы, то добавляю в группу и их.
        if (this.props.extraClass != null) {
            extraClass = extraClass != null ? [...extraClass, ...this.props.extraClass] : this.props.extraClass;
        }

        // Формирую строку дополнительных классов через пробел,
        const cls = extraClass != null ? " " + extraClass.join(" ") : ""
        // и формирую класс поля группы формы.
        return  "form-group field-" + dataField.fieldName + cls;
    }

    /** Есть ли ошибки */
    isErrors() {
        if (this.props.errors != null) {
            if (Array.isArray(this.props.errors)) {
                if (this.props.errors.length > 0)
                    return true;
            } else if(isString(this.props.errors)) {
                return Boolean(this.props.errors);
            } else {
                throw new Error(`Ошибка FormGroup, поле "${this.props.dataField.fieldName}": ошибки должны быть представлены в виде строки или списка.`);
            }
        }
        return false;
    }

    /** Возвращает всплывающую подсказку помощи*/
    getTooltip() {
        const dataField = this.props.dataField;
        const helpList = dataField.helper.map((help, index) => <li key={index}>{help}</li>);
        return (
            <Tooltip id={`tooltip-${dataField.fieldName}`}>
                <ul className="help-text">
                    {helpList}
                </ul>
            </Tooltip>
        )
    }

    render() {
        const dataField = this.props.dataField;
        // const _errors = (this.props.errors !== undefined && isString(this.props.errors)) ? [this.props.errors] : this.props.errors;
        const _errors = this.props.errors === undefined ? [] : isString(this.props.errors) ? [this.props.errors] : this.props.errors;
        const errors = _errors.map((error, index) => <li key={index}>{error}</li>)
        const questionImage = <img alt="?" src="static/common/images/icons32/question.png" data-bs-toggle="tooltip"
                                   className="help-sign-question" data-bs-original-title="" title=""/>
        const inputBlock = this.props.dataField.helper
            ? <div className="input-img-block">
                {this.getInput()}
                <Form.Control.Feedback as="ul" type="invalid">
                    {errors}
                </Form.Control.Feedback>
                <OverlayTrigger overlay={this.getTooltip()} triger="hover" placement="auto">
                    {questionImage}
                </OverlayTrigger>
            </div>
            : <>
                {this.getInput()}
                <Form.Control.Feedback as="ul" type="invalid">
                    {errors}
                </Form.Control.Feedback>
            </>;

            return (
            <Form.Group className={this.getFormGroupClass()} controlId={dataField.id}>
                {!(this.props.dataField.fieldType === "checkbox") && <Form.Label>{dataField.label}</Form.Label>}
                {inputBlock}
            </Form.Group>
        )
    }
}