// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';

class Hello extends Component {
    render() {
        const {firstName, lastName} = this.props;
        const data = new Date();
        const hours = data.getHours();
        let timeOfDay;
        const styles = {
            fontSize: "1.1em"
        }

        if (hours < 12) {
            timeOfDay = "Доброе утро";
            styles.color = "#ffe600";
        } else if (hours >= 12 && hours < 17) {
            timeOfDay = "Добрый день";
            styles.color = "#a50000"
        } else if (hours >= 17 && hours < 23) {
            timeOfDay = "Добрый вечер";
            styles.color = "#234c86"
        } else {
            timeOfDay = "Доброй ночи";
            styles.color = "#2E0927"
        }

        return (
            <h5 style={styles}>{timeOfDay}! Я {`${firstName} ${lastName}.`}</h5>
        )
    }
}

export default Hello