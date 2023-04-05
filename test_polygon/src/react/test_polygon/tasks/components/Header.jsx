// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import "../styles/Header.css"

function Header({title}) {
    return (
        <header className="App-header">
            <h2 className="App-title">{title}</h2>
        </header>
    )
}

export default Header