import React, {Component} from "../../../../../../../../../../node_modules/react";
import {bindActionCreators} from "../../../../../../../../../../node_modules/redux"
import {connect} from "../../../../../../../../../../node_modules/react-redux";
import {setAboutPage} from "../../../../../store/actions/cachePagesActions";

class About extends Component {
    setHtml = () => {
        if (!this.props.html.length) {
            fetch("/api/get-about-page")
                .then(response => response.text())
                .then(html => {
                    this.props.setAboutPageCache(html);
                });
        }
    }

    componentDidMount() {
        // Устанавливает стили для страницы
        this.props.setStyle(["main/css/about"]);
        this.setHtml();
    }

    componentWillUnmount() {
        // Удаляет стили страницы
        this.props.clearStyle();
    }

    render() {
        return (
            <div className="main-about" dangerouslySetInnerHTML={{__html: this.props.html}} >
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        html: state.cachePage.aboutPage
    }
}

function mapDispatchToProps(dispatch) {
    return {
        setAboutPageCache: bindActionCreators(setAboutPage, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(About);