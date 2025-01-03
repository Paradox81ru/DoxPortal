import React from "react";
import Greetings from "./Greetings";
import style from "../styles/style";
import {FirstNameField, LastNameField} from "./TextField";

class SimpleForm extends React.Component {
    state = {
        firstName: "",
        firstNameError: "",
        lastName: "",
        lastNameError: "",
    };

    validateName(name) {
        const regex = /^[А-Яа-я]{3,}$/;
        return !regex.test(name)
            ? "Имя должно содержать не менее трех русских букв. Цифры и специальные символы не допускаются."
            : "";
    };

    onFirstNameBlur = () => {
        const {firstName} = this.state;
        const firstNameError = this.validateName(firstName);
        return this.setState({firstNameError});
    }

    onFirstNameChange = event => {
        this.setState({
            firstName: event.target.value
        })
    };

    onLastNameBlur = () => {
        const {lastName} = this.state;
        const lastNameError = this.validateName(lastName);
        return this.setState({lastNameError});
    };

    onLastNameChange = event => {
        this.setState({
            lastName: event.target.value
        });
    }

    render() {
        const {firstNameError, firstName, lastName, lastNameError} = this.state;
        return (
            <div style={style.form}>
                <FirstNameField onChange={this.onFirstNameChange}
                           onBlur={this.onFirstNameBlur}
                           error={firstNameError} />
                <LastNameField onChange={this.onLastNameChange}
                           onBlur={this.onLastNameBlur}
                           error={lastNameError} />
                <Greetings firstName={firstName} lastName={lastName}/>
            </div>
        )
    }
}

export default SimpleForm