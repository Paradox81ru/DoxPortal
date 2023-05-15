import {REMOVE_SYSTEM_MESSAGE} from "../constans";

/**
 * Удаляет системное сообщение
 * @param id идентификатор системного сообщения
 */
export default function removeSystemMessage(id) {
    console.log("Remove message " + id);
    return {
        type: REMOVE_SYSTEM_MESSAGE,
        id: id
    }
}