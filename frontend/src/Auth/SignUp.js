import React, { useState } from "react";
import styled from "styled-components";
import { TextField, Button } from "@mui/material";
import { styled as muiStyled } from "@mui/material/styles";
import { useNavigate } from "react-router-dom";
import { HiMiniFire } from "react-icons/hi2";

const SignIn = () => {
  const [inputValue, setInputValue] = useState({
    userID: "",
    userPW: "",
    userPWCheck: "",
    userLOC: "",
  });
  const navigate = useNavigate();

  const { userID, userPW, userPWCheck, userLOC } = inputValue;

  const inputHandler = (e) => {
    const { name, value } = e.target;

    setInputValue({
      ...inputValue,
      [name]: value,
    });
  };

  const submitHandler = () => {
    if (!userID || !userPW || !userPWCheck || !userLOC) return;
    fetch("http://127.0.0.1:8000/api/register/", {
      //signup 요청주소 기입
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: userID,
        password: userPW,
        password2: userPWCheck,
        location: userLOC,
      }),
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.message === 200) {
          console.log("success!");
        } else if (
          res.password[0] ===
          "This password is too short. It must contain at least 8 characters."
        ) {
          console.log(
            "This password is too short. It must contain at least 8 characters."
          );
        } else if (res.password[0] === "not matched password1, password2") {
          console.log("not matched password1, password2");
        }
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
            <TextInput
              id="standard-basic"
              name="userPWCheck"
              label="PassWord check"
              variant="standard"
              type="password"
              fullWidth
              value={userPWCheck}
              onChange={inputHandler}
            />
            <TextInput
              id="standard-basic"
              name="userLOC"
              label="User Location"
              variant="standard"
              fullWidth
              value={userLOC}
              onChange={inputHandler}
            />
          </InputField>
          <SignUpButton
            variant="contained"
            size="large"
            onClick={submitHandler}
          >
            SIGNUP
          </SignUpButton>
          <GotoSignIn onClick={() => navigate("/signin")}>SIGNIN</GotoSignIn>
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
  height: 320px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
`;

const InputField = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 150px;
`;

const TextInput = muiStyled(TextField)(() => ({
  "& label.Mui-focused": {
    color: "#493d26",
  },
  "& .MuiInput-underline:after": {
    borderBottomColor: "#493d26",
  },
}));

const SignUpButton = muiStyled(Button)(() => ({
  background: "#786d5f",
  color: "black",
  "&: hover": {
    color: "white",
    background: "#786d5f",
  },
}));

const GotoSignIn = styled.button`
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
