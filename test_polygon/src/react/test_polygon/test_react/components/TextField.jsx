import React from "react";
import style from "../styles/style";

const TextField = ({name, onChange, onBlur, error, label}) => (
    <div style={{marginBottom: 10}}>
        <label>
            {label}
        </label>
        <input
            style={style.input}
            type="text"
            name={name}
            onChange={onChange}
            onBlur={onBlur}
        />
        {error && <div style={style.error}>{error}</div>}
    </div>
);

const FirstNameField = ({...rest}) => (
    <TextField name="firstName"
               label="First name:"
                {...rest} />
)

const LastNameField = ({...rest}) => (
    <TextField name="lastName"
               label="Last name:"
                {...rest} />
)

export {FirstNameField, LastNameField};