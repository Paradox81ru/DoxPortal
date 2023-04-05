import {CHANGE_USER_AUTHENTICATION, RESET_USER_AUTHENTICATION, CHANGE_MAIN_MENU, RESET_MAIN_MENU,
    ADD_SYSTEM_MESSAGE, REMOVE_SYSTEM_MESSAGE} from "../constants/generalConstants";

/** Изменяет данные авторизованного пользователя */
function changeUserAuthentication(data) {
    return {
        type: CHANGE_USER_AUTHENTICATION,
        userAuthentication: data.userAuthentication
    }
}

/** Сбрасывает данные авторизованного пользователя */
function resetUserAuthentication() {
    return {
        type: RESET_USER_AUTHENTICATION,
        userAuthentication: {
            username: null,
            email: null,
            firstName: null,
            lastName: null
        }
    }
}

/** Изменяет главное меню расположенное в левом сайдбаре */
function changeMainMenu(data) {
    return {
        type: CHANGE_MAIN_MENU,
        mainMenu: data.mainMenu
    }
}

/** Сбрасывает главное меню расположенное в левом сайдбаре до стандартного меню гостя */
function resetMainMenu() {
    return {
        type: RESET_MAIN_MENU,
        mainMenu: [
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
        ]
    }
}

/**
 * Добавляет системное сообщение
 * @param type тип сообщения (primary, secondary, success, danger, warning, info, light, dark)
 * @param message текст сообщения
 */
function addSystemMessage(type, message) {
    return {
        type: ADD_SYSTEM_MESSAGE,
        message: {type: type, message: message}
    }
}

/**
 * Удаляет системное сообщение
 * @param id идентификатор системного сообщения
 */
function removeSystemMessage(id) {
    return {
        type: REMOVE_SYSTEM_MESSAGE,
        id: id
    }
}

export {changeUserAuthentication, resetUserAuthentication, changeMainMenu, resetMainMenu,
    addSystemMessage, removeSystemMessage};