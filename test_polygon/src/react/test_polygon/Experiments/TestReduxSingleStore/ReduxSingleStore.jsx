import React from "../../../../../../../../../node_modules/react";
import {Provider} from "../../../../../../../../../node_modules/react-redux"
import store from "./store/store"
import Calculator_W from "./containers/Calculator";

export default function ReduxSingleStore() {
    return (
        <Provider store={store}>
            <div className="TestSingleRedux">
                <h2>Тестирование React + Redux с единым хранилищем</h2>
                <Calculator_W/>
            </div>
        </Provider>
    )
}
