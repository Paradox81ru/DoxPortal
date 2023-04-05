import React from "../../../../../../../../../../node_modules/react";
import {connect} from "../../../../../../../../../../node_modules/react-redux";
import {bindActionCreators} from "../../../../../../../../../../node_modules/redux"
import TemperatureInput from "../components/TemperatureInput";
import BoilingVerdict_W from "./BoilingVerdict";
import {toCelsius, toFahrenheit, tryConvert} from "../../TestReduxSingleStore/lib";
import {changeTemperature} from "../../TestReduxSingleStore/store/actions";

// import store from "../store/store";
// import changeTemperature from "../store/actions/changeTemperature";

// Ручной вызов действия (action) из хранилища (store)
// store.dispatch(changeTemperature('c', temperature));

function Calculator(props) {
    // Если в mapDispatchToProps не используется bindActionCreators, то действие должно быть вручную запущено через dispatch хранилища.
    // const onTemperatureCelsiusChange = (temperature) => {store.dispatch(props.onTemperatureChange('c', temperature))}
    const onTemperatureCelsiusChange = (temperature) => {
        props.onTemperatureChange('c', temperature)
    };
    const onTemperatureFahrenheitChange = (temperature) => {
        props.onTemperatureChange('f', temperature)
    };
    return (
        <div>
            <TemperatureInput
                scale="c"
                temperature={props.celsius}
                onTemperatureChange={onTemperatureCelsiusChange}/>
            <TemperatureInput
                scale="f"
                temperature={props.fahrenheit}
                onTemperatureChange={onTemperatureFahrenheitChange}/>
            <BoilingVerdict_W
                celsius={props.celsius}
            />
        </div>
    );
}

function mapStateToProps(state) {
    return {
        celsius: state.calc.scale === 'f' ? tryConvert(state.calc.temperature, toCelsius) : state.calc.temperature,
        fahrenheit: state.calc.scale === 'c' ? tryConvert(state.calc.temperature, toFahrenheit) : state.calc.temperature
    }
}

function mapDispatchToProps(dispatch) {
    return {
        // Если не использовать bindActionCreators то в компоненте действие onTemperatureChange
        // придется самому запускать через dispatch хранилища.
        // onTemperatureChange: changeTemperature
        onTemperatureChange: bindActionCreators(changeTemperature, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Calculator);