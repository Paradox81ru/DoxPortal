import React, {Component} from "../../../../../../../../node_modules/react";
import LogoImage from "./LogoImage";
import LogoData from "./logo_data/LogoData";

/** Шапка-заголовок сайта */
export default function Header() {
    return(
            <header className="container d-flex p-1">
                <LogoImage />
                <LogoData />
            </header>
    )
}