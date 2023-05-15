import React, {Component} from "../../../../../../../../../node_modules/react";
import {Link} from "../../../../../../../../../node_modules/react-router-dom";
import Nav from '../../../../../../../../../node_modules/react-bootstrap/Nav';
import NavDropdown from '../../../../../../../../../node_modules/react-bootstrap/NavDropdown';
const DIVIDER = "divider";


export default class NavigationNav extends Component {
    getNavItemDropdown(item, key) {
        const links = item[1].map((_item, index) => _item[0] === DIVIDER
            ? <NavDropdown.Divider key={index}/>
            : <NavDropdown.Item key={index} as={Link} to={_item[1]}>{_item[0]}</NavDropdown.Item>)

        return(
            <NavDropdown key={key} title={item[0]} >
                {links}
            </NavDropdown>
        )
    }

    getLink(item, key) {
        return item.length === 3 && item[2]
            ? <Nav.Link key={key} href={item[1]}>{item[0]}</Nav.Link>
            : <Nav.Link key={key} as={Link} to={item[1]}>{item[0]}</Nav.Link>
    }

    render() {
        const menu = this.props.nav.map((item, index) => Array.isArray(item[1])
            ? this.getNavItemDropdown(item, index)
            : this.getLink(item, index) )
        return(
        <Nav className={this.props.cls}>
            {menu}
        </Nav>
        )
    }
}