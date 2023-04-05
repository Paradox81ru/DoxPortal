import React from "../../../../../../../../../../node_modules/react";
import ContactCard from "./Components/ContactCard";
import "./style/index.css"

function App() {
    return (
        <div className="contacts">
            <ContactCard
                contact={{
                    name: "Mr. Whiskerson",
                    imgUrl: "http://placekitten.com/300/200",
                    phone: "(212) 555-1234",
                    email: "mr.whiskaz@catnap.meow"
                }}
            />

            <ContactCard
                contact={{
                    name: "Fluffykins",
                    imgUrl: "http://placekitten.com/400/200",
                    phone: "(212) 555-2345",
                    email: "fluff@me.com"
                }}
            />

            <ContactCard
                name="Destroyer"
                imgUrl="http://placekitten.com/400/300"
                phone="(212) 555-3456"
                email="ofworlds@yahoo.com"
            />

            <ContactCard
                name="Felix"
                imgUrl="http://placekitten.com/200/100"
                phone="(212) 555-4567"
                email="thecat@hotmail.com"
            />
        </div>
    )
}

export default App;