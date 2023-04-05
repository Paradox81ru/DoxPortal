import React from "../../../../../../../../../../node_modules/react";
import {connect } from "../../../../../../../../../../node_modules/react-redux";
import mapStateToProps from "../store/mapStateToProps";
import mapDispatchToProps from "../store/mapDispatchToProps";
// import store from "../store/store";
// import changeShowResultBoiling from "../store/actions/changeShowResultBoiling";

// Ручной вызов действия (action) из хранилища (store)
// store.dispatch(changeShowResultBoiling(e.target.checked));

function BoilingVerdict(props) {
    return (
        <div>
            <label>
                <input
                    type="checkbox"
                    onChange={(e) => {props.onChangeShowResultBoiling(e.target.checked);}}
                    checked={props.isShowResultBoiling}
                />
                Показать результат
            </label>
            {boilingResult(props)}
        </div>
    )
}

function boilingResult(props) {
    if (!props.isShowResultBoiling)
        return null;
    if (props.celsius >= 100) {
        return <p>Вода закипит.</p>;
    }
    return <p>Вода не закипит.</p>;
}

export default connect(mapStateToProps("BoilingVerdict"), mapDispatchToProps("BoilingVerdict"))(BoilingVerdict);