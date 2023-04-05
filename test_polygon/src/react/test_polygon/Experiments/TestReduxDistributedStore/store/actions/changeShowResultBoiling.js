import { CHANGE_SHOW_RESULT_BOILING } from "./actions";

export default function changeShowResultBoiling(value) {
    return {
        type: CHANGE_SHOW_RESULT_BOILING,
        isShow: value
    }
}