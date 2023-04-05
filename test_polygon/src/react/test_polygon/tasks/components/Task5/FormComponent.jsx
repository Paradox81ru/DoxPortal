// noinspection NpmUsedModulesInstalled
import React, {Component} from "react";

function FormComponent(props) {
    return (
        <form onSubmit={props.handleSubmit}>
            <input type="text"
                   value={props.data.firstName}
                   name="firstName"
                   placeholder="First name"
                   onChange={props.handleChange}/>
            <br/>
            <input type="text"
                   value={props.data.lastName}
                   name="lastName"
                   placeholder="Last name"
                   onChange={props.handleChange}
            />
            <br/>
            <textarea
                value="Some default value"
                onChange={props.handleChange}
            />
            <br/>
            <label>
                <input
                    type="radio"
                    name="gender"
                    value="male"
                    checked={props.data.gender === "male"}
                    onChange={props.handleChange}
                /> Male
            </label>
            <br/>
            <label>
                <input
                    type="radio"
                    name="gender"
                    value="female"
                    checked={props.data.gender === "female"}
                    onChange={props.handleChange}
                /> Female
            </label>
            <br/>
            <label>Favorite Color:</label>
            <select
                value={props.data.favColor}
                onChange={props.handleChange}
                name="favColor"
            >
                <option value="blue">Blue</option>
                <option value="green">Green</option>
                <option value="red">Red</option>
                <option value="orange">Orange</option>
                <option value="yellow">Yellow</option>
            </select>
            <br/>
            <label>
                <input
                    type="checkbox"
                    name="isVegan"
                    onChange={props.handleChange}
                    checked={props.data.dietaryRestrictions.isVegan}
                /> Vegan?
            </label>
            <br/>
            <label>
                <input
                    type="checkbox"
                    name="isKosher"
                    onChange={props.handleChange}
                    checked={props.data.dietaryRestrictions.isKosher}
                /> Kosher?
            </label>
            <br/>

            <label>
                <input
                    type="checkbox"
                    name="isLactoseFree"
                    onChange={props.handleChange}
                    checked={props.data.dietaryRestrictions.isLactoseFree}
                /> Lactose Free?
            </label>
            <h3>{props.data.firstName} {props.data.lastName}</h3>
            <h4>You are a {props.data.gender}</h4>
            <h4>Your favorite color is {props.data.favColor}</h4>
            <p>Your dietary restrictions:</p>

            <p>Vegan: {props.data.dietaryRestrictions.isVegan ? "Yes" : "No"}</p>
            <p>Kosher: {props.data.dietaryRestrictions.isKosher ? "Yes" : "No"}</p>
            <p>Lactose Free: {props.data.dietaryRestrictions.isLactoseFree ? "Yes" : "No"}</p>
            <button>Submit</button>
        </form>
    )
}

export default FormComponent