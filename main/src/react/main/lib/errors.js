
/** Ошибка неавторизованного пользователя */
class UnauthorizedError extends Error {
    constructor(message, code = 401) {
        super(message);
        this.code = code;
        this.name = "UnauthorizedError";
    }
}

/** Ошибка недостаточно прав */
class ForbiddenError extends Error {
    constructor(message, code = 403) {
        super(message);
        this.code = code;
        this.name = "ForbiddenError";
    }
}

/** Ошибка неверной проверки каптчи */
class CaptchaValidateError extends Error {
    constructor() {
        super();
        this.message = "Неверный код!";
        this.name = "CaptchaValidateError";
    }
}

/** Ошибка проверки правильности ввода полей */
class FieldValidateError extends Error {
    constructor(validateResult) {
        super();
        // Так как это ошибка, то устанавливаю список ошибок в объект с ключoм error.
        this.validateResult = validateResult;
        this.name = "FieldValidateError";
    }
}

/** Ошибка истекшего токена доступа */
class TokenAccessExpired extends Error {
    constructor(message) {
        super(message);
        this.name = "TokenAccessExpired";
    }
}

/** Неизвестная ошибка ответа */
class UnknownResponseError extends Error {
    constructor(message, code) {
        super(message);
        this.code = code;
        this.name = "UnknownRequestError";
    }
}

export {UnauthorizedError, ForbiddenError, CaptchaValidateError, FieldValidateError, TokenAccessExpired, UnknownResponseError};