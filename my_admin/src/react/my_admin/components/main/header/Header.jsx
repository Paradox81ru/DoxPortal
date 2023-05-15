import React, {Component} from "../../../../../../../../node_modules/react";
import {Link} from "../../../../../../../../node_modules/react-router-dom";
import Container from '../../../../../../../../node_modules/react-bootstrap/Container';
import Navbar from '../../../../../../../../node_modules/react-bootstrap/Navbar';
import Navigation from "./navbar/Navigation";

export default function Header() {
    return(
        <Navbar bg="dark" expand="md" variant="dark" fixed="top">
            <Container>
                <Navbar.Brand as={Link} to="/dox-admin/">MyAdmin</Navbar.Brand>
                <Navbar.Toggle aria-controls="navbarSupportedContent" />
                <Navigation />
            </Container>
        </Navbar>
    )
}