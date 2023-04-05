export default function reducer(state, action) {
    switch (action.type) {
        case "CHANGE_TEMPERATURE":
            return {
                ...state,
                scale: action.scale,
                temperature: action.temperature
            }
        case "CHANGE_SHOW_RESULT_BOILING":
            return {
                ...state,
                isShowResultBoiling: action.isShow
            }

        default:
            return state
    }
}