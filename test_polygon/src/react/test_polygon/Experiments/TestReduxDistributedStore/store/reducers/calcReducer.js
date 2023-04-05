import { CHANGE_TEMPERATURE } from "../actions/actions";

const initialStore = {
    temperature: '0',
    scale: 'c',
}

export default function calcReducer(state = initialStore , action) {
    switch (action.type) {
        case CHANGE_TEMPERATURE:
            return {
                scale: action.scale,
                temperature: action.temperature
            }
        default:
            return state;
    }
}