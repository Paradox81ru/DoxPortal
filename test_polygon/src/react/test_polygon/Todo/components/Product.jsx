// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';

function Product(props) {
    return (
        <div>
            <h2>{props.product.name}</h2>
            <p>{props.product.price.toLocaleString("ru-Ru", { style: "currency", currency: "RUB" })} - {props.product.description}</p>
        </div>
    )
}

export default Product