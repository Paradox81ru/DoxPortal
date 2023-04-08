const TOKEN = "auth_token";

const REMEMBER_LOCAL = "local";
const REMEMBER_SESSION = "session";

/** Сохраняет токен */
function saveToken(whereRemember, token) {
    switch (whereRemember) {
        case REMEMBER_LOCAL:
            if (token != null)
                localStorage.setItem(TOKEN, token);
            break;
        case REMEMBER_SESSION:
            if (token != null)
                sessionStorage.setItem(TOKEN, token);
            break;
    }
}

/** Возвращает токен */
function getToken() {
    let result = ""

    let whereRemember = whereRememberToken();

    switch (whereRemember) {
        case REMEMBER_LOCAL:
            result = localStorage.getItem(TOKEN);
            break;
        case REMEMBER_SESSION:
            result = sessionStorage.getItem(TOKEN);
            break;
    }

    return result;
}

/** Удаляет токен */
function removeToken() {
    let whereRemember = whereRememberToken();

    switch (whereRemember) {
        case REMEMBER_LOCAL:
            localStorage.removeItem(TOKEN);
            break;
        case REMEMBER_SESSION:
            sessionStorage.removeItem(TOKEN);
    }
}

/** Возвращает где сохранен токен */
function whereRememberToken() {
    if (localStorage.hasOwnProperty(TOKEN))
        return REMEMBER_LOCAL;
    if (sessionStorage.hasOwnProperty(TOKEN))
        return REMEMBER_SESSION;
    return null;
}

/** Преобразует переменную "remember my" в тип хранилища токена */
function isRememberMiToWhereRememberToken(isRememberMe) {
    return isRememberMe ? REMEMBER_LOCAL : REMEMBER_SESSION
}

export {saveToken, getToken, whereRememberToken, isRememberMiToWhereRememberToken, removeToken,
    REMEMBER_LOCAL, REMEMBER_SESSION};