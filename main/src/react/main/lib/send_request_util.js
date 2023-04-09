import {getToken, saveToken, whereRememberToken} from "./auth_token_util";
import {addSystemMessage} from "../store/actions/generalActions";
import store from "../store/store";
import {UnauthorizedError, ForbiddenError, TokenAccessExpired, UnknownResponseError} from "./errors";

/**
 * Возвращает заголовок для fetch запроса
 * @param extHeaders дополнительные заголовки
 * @returns {Headers}
 */
function getFetchHeaders(extHeaders = {}) {
    let headers = new Headers();
    headers.append("Content-Type", "application/json");
    // Ищу в хранилище токены,
    let token = getToken();
    // и если токен доступа был найден,
    if (token.length !== 0)
        // то добавляю его в заголовок авторизации.
        headers.append("Authorization", "Token " + token);
    // Если были переданы дополнительные заголовки,
    if (extHeaders != null) {
        // то добавляю и их.
        Object.keys(extHeaders).map(key => headers.append(key, extHeaders[key]));
    }
    return headers;
}

/**
 * Производит отправку запроса по указанному URL
 * @param url
 * @param method
 * @param data
 * @returns {Promise<unknown>}
 */
function sendRequest(url, method, data=undefined) {
    return new Promise((resolve, reject) => {
        // Отправляю прокси fetch запрос,
        proxyFetch(url, method, data)
            // запрос, то возвращается корректный ответ.
            .then(response => {
                    resolve(response);
                },
                error => {
                    // А если нет, то проверяю какая ошибка помешала запросу.
                    switch (error.name) {
                        case "UnauthorizedError":
                            // Если это ошибка авторизации или неизвестная ошибка,
                            // то её надо обработать предоставленным reject-ом.
                            reject(error);
                            break;
                        case "TokenAccessExpired":
                            console.log(error.message);
                            // addSystemMessage("danger", error.message)
                             reject(error);
                            break;
                        case "UnknownResponseError":
                             // Если это неизвестная ошибка,
                            let message = `Неизвестная ошибка код ${error.code}; ${error.message}`;
                            // то её надо отобразить,
                            console.log(message);
                            _addSystemMessage("danger", message);
                            // а затем обработать предоставленным reject-ом.
                            reject(error);
                        break;
                    }
                });
    })
}

/**
 * Отправляет прокси fetch запрос по указанному URL
 * @param url
 * @param method
 * @param data
 * @returns {Promise<Response>}
 */
function proxyFetch(url, method, data=undefined) {
    let headers = getFetchHeaders();
    let options = {headers: headers};
    options["method"] = method;
    if (data !== undefined) {
        options["body"] = JSON.stringify(data);
    }
    return fetch(url, options)
        .then(response => {
            if (response.status === 200) {
                // Если ответ корректный, то просто преобразую его в JSON и возвращаю дальше.
                return response.json();
            } else if (response.status === 204) {
                // Если ответ 204 - то это положительный ответ без возвращения данных.
                // Поэтому и вернём null
                return null;
            } else if (response.status === 401) {
                // Если вернулась ошибка авторизации, то проверяю где в данный момент сохранены токены.
                if (whereRememberToken() == null)
                    // Если нигде, значит пользователь авторизован и не был, возвращаю ошибку авторизации.
                    throw new UnauthorizedError("Ошибка авторизации.");
                else {
                    // Иначе пользователь был авторизован, и надо вернуть ошибку,
                    // которая приведет к запросу на получение нового токена доступа.
                    throw new TokenAccessExpired("Срок действия токена доступа истёк.");
                }
            } else
                // А если это была не ошибка авторизации, значит что-то пошло не так, просто верну текущую ошибку.
                throw new UnknownResponseError(response.statusText, response.status);
        });
}

