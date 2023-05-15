import React, {Component} from "../../../../../../../../node_modules/react";
import {Link} from "../../../../../../../../node_modules/react-router-dom"
import {connect} from "../../../../../../../../node_modules/react-redux";

class Breadcrumb1 extends Component {
    /**
     * Возвращает список хлебных крошек
     * @returns {JSX.Element}
     */
    getBreadCrumbs() {
        let currentURL = this.props.currentURL;
        // Если в крошках путь не найден,
        if (!this.props.breadcrumbList.hasOwnProperty(currentURL))
            // то отобразится просто текст "Главная"
            return <li className="breadcrumb-item active" aria-current="page">Главная</li>;

        // Иначе беру крошки соответствующие текущему URL.
        let breadcrumbs = this.props.breadcrumbList[currentURL];
        return breadcrumbs.map((crumb, index) =>
            crumb.path != null
                ? <li key={index} className="breadcrumb-item"><Link to={crumb.path}>{crumb.title}</Link></li>
                : <li key={index} className="breadcrumb-item active" aria-current="page">{crumb.title}</li>
        );
    }

    render() {
        return (
            <nav aria-label="breadcrumb">
                <ol className="breadcrumb">
                    {this.getBreadCrumbs()}
                </ol>
            </nav>
        );
    }
}

function mapStatToProps(state) {
    return {
        breadcrumbList: state.hasOwnProperty("cachePage")  ? state.cachePage.header.breadcrumbList : state.breadcrumbList
    }
}

export default connect(mapStatToProps, null)(Breadcrumb1);