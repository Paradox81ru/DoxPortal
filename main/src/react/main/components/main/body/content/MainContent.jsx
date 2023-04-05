import React, {Component} from "../../../../../../../../../node_modules/react";
import {Outlet} from "../../../../../../../../../node_modules/react-router-dom"
import Alert from "./Alert";
import Col from '../../../../../../../../../node_modules/react-bootstrap/Col';
import {bindActionCreators} from "../../../../../../../../../node_modules/redux"
import {connect} from "../../../../../../../../../node_modules/react-redux";
import {removeSystemMessage} from "../../../../store/actions/generalActions";

class MainContent extends Component{
    /** Обрабатывает событие удаления сообщения */
    handleRemoveMessage = (messageId) => {
        this.props.handleRemoveSystemMessage(messageId);
    }

    render() {
        const messages = this.props.messages;
        // Это всё-таки мой собственный Alert.
        const messageBlocks = Object.keys(messages).map(key =>
            <Alert key={key}
                   messageId={key}
                   type={this.props.messages[key]["type"]}
                   message={this.props.messages[key]["message"]}
                   isClose
                   isAnimation
                   onCloseMessage={this.handleRemoveMessage}>
                {messages[key]["message"]}
            </Alert>)

        const attrs = this.props.admin ? {id: "admin-main"} : {sm: 11, lg: 9,  id: "main-content"}
        return (
            <Col {...attrs}>
                <div id="messages" style={{width: "840px"}}>
                    {messageBlocks}
                </div>
                <Outlet/>
            </Col>
        )
    }
}

function mapStateToProps(state) {
    return {
        messages: state.hasOwnProperty("general") ? state.general.systemMessages : state.systemMessages
    }
}

function mapDispatchToProps(dispatch) {
    return {
        handleRemoveSystemMessage: bindActionCreators(removeSystemMessage, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MainContent);