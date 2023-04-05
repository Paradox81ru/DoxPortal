import React from "../../../../../../../../../../node_modules/react";
import {Calculator as CalculatorComponent} from "../components/Calculator";

function toCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5 / 9;
}

function toFahrenheit(celsius) {
    return (celsius * 9 / 5) + 32;
}

function tryConvert(temperature, convert) {
    const input = parseFloat(temperature);
    if (Number.isNaN(input)) {
        return '';
    }
    const output = convert(input);
    const rounded = Math.round(output * 1000) / 1000;
    return rounded.toString();
}

export default class Calculator extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            temperature: '',
            scale: 'c',
            isShowResultBoiling: true
        };
    }

    handleCelsiusChange = (temperature) => {
        this.setState({scale: 'c', temperature});
    }

    handleFahrenheitChange = (temperature) => {
        this.setState({scale: 'f', temperature});
    }

    handleCheckShowBoiling = (isShow) => {
        this.setState({isShowResultBoiling: isShow});
    }

    render() {
        const scale = this.state.scale;
        const temperature = this.state.temperature;
        const isShowResultBoiling = this.state.isShowResultBoiling;
        const celsius = scale === 'f' ? tryConvert(temperature, toCelsius) : temperature;
        const fahrenheit = scale === 'c' ? tryConvert(temperature, toFahrenheit) : temperature;
        return (
            <CalculatorComponent
                celsius={celsius}
                fahrenheit = {fahrenheit}
                isShowResultBoiling = {isShowResultBoiling}
                onTemperatureCelsiusChange = {this.handleCelsiusChange}
                onTemperatureFahrenheitChange = {this.handleFahrenheitChange}
                onHandleCheckShowBoiling = {this.handleCheckShowBoiling}
            />
        )
    }
}