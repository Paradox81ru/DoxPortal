import React from "../../../../../../../../node_modules/react";
import {Link} from "../../../../../../../../node_modules/react-router-dom"

export default function LogoImage() {
    return(
        <div className="logo-image">
            <Link to="/"><img src="/static/common/images/site/logo-head.jpg" alt="Парадокс-портал" height="200" /></Link>
        </div>
    )
}