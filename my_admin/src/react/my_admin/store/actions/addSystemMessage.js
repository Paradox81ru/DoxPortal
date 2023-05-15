import {ADD_SYSTEM_MESSAGE} from "../constans";

/**
 * Добавляет системное сообщение
 * @param type тип сообщения (primary, secondary, success, danger, warning, info, light, dark)
 * @param message текст сообщения
 */
export default function addSystemMessage(type, message) {
    return {
        type: ADD_SYSTEM_MESSAGE,
        message: {type: type, message: message}
    }
}