/**
 * Обрабатывает изменения ввода в поля
 * @param {Object} context ссылка на компонент React
 * @returns {(function(*): void)|*}
 */
function handleFieldValueChange(context) {
    return (event) => {
        const {name, value, type, checked} = event.target;
        const val = type === "checkbox" ? checked : value;
        context.setState(prevState => ({
            ...prevState,
            fields: {
                ...prevState.fields,
                [name]: val
            }
        }));
    }
}

/**
 * Обрабатывает изменения ввода в поля без сложных полей
 * @param {Object} context ссылка на компонент React
 * @returns {(function(*): void)|*}
 */
function handleSimpleFieldValueChange(context) {
    return (event) => {
        const {name, value} = event.target;
        context.setState(prevState => ({
            ...prevState,
            fields: {
                ...prevState.fields,
                [name]: value
            }
        }));
    }
}

/**
 * Очищает значения всех полей
 * @param {Object} context ссылка на компонент React
 */
function clearAllFieldsValue(context) {
    context.setState(prevState => {
        let clearFields = {};
        Object.keys(prevState.fields).forEach(key => clearFields[key] = "");
        return {
            ...prevState,
            fields: clearFields
        }
    });
}

/**
 * Устанавливает ошибку указанного поля
 * @param {string} fieldName наименование поля
 * @param {string|Array} errors ошибки
 * @param {Object} context ссылка на компонент React
 */
function setFieldError(fieldName, errors, context) {
    const _errors = checkListErrors(errors, fieldName);
    context.setState(prevState => ({
            ...prevState,
            errors: {
                ...prevState.errors,
                [fieldName]: _errors
            }
        }
    ));
}

/**
 * Устанавливает ошибки нескольких полей
 * @param {Object} listErrors ассоциативный массив, где ключи - наименование поле, а значение - список ошибок.
 * @param {Object} context ссылка на компонент React
 */
function setFieldsError(listErrors, context) {
    Object.keys(listErrors).forEach(key => setFieldError(key, listErrors[key], context));
}

/**
 * Устанавливает ошибку вне поля
 * @param {string|Array} errors ошибка (строка или список), которая устанавливается
 * @param {Object} context ссылка на компонент React
 */
function setNonFieldError(errors, context) {
    setFieldError("non_field_errors", errors, context);
}

/**
 * Удаляет ошибку
 * @param {string} fieldName наименование поля ошибка которой сбрасывается
 * @param {Object} context ссылка на компонент React
 */
function removeFieldError(fieldName, context) {
    context.setState(prevState => ({
            ...prevState,
            errors: {
                ...prevState.errors,
                [fieldName]: []
            }
        })
    );
}

/**
 * Удаляет ошибку вне поля
 * @param {Object} context ссылка на компонент React
 */
function removeNonFieldError(context) {
    removeFieldError("non_field_errors", context);
}

/**
 * Удаляет все ошибки полей
 * @param {Object} context ссылка на компонент React
 */
function removeAllFieldsErrors(context) {
    context.setState(prevState => {
        let clearErrors = {};
        Object.keys(prevState.errors).forEach(key => clearErrors[key] = []);
        return {
            ...prevState,
            errors: clearErrors
        }
    });
}

/**
 * Проверяет список ошибок одного поля
 * @param {string|Array} errors
 * @param {string} fieldName
 * @returns {string[]|*}
 */
function checkListErrors(errors, fieldName) {
    if (typeof errors === 'string' || errors instanceof String)
        return [errors];

    if (!Array.isArray(errors))
        throw new Error(`Ошибка поле ${fieldName}: ошибки должны быть представлены в виде строки или списка строк.`);

    return errors;
}

export {
    handleFieldValueChange, handleSimpleFieldValueChange, clearAllFieldsValue, setFieldError, setFieldsError, setNonFieldError,
    removeFieldError, removeAllFieldsErrors, removeNonFieldError, checkListErrors
}