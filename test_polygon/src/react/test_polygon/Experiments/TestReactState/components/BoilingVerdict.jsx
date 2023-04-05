import React from "../../../../../../../../../../node_modules/react";

export default class BoilingVerdict extends React.Component {
    constructor(props) {
        super(props);
    }

    get boilingResult() {
        if (!this.props.isShowResultBoiling)
            return null;
        if (this.props.celsius >= 100) {
            return <p>Вода закипит.</p>;
        }
        return <p>Вода не закипит.</p>;
    }

    onChange = (e) => {
         this.props.onCheckShowBoiling(e.target.checked)
    }

    render() {
        return (
            <div>
                <label>
                <input
                    type="checkbox"
                    onChange={this.onChange}
                    checked={this.props.isShowResultBoiling}
                />
                Показать результат
                </label>
                {this.boilingResult}
            </div>
        )
    }
}