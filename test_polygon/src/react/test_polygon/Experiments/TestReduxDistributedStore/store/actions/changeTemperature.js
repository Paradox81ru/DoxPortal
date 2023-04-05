import { CHANGE_TEMPERATURE } from "./actions";

export default function changeTemperature(scale, value) {
    return {
        type: CHANGE_TEMPERATURE,
        scale: scale,
        temperature: value
    }
}