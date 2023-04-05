import React from "../../../../../../../../../node_modules/react";
import HeaderParadox_W from "./HeaderParadox";
import NavHeader from "./nav_header/NavHeader";

export default function LogoData() {
    return(
            <div className="logo-data flex-fill d-flex flex-column">
                <HeaderParadox_W />
                <NavHeader />
            </div>
    )
}