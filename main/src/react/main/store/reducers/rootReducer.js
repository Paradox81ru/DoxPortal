import { combineReducers } from "../../../../../../../node_modules/redux";
import cachePageReducer from "./cachePagesReducer";
import generalReducer from "./generalReducer";

const rootReducer = combineReducers({
    cachePage: cachePageReducer,
    general: generalReducer
});

export default rootReducer