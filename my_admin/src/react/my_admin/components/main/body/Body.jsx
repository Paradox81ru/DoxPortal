import React, {Component} from "../../../../../../../../node_modules/react";
import Container from "../../../../../../../../node_modules/react-bootstrap/Container";
import Row from "../../../../../../../../node_modules/react-bootstrap/Row";
import MainContent_W from "../../../../../../../main/src/react/main/components/main/body/content/MainContent";

export default function Body() {

    return (
        <div className="body">
            <Container fluid="xxl">
                <Row>
                    <MainContent_W admin />
                </Row>
            </Container>
        </div>
    )
}