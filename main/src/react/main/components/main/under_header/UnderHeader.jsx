import React, {Component} from "../../../../../../../../node_modules/react";
import {useLocation} from "../../../../../../../../node_modules/react-router-dom"
import Breadcrumb_W from "./BreadcrumbBlock";
import LoginField_W from "./LoginField";

export default function UnderHeader(props) {
    const location = useLocation();
    return (
        <div className="container under-header">
            <Breadcrumb_W currentURL={location.pathname} isAdmin={props.isAdmin} />
            <LoginField_W isAdmin={props.isAdmin}  />
        </div>
    )
}