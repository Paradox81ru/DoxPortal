import React from "../../../../../../../../../node_modules/react";

function MainContent() {
    const date = new Date();
    const hours = date.getHours();
    const styles = {
        color: "#FF8C00",
        backgroundColor: "#FF2D00",
        fontSize: "24px"
    };
    let timeOfDay;

    if (hours < 12)
        timeOfDay = "утро";
    else if (hours >= 12 && hours < 17)
        timeOfDay = "обед";
    else
        timeOfDay = "вечер";

    return (
        <h1 style={styles}>Добрый {timeOfDay}!</h1>
    )
}

export default MainContent;