import React, {Component} from "../../../../../../../../node_modules/react";

export default class Captcha extends Component{
    constructor() {
        super();
        this.state = {
            captchaSrc: "captcha1.png"
        }
    }

    /** Обрабатывает событие обновления каптчи */
    handleReloadCaptcha = (e) => {
        e.preventDefault();
        this.reloadCaptcha();
    }

    /** Обновляет каптчу */
    reloadCaptcha() {
        let rnd = Math.floor(Math.random()*9999.9999);
        this.setState({
            captchaSrc: `captcha${rnd}.png`
        })
    }

    render() {
        return(
            <table className="tbl_captcha">
                <tbody>
                <tr>
                    <td>
                        <img id="captcha" src={'main/' + this.state.captchaSrc} alt="captcha" />
                    </td>
                </tr>
                <tr>
                    <td>
                        <a onClick={this.handleReloadCaptcha} href="#">Обновить капчу</a>
                    </td>
                </tr>
                </tbody>
            </table>
        )
    }
}