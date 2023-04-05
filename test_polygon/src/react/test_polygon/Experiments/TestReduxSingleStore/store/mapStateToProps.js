import {tryConvert, toCelsius, toFahrenheit} from "../lib";

export default function mapStateToProps(component) {
    switch (component) {
        case "Calculator":
            return function (state) {
                return {
                    celsius: state.scale === 'f' ? tryConvert(state.temperature, toCelsius) : state.temperature,
                    fahrenheit: state.scale === 'c' ? tryConvert(state.temperature, toFahrenheit) : state.temperature
                }
            }
        case "BoilingVerdict":
            return function (state) {
                return {
                    isShowResultBoiling: state.isShowResultBoiling,
                    // celsius: state.scale === 'f' ? tryConvert(state.temperature, toCelsius) : state.temperature
                }
            }

        default: return undefined;
    }
}