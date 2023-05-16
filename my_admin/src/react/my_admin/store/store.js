import {createStore} from '../../../../../../node_modules/redux';
import reducer from "./reducer";

const initialStore = {
    userAuthentication: {
        username: null,
        email: null,
        firstName: null,
        lastName: null
    },
    loginForm: [],
    breadcrumbList: {
        "/dox-admin": [
            {
                "title": "Главная",
                "path": null
            }
        ],
        "/dox-admin/edit-profile": [
            {
                "title": "Главная",
                "path": "/dox-admin"
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