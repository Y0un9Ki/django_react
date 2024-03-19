import React, { useState } from "react";
import styled from "styled-components";
import { TextField, Button } from "@mui/material";
import { styled as muiStyled } from "@mui/material/styles";
import { useNavigate } from "react-router-dom";
import { HiMiniFire } from "react-icons/hi2";

const SignIn = () => {
  const [inputValue, setInputValue] = useState({ userID: "", userPW: "" });
  const navigate = useNavigate();

  const { userID, userPW } = inputValue;

  const inputHandler = (e) => {
    const { name, value } = e.target;

    setInputValue({
      ...inputValue,
      [name]: value,
    });
  };

  return (
    <SignInPage>
      <Container>
        <HiMiniFire
          size={120}
          style={{ margin: 30, cursor: "pointer" }}
          onClick={() => navigate("/")}
        />
        <FormField>
          <InputField>
            <TextInput
              id="standard-basic"
              name="userID"
              label="User ID"
              variant="standard"
              fullWidth
              value={userID}
              onChange={inputHandler}
            />
            <TextInput
              id="standard-basic"
              name="userPW"
              label="PassWord"
              variant="standard"
              type="password"
              fullWidth
              value={userPW}
              onChange={inputHandler}
            />
          </InputField>
          <SignInButton variant="contained" size="large">
            SIGNIN
          </SignInButton>
          <SignUpButton onClick={() => navigate("/signup")}>
            SIGNUP
          </SignUpButton>
        </FormField>
      </Container>
    </SignInPage>
  );
};

export default SignIn;

const SignInPage = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  width: 100vw;
  height: 100vh;
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  width: 400px;
  height: 550px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #e9e6dd;
  box-shadow: 2px 2px 2px 2px #eee;
`;

const FormField = styled.div`
  width: 240px;
  height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
`;

const InputField = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 120px;
`;

const TextInput = muiStyled(TextField)(() => ({
  "& label.Mui-focused": {
    color: "#493d26",
  },
  "& .MuiInput-underline:after": {
    borderBottomColor: "#493d26",
  },
}));

const SignInButton = muiStyled(Button)(() => ({
  background: "#786d5f",
  color: "black",
  "&: hover": {
    color: "white",
    background: "#786d5f",
  },
}));

const SignUpButton = styled.button`
  margin: 0 auto;
  width: 80px;
  height: 30px;
  border: none;
  color: #aaa;
  background-color: transparent;
  cursor: pointer;
  &:hover {
    color: black;
    transition: 0.3s;
  }
`;