// /** Запрос нового токена доступа */
// function requestNewTokenAccess() {
//     return new Promise((resolve, reject) => {
//         fetch("/api/auth/token", getNewTokenOptions())
//             .then(response => {
//                 if (response.status === 200)
//                     return response.json();
//                 else if (response.status === 401) {
//                     throw new UnauthorizedError("Ошибка авторизации");
//                 }
//             })
//             .then(data => {
//                 // В ответ получаю новый токен доступа.
//                 let whereRemember = whereRememberToken();
//                 // Если место хранения токенов не найдено, значит пользователь авторизован и не был.
//                 if (whereRemember == null)
//                     throw new UnauthorizedError("Ошибка авторизации");
//                 else {
//                     // Сохраняю новый токен в хранилище.
//                     saveToken(whereRemember, data.token);
//                     console.log("Новый токен доступа сохранён.")
//                     // Возвращаю, истекает ли токен обновления.
//                     resolve(data.isRefreshTokenExpireSoon);
//                 }
//             }).catch(reject);
//     });
// }
//
// /** Запрос нового токена обновления */
// function requestNewRefreshToken() {
//     return new Promise((resolve, reject) => {
//         fetch("/api/auth/refresh-token", getNewTokenOptions())
//             .then(response => {
//                 if (response.status === 200)
//                     return response.json();
//                 else if (response.status === 401) {
//                     throw new UnauthorizedError("Ошибка авторизации");
//                 }
//             })
//             .then(data => {
//                 // В ответ получаю новый токен обновления.
//                 let whereRemember = whereRememberToken();
//                 // Если место хранения токенов не найдено, значит пользователь авторизован не был.
//                 if (whereRemember == null)
//                     throw new UnauthorizedError("Ошибка авторизации");
//                 else {
//                     // Сохраняю новый токен обновления в хранилище.
//                     saveToken(whereRemember, null, data.token);
//                     console.log("Новый токен обновления сохранён.");
//                     resolve();
//                 }
//             }).catch(reject);
//     });
// }

// /** Возвращает опции для запроса новых токенов */
// function getNewTokenOptions() {
//     let headers = getFetchHeaders();
//     let options = {headers: headers};
//     options["method"] = "POST";
//     // Ищу в хранилище токены,
//     let tokens = getToken();
//     // и передаю токен обновления.
//     options["body"] = JSON.stringify({refreshToken: tokens.refreshToken});
//     return options;
// }

/**
 * Ответ на запрос начальных данных
 * @param urlBegin url адрес получения начальных данных без последней части означающего режим возвращение ошибок.
 * @param isAdmin если это начальные данные администратора
 * @returns {(function(*): (*|undefined))|*}
 */
function resolveBeginData(urlBegin, isAdmin=false) {
    // url ссылка на получение начальных данных с нулём, означающем запрос без возвращения ошибок.
    const url = urlBegin + "/0";
    return (response, reject) => {
        if (response.status === 200) {
            // Если ответ корректный, то просто преобразую его в JSON и возвращаю дальше.
            return response.json();
        } else if (response.status === 401) {
            // Если вернулась ошибка авторизации, то запрашиваю новый токен доступа,
            // return requestNewTokenAccess()
            //     .then(
            //         (result) => {
            //             // Если в результате обновления токена доступа вернулся true,
            //             if (result === true)
            //                 // запрашиваю ещё и новый токен обновления,
            //                 // после чего снова делаю повторный запрос на начальные данные, но уже без возвращения ошибок,
            //                 // причем неважно закончилось ли обновление токена обновления удачно или с ошибкой.
            //                 return  requestNewRefreshToken()
            //                     .then(() => repeatFetch(url))
            //                     .catch(() => repeatFetch(url));
            //             else
            //                 // Иначе просто делаю заново запрос на начальные данные, но уже без возвращения ошибок.
            //                 return repeatFetch(url);
            //         },
            //         (error) => {
            //             // Если при обновлении токена произошла ошибка,
            //             console.log("Ошибка получения нового токена доступа " + error.message);
            //             if (isAdmin)
            //                 throw new UnauthorizedError("Для просмотра страницы требуется авторизация");
            //             // то всё равно надо сделать запрос для получения начальных данных.
            //             return repeatFetch(url);
            //         })
        } else if (response.status === 403) {
            throw new ForbiddenError("У Вас недостаточно прав для просмотра страницы")
        }
    }

    /** Повторный запрос */
    function repeatFetch(url) {
        let options = {headers: getFetchHeaders()};
        return fetch(url, options)
            .then(response => response.json());
    }
}

/**
 * Добавляет системное сообщение
 * @param type
 * @param message
 */
function _addSystemMessage(type, message) {
    store.dispatch(addSystemMessage(type, message));
}

export {getFetchHeaders, sendRequest, resolveBeginData};