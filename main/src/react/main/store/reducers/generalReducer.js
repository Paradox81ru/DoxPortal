import {CHANGE_USER_AUTHENTICATION, CHANGE_MAIN_MENU, ADD_SYSTEM_MESSAGE, REMOVE_SYSTEM_MESSAGE} from "../constants/generalConstants";
import {CHANGE_USER_GROUPS} from "../../../../../../my_admin/src/react/my_admin/store/constans";

const initialStore = {
    userAuthentication: {
        username: null,
        email: null,
        firstName: null,
        lastName: null
    },
    userGroups: [],
    mainMenu:  [
            {
                "label": "Статьи",
                "style": "default",
                "icon": "pencil",
                "url": "/blog/articles",
                "isReal": false,
                "items": null
            },
            {
                "label": "Приложения",
                "style": "default",
                "icon": "file-code",
                "url": "#",
                "isReal": false,
                "items": [
                    {
                        "label": "Скачать",
                        "url": "/software/downloads"
                    },
                    {
                        "label": "Зарегистрировать",
                        "url": "/software/get-register-number"
                    }
                ]
            },
            {
                "label": "Сервисы",
                "style": "default",
                "icon": "wrench",
                "url": "/service",
                "isReal": false,
                "items": null
            },
            {
                "label": "Фото-фэнтези",
                "style": "default",
                "icon": "dragon",
                "url": "/picture",
                "isReal": false,
                "items": null
            }
        ],
    systemMessagesNumber: 0,
    systemMessages: {}

}

/** Общий редюсер */
export default function generalReducer(state = initialStore, action) {
    switch (action.type) {
        case CHANGE_USER_AUTHENTICATION:
            return {
                ...state,
                userAuthentication: action.userAuthentication
            };
        case CHANGE_USER_GROUPS:
            return {
                ...state,
                userGroups: action.userGroups
            }
        case CHANGE_MAIN_MENU:
            return {
                ...state,
                mainMenu: action.mainMenu
            };
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
        default:
            return state;
    }
}