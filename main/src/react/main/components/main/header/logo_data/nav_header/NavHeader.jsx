import React from "../../../../../../../../../../node_modules/react";
import {useLocation} from "../../../../../../../../../../node_modules/react-router-dom"
import HeaderMenu from "./HeaderMenu";
import FieldSearch from "./FieldSearch";

export default function NavHeader(props) {
    const location = useLocation();
    return(
        <nav className="nav-header">
            <HeaderMenu />
            <FieldSearch currentUrl={location.pathname} />
        </nav>
    );
}