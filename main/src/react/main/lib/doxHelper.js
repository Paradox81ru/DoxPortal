import {getToken} from "./auth_token_util";

// /**
//  * Возвращает заголовок для fetch запроса
//  * @param extHeaders дополнительные заголовки
//  * @returns {Headers}
//  */
// function getFetchHeaders(extHeaders= {}) {
//     let headers = new Headers();
//     headers.append("Content-Type", "application/json");
//     // Ищу в хранилище токены,
//     let tokens = getTokens();
//     // и если токен доступа был найден,
//     if (tokens.accessToken.length !== 0)
//         // то добавляю его в заголовок авторизации.
//         headers.append("Authorization", "Bearer " + tokens.accessToken);
//     // Если были переданы дополнительные заголовки,
//     if (extHeaders != null) {
//         // то добавляю и их.
//         Object.keys(extHeaders).map(key => headers.append(key, extHeaders[key]));
//     }
//     return headers;
// }

/**
 * Формирует и возвращает строку параметра запроса
 * @param data {Object}
 * @returns {string}
 */
function getSearchParams(data) {
    let searchParams = new URLSearchParams();
    for (let key in data)
        searchParams.append(key, data[key]);

    return searchParams.toString();
}

/**
 * Проверяет переменную на строку
 * @param str переменная
 * @returns {boolean}
 */
function isString(str) {
    return (typeof str === 'string' || str instanceof String);
}

export {getSearchParams, isString};