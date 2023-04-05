// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';

class ContactCard extends Component {
    constructor() {
        super();
        this.state = {
            count: 0
        }
    }

    handleClick = () => {
        this.setState(prevState => {
            return {
                count: prevState.count + 1
            }
        });
    }

    render() {
        return (
            <div className="contact-card">
                <img onMouseOver={() => console.log("Hovered!")} align="center" src={this.props.contact.imgUrl}/>
                <h3>{this.props.contact.name}</h3>
                <p>Phone: {this.props.contact.phone}</p>
                <p>Email: {this.props.contact.email}</p>
                <button onClick={this.handleClick}>Нажми меня</button>
                <p className="counter">{this.state.count}</p>
            </div>
        )
    }
}

export default ContactCard