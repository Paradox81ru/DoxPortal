import {CHANGE_USER_AUTHENTICATION} from "../constans";

/** Изменяет данные авторизованного пользователя */
export default function changeUserAuthentication(user) {
    return {
        type: CHANGE_USER_AUTHENTICATION,
        userAuthentication: user
    }
}