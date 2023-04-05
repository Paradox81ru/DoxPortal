import React, {Component} from "../../../../../../../../node_modules/react";
import {checkListErrors} from "../../../lib/FormUtils";

export default function NonFieldError(props) {
    const errors = checkListErrors(props.errors, "без поля");
    const errorsBlock = errors.map((error, index) => <li key={index}>{error}</li>)
    return (
        <ul className="errorList nonField">
            {errorsBlock}
        </ul>
    );
}