import React, {Component} from "../../../../../../../../../../node_modules/react";

const scaleNames = {  c: 'Цельсия',  f: 'Фаренгейта'};

export default class TemperatureInput extends Component {
  constructor(props) {
    super(props);
  }

  handleChange = (e) => {
    this.props.onTemperatureChange(e.target.value);
  }

  render() {
    const temperature = this.props.temperature;
    const scale = this.props.scale;
    return (
      <fieldset>
        <legend>Введите температуру в градусах {scaleNames[scale]}:</legend>
          <input value={temperature}
               onChange={this.handleChange} />
      </fieldset>
    );
  }
}