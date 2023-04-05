import React, {Component} from "../../../../../../../../node_modules/react";
import Form from '../../../../../../../../node_modules/react-bootstrap/Form';
import InputGroup from '../../../../../../../../node_modules/react-bootstrap/InputGroup';
import Button from '../../../../../../../../node_modules/react-bootstrap/Button';

export default class PasswordInputField extends Component {
    constructor() {
        super();
        this.state = {
            isPasswordShow: false
        }
    }

    handleButtonIsShow = () => {
        this.setState(prevState => {
            return {
                isPasswordShow: !prevState.isPasswordShow
            }
        } )
    }

    render() {
        let attributes = {
            type: this.state.isPasswordShow ? "text" : "password",
            name: this.props.name,
            value: this.props.value,
            required: this.props.required,
            onChange: this.props.onChange,
            isInvalid: this.props.isInvalid
        }
        if (this.props.extraAttributes != null)
            attributes = Object.assign(attributes, this.props.extraAttributes);
        return (
            <InputGroup className={this.props.isInvalid && "is-invalid"}>
                <Form.Control {...attributes} />
                <Button onClick={this.handleButtonIsShow} variant="default" >
                    <i className={"fas fa-lg fa-eye" + (this.state.isPasswordShow ? "" : "-slash") }></i>
                </Button>
            </InputGroup>
        )
    }
}