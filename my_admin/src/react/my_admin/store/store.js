import {createStore} from '../../../../../../../../node_modules/redux';
import reducer from "./reducer";

const initialStore = {
    userAuthentication: {
        username: null,
        email: null,
        firstName: null,
        lastName: null
    },
    breadcrumbList: {
        "/my-admin": [
            {
                "title": "Главная",
                "path": null
            }
        ],
        "/my-admin/edit-profile": [
            {
                "title": "Главная",
                "path": "/my-admin"
            },
            {
                "title": "Редактирование профилей",
                "path": null
            }
        ]
    },
    systemMessagesNumber: 0,
    systemMessages: {}
}

const store = createStore(reducer, initialStore);

export default store;