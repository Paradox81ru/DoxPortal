import {createStore} from '../../../../../../../../../../node_modules/redux'
import rootReducer from "./reducers/rootReducer";

const store = createStore(rootReducer)
export default store