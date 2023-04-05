import React from "../../../../../../../../../../node_modules/react";
import {bindActionCreators} from "../../../../../../../../../../node_modules/redux"
import {connect} from "../../../../../../../../../../node_modules/react-redux";
import {changeShowResultBoiling} from "../../TestReduxSingleStore/store/actions";
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
                    onChange={(e) => {
                        props.onChangeShowResultBoiling(e.target.checked);
                    }}
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

function mapStateToProps(state) {
    return {
        isShowResultBoiling: state.isShowResultBoiling,
    }
}

function mapDispatchToProps(dispatch) {
    return {
        onChangeShowResultBoiling: bindActionCreators(changeShowResultBoiling, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(BoilingVerdict);