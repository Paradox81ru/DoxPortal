import React from "../../../../../../../../../../node_modules/react";
import TemperatureInput from "./TemperatureInput";
import BoilingVerdict from "./BoilingVerdict";

export class Calculator extends React.Component {
    render() {
        return (
            <div>
                <TemperatureInput
                    scale="c"
                    temperature={this.props.celsius}
                    onTemperatureChange={this.props.onTemperatureCelsiusChange}/>
                <TemperatureInput
                    scale="f"
                    temperature={this.props.fahrenheit}
                    onTemperatureChange={this.props.onTemperatureFahrenheitChange}/>
                <BoilingVerdict
                    isShowResultBoiling={this.props.isShowResultBoiling}
                    onCheckShowBoiling={this.props.onHandleCheckShowBoiling}
                    celsius={parseFloat(this.props.celsius)}/>
            </div>
        );
    }
}