import React, {Component} from "../../../../../../../../node_modules/react";
import Container from "../../../../../../../../node_modules/react-bootstrap/Container";
import Row from "../../../../../../../../node_modules/react-bootstrap/Row";

import LeftSidebar_W from "./LeftSidebar";
import MainContent_W from "./content/MainContent";

export default function Body() {
    return (
        <div className="body">
            <Container>
                <Row>
                    <LeftSidebar_W/>
                    <MainContent_W />
                </Row>
            </Container>
        </div>
    )
}
