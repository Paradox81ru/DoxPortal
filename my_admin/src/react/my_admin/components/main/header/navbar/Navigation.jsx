import React, {Component} from "../../../../../../../../../node_modules/react";
import Nav from '../../../../../../../../../node_modules/react-bootstrap/Nav';
import Navbar from '../../../../../../../../../node_modules/react-bootstrap/Navbar';

import NavigationNav from "./NavigationNav";

const DIVIDER = "divider";

export default function Navigation() {
        const nav1 = [
            ["Управление сайтом", [
                ["Изменение профиля пользователей", "/dox-admin/edit-profile"],
                ["Управление временными пользователями", "/dox-admin/manage-temp-user"],
                [DIVIDER],
                ["Парадоксы", "/dox-admin/paradox-processing"],
                ["Тэги", "/dox-admin/tags-processing"],
                [DIVIDER],
                ["One more separated link", "#"]
            ]],
            ["Link", "#"],
            ["Тестовый полигон", [
                ["Тест React", "/test-polygon/test-react"],
                ["DataTable 1", "/test-polygon/test-data-table-1"],
                ["DataTable 2", "/test-polygon/test-data-table-2"]
            ]]
        ]

        const nav2 = [
            ["Открыть сайт", "/", true],
            ["Dropdown", [
                ["Action", "#"],
                ["Another action", "#"],
                ["Something else here", "#"],
                [DIVIDER],
                ["Separated link", "#"]
            ]]
        ]

    return (
        <Navbar.Collapse className="justify-content-between" id="navbarSupportedContent">
            <NavigationNav nav={nav1} cls="justify-content-start flex-grow-1 pe-3"/>
                <NavigationNav nav={nav2} cls="justify-content-end flex-grow-1 pe-3"/>
        </Navbar.Collapse>
    )
}