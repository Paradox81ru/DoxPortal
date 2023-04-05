import { CHANGE_SHOW_RESULT_BOILING } from "../actions/actions";

export default function verdictReducer(state=true, action) {
    switch (action.type) {
        case CHANGE_SHOW_RESULT_BOILING:
            return action.isShow;
        default:
            return state;
    }
}