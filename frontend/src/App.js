import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { PiSignOutBold } from "react-icons/pi";
import { FaRegUser } from "react-icons/fa6";
import { HiMiniFire } from "react-icons/hi2";
import { FaUser } from "react-icons/fa6";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { styled as muiStyled } from "@mui/material/styles";
import Rank from "./Contents/Rank";
import Cat2 from "./Contents/Cat2";
import Cat3 from "./Contents/Cat3";
import QnA from "./Contents/QnA";

function App() {
  const [value, setValue] = useState(0);
  const navigate = useNavigate();
  const [signinStatus, setSigninStatus] = useState(false);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  console.log(value);

  useEffect(() => {
    if (localStorage.getItem("SEMITOKEN")) {
      setSigninStatus(true);
    }
  }, []);

  return (
    <Mainpage>
      <Container>
        <Header>
          <HiMiniFire size={40} />
          {signinStatus ? (
            <Auth>
              <FaUser size={25} style={{ cursor: "pointer" }} />
              <PiSignOutBold
                size={30}
                style={{ cursor: "pointer" }}
                onClick={() => {
                  localStorage.removeItem("SEMITOKEN");
                  setSigninStatus(false);
                }}
              />
            </Auth>
          ) : (
            <Auth>
              <FaRegUser
                size={25}
                style={{ cursor: "pointer" }}
                onClick={() => navigate("/signin")}
              />
            </Auth>
          )}
        </Header>
        <Tapbar>
          <StyleTabs
            value={value}
            onChange={handleChange}
            variant="scrollable"
            scrollButtons={false}
            aria-label="scrollable prevent tabs example"
            TabIndicatorProps={{ style: { backgroundColor: "#493d26" } }}
          >
            <StyleTab label="서울시 주택화재 취약지역 분석" />
            <StyleTab label="Cat2" />
            <StyleTab label="Cat3" />
            <StyleTab label="문의사항" />
          </StyleTabs>
        </Tapbar>
        <ContentSection>
          {value === 0 && <Rank />}
          {value === 1 && <Cat2 />}
          {value === 2 && <Cat3 />}
          {value === 3 && <QnA />}
        </ContentSection>
      </Container>
    </Mainpage>
  );
}

export default App;

const Mainpage = styled.div`
  display: flex;
  justify-content: center;
  background-color: #f5f5f5;
`;

const Container = styled.div`
  width: 800px;
  height: 100vh;
  background-color: #e9e6dd;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 20px;
  padding-right: 20px;
  height: 60px;
  border-bottom: 1px solid #554d42;
`;

const Auth = styled.div`
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 80px;
  height: 64px;
`;

const Tapbar = styled.div`
  width: 100%;

  border-bottom: 1px solid #afa79c;
`;

const StyleTabs = muiStyled(Tabs)(() => ({
  color: "black",
}));

const StyleTab = muiStyled(Tab)(() => ({
  color: "#aaa",
  borderBottomColor: "#493d26",
  "&.Mui-selected": {
    color: "#493d26",
    borderBottomColor: "#493d26",
  },
}));

const ContentSection = styled.div`
  padding-top: 30px;
  height: 80vh;
`;
