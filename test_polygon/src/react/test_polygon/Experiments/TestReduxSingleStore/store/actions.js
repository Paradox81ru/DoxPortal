function changeTemperature(scale, value) {
    return {
        type: "CHANGE_TEMPERATURE",
        scale: scale,
        temperature: value
    }
}

function changeShowResultBoiling(value) {
    return {
        type: "CHANGE_SHOW_RESULT_BOILING",
        isShow: value
    }
}

export {changeTemperature, changeShowResultBoiling}