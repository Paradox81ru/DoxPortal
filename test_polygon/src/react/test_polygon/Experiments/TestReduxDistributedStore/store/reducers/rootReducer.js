import { combineReducers } from "../../../../../../../../../../../node_modules/redux";
import calcReducer from "./calcReducer";
import verdictReducer from "./verdictReducer";

const rootReducer = combineReducers({
    calc: calcReducer,
    isShowResultBoiling: verdictReducer
})
export default rootReducer