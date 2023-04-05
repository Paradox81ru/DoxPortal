import React, {Component} from "../../../../../../../../../../node_modules/react";
import {Link} from "../../../../../../../../../../node_modules/react-router-dom"

/** Формирует верхнее меню заголовка */
export default class HeaderMenu extends Component{
    /** Возвращает данные для формирования меню заголовка */
    getMenuData() {
        return [
            {
                "itemName": "Домой",
                "faName": "house",
                "link": "/",
                "cls": null
            },
            {
                "itemName": "О сайте",
                "faName": "circle-info",
                "link": "/about",
                "cls": null
            },
            {
                "itemName": "Обратная связь",
                "faName": "envelope",
                "link": "/contact",
                "cls": null
            },
            {
                "itemName": "Права на сайт",
                "faName": "copyright",
                "link": "/copyright",
                "cls": null
            },
            {
                "itemName": "Поиск",
                "faName": "magnifying-glass",
                "link": "/main",
                "cls": "hidden-icon-search"
            }
        ]
    }

    /** Возвращает пункт меню заголовка */
    getMenuItem(item, index) {
        const cls = "fa-solid fa-2x fa-" + item.faName;
        return(
            <li key={index} className={item.cls}>
                <Link to={item.link}>
                    <i className={cls} title={item.itemName}></i>
                    <span className="d-none d-lg-block">{item.itemName}</span>
                </Link>
            </li>
        )
    }

    render() {
        // Формирует список пунктов меню заголовка
        const menu = this.getMenuData().map((item, index) => this.getMenuItem(item, index));
        return(
            <ul className="header-menu">
                {menu}
            </ul>
        )
    }
}