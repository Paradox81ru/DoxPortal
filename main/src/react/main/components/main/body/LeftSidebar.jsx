import React, {Component} from "../../../../../../../../node_modules/react";
import {connect} from "../../../../../../../../node_modules/react-redux";
import {Link} from "../../../../../../../../node_modules/react-router-dom"
import Anchor from '../../../../../../../../node_modules/react-bootstrap/Anchor';
import Col from '../../../../../../../../node_modules/react-bootstrap/Col';
import Button from '../../../../../../../../node_modules/react-bootstrap/Button';
import ButtonGroup from '../../../../../../../../node_modules/react-bootstrap/ButtonGroup';
import Dropdown from '../../../../../../../../node_modules/react-bootstrap/Dropdown';
import DropdownButton from '../../../../../../../../node_modules/react-bootstrap/DropdownButton';

class LeftSidebar extends Component {
    getMenu() {
        return this.props.mainMenu.map((item, index) =>
            (item.items != null && item.items.length > 0 ) ? this.getMenuDropButton(item, index) : this.getMenuButton(item, index)
        )
    }

    getMenuButton(item, index) {
        if (item.isReal)
            return (
                <Button key={index}
                        as={Anchor} href={item.url}
                        variant={item.style}
                        size="sm"
                        title={item.label}>
                    {this.getButtonLabel(item.icon, item.label)}
                </Button>
            )
        else
            return(
                <Button
                    key={index}
                    as={Link}
                    to={item.url}
                    variant={item.style}
                    size="sm"
                    title={item.label}>
                    {this.getButtonLabel(item.icon, item.label)}
                </Button>
            )
    }

    getMenuDropButton(item, index) {
        const subMenu = item.items.map((_item, _index) => <Dropdown.Item
            key={_index}
            as={Link}
            to={_item.url}>{_item.label}
        </Dropdown.Item>);
        return(
            <DropdownButton
                key={index}
                size="sm"
                drop='end'
                title={this.getButtonLabel(item.icon, item.label)}
                as={ButtonGroup}
                variant={item.style}>
                {subMenu}
            </DropdownButton>
        )
    }

    /** Возвращает содержимое кнопки с иконкой и текстом */
    getButtonLabel(icon, text) {
        return(
        <span className="float-start label-button-menu">
                <i className={`label-icon fas fa-${icon}`}></i>
                <span className="label-text">{text}</span>
            </span>
        )
    }

    render() {
        return(
            <Col id="left-sidebar" sm={1} lg={3}>
                <ButtonGroup className="dox-bootstrap-menu" vertical aria-label="Main menu">
                    {this.getMenu()}
                </ButtonGroup>
            </Col>
        )
    }
}

function mapStatProps(state) {
    return {
        mainMenu: state.general.mainMenu
    }
}

export default connect(mapStatProps, null)(LeftSidebar);