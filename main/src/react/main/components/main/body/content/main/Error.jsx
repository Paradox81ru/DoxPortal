import React, {Component} from "../../../../../../../../../../node_modules/react";

export default function Error(props) {
    let dateNow = new Date();
    return(
        <div id="errorContent">
            <h1>Ошибка {props.code}.</h1>
            <p style={{fontSize: "1.4em"}}>Дата:
                <span>{`${dateNow.getDate()}.${dateNow.getMonth() + 1}.${dateNow.getFullYear()}`}</span>г. {props.message}
            </p>
        </div>
    )
}