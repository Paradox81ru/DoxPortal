// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import Header from "../Header";
import ContactCard from "./ContactCard";
import contactData from "./contactData.json"
import '../../styles/Task2.scss';

function Task2() {
    const contactsComponent = contactData.map(contact => <ContactCard key={contact.id} contact={contact} />)
    return (
        <div className="task task2">
            <Header title="Тестовое задание 2"/>
            <div className="contacts">
                {contactsComponent}
            </div>
        </div>
    )
}

export default Task2