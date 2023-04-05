import React, {Component} from "../../../../../../../../../../node_modules/react";
import {Link} from "../../../../../../../../../../node_modules/react-router-dom";
import {Form} from "../../../../../../../../../../node_modules/react-router-dom";

export default class FieldSearch extends Component{
    handleSubmit(event) {
        event.preventDefault();
    }

    /** Должна ли отображаться кнопка поиска с формой */
    isFormSearch() {
        const beginPathList = ["blog", "software", "service", "picture"];
        const beginPath = this.props.currentUrl.split("/")[1];
        return beginPathList.indexOf(beginPath) > -1;
    }

    render() {
        const link =
            <Link to="/extended-search"
                  className="btn btn-orange-gradient btn-outline-secondary btn-extended-search"
                  title="Расширенный поиск">
                <i className="fas fa-angle-double-left fa-2x"></i>
            </Link>

        const buttonSearch =
            <div className="input-group input-group-sm field-search">
                <div className="input-group-prepend">
                    {link}
                </div>
            </div>

        const formSearch =
            <form onSubmit={this.handleSubmit} method="get" action="/blog/search">
                <div className="input-group input-group-sm field-search">
                    {link}
                    <input className="form-control" aria-label="поиск" placeholder="поиск" type="text" name="text_find" />
                    <button type="submit"
                            className="btn btn-outline-secondary btn-orange-gradient btn-outline-secondary btn-search"
                            title="Быстрый поиск">
                        <i className="fas fa-search fa-2x"></i>
                    </button>
                </div>
            </form>

        return (
            <React.Fragment >
                {this.isFormSearch() ? formSearch : buttonSearch}
            </React.Fragment>
        )
    }
}
