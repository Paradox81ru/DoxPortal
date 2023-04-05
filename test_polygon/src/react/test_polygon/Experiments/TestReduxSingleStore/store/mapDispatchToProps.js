import {bindActionCreators} from "../../../../../../../../../../node_modules/redux"
import {changeTemperature, changeShowResultBoiling} from "./actions"

export default function mapDispatchToProps(component) {
    switch (component) {
        case "Calculator":
            return function (dispatch) {
                return {
                    // Если не использовать bindActionCreators то в компоненте действие onTemperatureChange
                    // придется самому запускать через dispatch хранилища.
                    // onTemperatureChange: changeTemperature
                    onTemperatureChange: bindActionCreators(changeTemperature, dispatch)
                }
            }
        case "BoilingVerdict":
            return function (dispatch) {
                return {
                    onChangeShowResultBoiling: bindActionCreators(changeShowResultBoiling, dispatch)
                }
            }

        default: return undefined;
    }
}