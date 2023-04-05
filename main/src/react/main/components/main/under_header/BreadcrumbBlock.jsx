import React, {Component} from "../../../../../../../../node_modules/react";
import {Link} from "../../../../../../../../node_modules/react-router-dom"
import {connect} from "../../../../../../../../node_modules/react-redux";

import Breadcrumb from '../../../../../../../../node_modules/react-bootstrap/Breadcrumb';

class BreadcrumbBlock extends Component {
    /**
     * Возвращает список хлебных крошек
     * @returns
     */
    getBreadCrumbs() {
        let currentURL = this.props.currentURL;
        // Если в крошках путь не найден,
        if (!this.props.breadcrumbList.hasOwnProperty(currentURL))
            // то отобразится просто текст "Главная"
            return <Breadcrumb.Item active>Главная</Breadcrumb.Item>;

        // Иначе беру крошки соответствующие текущему URL.
        let breadcrumbs = this.props.breadcrumbList[currentURL];
        return breadcrumbs.map((crumb, index) =>
            crumb.length === 2
                ? <Breadcrumb.Item key={index} linkAs={Link} linkProps={{ to: crumb[1] }}>{crumb[0]}</Breadcrumb.Item>
                : <Breadcrumb.Item key={index} active>{crumb[0]}</Breadcrumb.Item>
        );
    }

    render() {
        return (
            <Breadcrumb>
                    {this.getBreadCrumbs()}
            </Breadcrumb>
        );
    }
}

function mapStatToProps(state) {
    return {
        breadcrumbList: state.hasOwnProperty("cachePage")  ? state.cachePage.header.breadcrumbList : state.breadcrumbList
    }
}

export default connect(mapStatToProps, null)(BreadcrumbBlock);