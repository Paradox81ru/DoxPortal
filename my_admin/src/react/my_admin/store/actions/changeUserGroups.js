import {CHANGE_USER_GROUPS} from "../constans";

/** Изменяет группу, в которую входит пользователь */
function changeUserGroups(data) {
    return {
        type: CHANGE_USER_GROUPS,
        userGroups: data.userGroups
    }
}