import React from "../../../../../../../../../../node_modules/react";
import {connect } from "../../../../../../../../../../node_modules/react-redux";
import mapStateToProps from "../store/mapStateToProps";
import mapDispatchToProps from "../store/mapDispatchToProps";
import TemperatureInput from "../components/TemperatureInput";
import BoilingVerdict_W from "./BoilingVerdict";

// import store from "../store/store";
// import changeTemperature from "../store/actions/changeTemperature";

// Ручной вызов действия (action) из хранилища (store)
// store.dispatch(changeTemperature('c', temperature));

function Calculator(props) {
    // Если в mapDispatchToProps не используется bindActionCreators, то действие должно быть вручную запущено через dispatch хранилища.
    // const onTemperatureCelsiusChange = (temperature) => {store.dispatch(props.onTemperatureChange('c', temperature))}
    const onTemperatureCelsiusChange = (temperature) => {props.onTemperatureChange('c', temperature)};
    const onTemperatureFahrenheitChange = (temperature) => {props.onTemperatureChange('f', temperature)};
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

export default connect(mapStateToProps("Calculator"), mapDispatchToProps("Calculator"))(Calculator);