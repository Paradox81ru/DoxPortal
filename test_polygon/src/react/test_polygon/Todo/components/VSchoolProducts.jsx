// noinspection NpmUsedModulesInstalled
import React, {Component} from 'react';
import Product from "./Product";
import productsData from "./vschoolProducts.json"

function VSchoolProducts() {
    const productComponents = productsData.map(item => <Product key={item.id} product={item} />);
    return (
        <div>
            {productComponents}
        </div>
    )
}

export default VSchoolProducts