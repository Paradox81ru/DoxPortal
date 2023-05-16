import {SET_BREADCRUMB, CHANGE_USER_AUTHENTICATION, ADD_SYSTEM_MESSAGE, REMOVE_SYSTEM_MESSAGE, SET_LOGIN_FORM} from "./constans";

export default function reducer(state, action) {
    switch (action.type) {
        case SET_BREADCRUMB:
            return {
                ...state,
                breadcrumbList: action.breadcrumbList
            }
        case CHANGE_USER_AUTHENTICATION:
            return {
                ...state,
                userAuthentication: action.userAuthentication
            }
        case ADD_SYSTEM_MESSAGE:
            return {
                ...state,
                systemMessages: {
                    ...state.systemMessages,
                    [state.systemMessagesNumber + 1]: action.message
                },
                systemMessagesNumber: state.systemMessagesNumber + 1
            };
        case REMOVE_SYSTEM_MESSAGE:
            const {[action.id]: _, ...newSystemMessages} = state.systemMessages;
            return {
                ...state,
                systemMessages: newSystemMessages
            }
        case SET_LOGIN_FORM:
            return {
                ...state,
                loginForm: action.form
            }
        default:
            return state
    }
}