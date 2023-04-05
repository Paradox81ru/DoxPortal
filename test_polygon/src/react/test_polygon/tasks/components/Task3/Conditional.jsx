// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';

function Conditional(props) {
    return (
        <div>
            <p>Что-то еще.,,.</p>
            {props.isLoading ? <h2>Загрузка...</h2> : <h2>Несколько интересных вещей об условном рендеринге</h2>}
        </div>
    )
}

export default Conditional