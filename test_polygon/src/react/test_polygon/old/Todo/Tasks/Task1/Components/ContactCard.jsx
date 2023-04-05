import React from "../../../../../../../../../../../node_modules/react"

function ContactCard(props) {
    let imgUrl = props.hasOwnProperty("contact") ? props.contact.imgUrl : props.imgUrl;
    let name = props.hasOwnProperty("contact") ? props.contact.name : props.name;
    let phone = props.hasOwnProperty("contact") ? props.contact.phone : props.phone;
    let email = props.hasOwnProperty("contact") ? props.contact.email : props.email;

    return (
        <div className="contact-card">
            <img align="center" src={imgUrl}/>
            <h3><font color="#3AC1EF">{name}</font></h3>
            <p>Phone: {phone}</p>
            <p>Email: {email}</p>
        </div>
    )
}

export default ContactCard;