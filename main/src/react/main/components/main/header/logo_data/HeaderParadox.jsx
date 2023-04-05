import React, {Component} from "../../../../../../../../../node_modules/react";
import {connect} from "../../../../../../../../../node_modules/react-redux";

function HeaderParadox(props) {
    return (
            <div className="header-paradox" title={props.header}>
                {props.content}
            </div>
    )
}

function mapStateToProps(state) {
    return {
        header: state.cachePage.header.paradoxData.header,
        content: state.cachePage.header.paradoxData.content
    }
}

export default connect(mapStateToProps, null)(HeaderParadox);
