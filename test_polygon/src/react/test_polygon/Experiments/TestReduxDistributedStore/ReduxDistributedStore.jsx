import React from "../../../../../../../../../node_modules/react";
import {Provider} from "../../../../../../../../../node_modules/react-redux"
import store from "./store/store"
import Calculator_W from "./containers/Calculator";

export default function ReduxDistributedStore() {
    return (
        <Provider store={store}>
            <div className="TestDistributedRedux">
                <h2>Тестирование React + Redux с распределенным хранилищем</h2>
                <Calculator_W/>
            </div>
        </Provider>
    )
}