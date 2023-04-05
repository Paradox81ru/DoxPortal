// noinspection NpmUsedModulesInstalled
import React, {Component} from "react";
import FormComponent from "./FormComponent";

class Form extends Component {
        constructor(props) {
        super(props);
        this.state = {
            firstName: "",
            lastName: "",
            gender: "",
            favColor: "blue",
            dietaryRestrictions: {
                isVegan: false,
                isKosher: false,
                isLactoseFree: false
            }
        }
    }

    handleChange = (event) => {
        const {name, value, type, checked} = event.target;
        type === "checkbox" ?
            this.setState(prevState => ({
                dietaryRestrictions: {
                    ...prevState.dietaryRestrictions,
                    [name]: checked
                }
            })) :
            this.setState({
                [name]: value
            });
    }

    handleSubmit = (event) => {
        event.preventDefault();
        console.log("Отправка данных формы...");
    }

    render() {
        return (
            <FormComponent
                handleChange={this.handleChange}
                handleSubmit={this.handleSubmit}
                data={this.state}
            />
        )
    }
}

export default Form