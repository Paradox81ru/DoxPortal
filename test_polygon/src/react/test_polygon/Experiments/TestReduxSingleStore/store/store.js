import {createStore} from '../../../../../../../../../../node_modules/redux'
// import React from "../../../../../../../../../../../../pyprojects/paradox-portal/pythonProject/node_modules/redux"
import reducer from "./reducer";

const initialState = {
    temperature: '0',
    scale: 'c',
    isShowResultBoiling: true
}
// Вообще isShowResultBoiling здесь лишнее, так как булевы значения не требуют полезной нагрузки,
// и такое состояние лучше реализовывать в виде локального состояния компонента.

const store = createStore(reducer, initialState)

export default store