import React, { useState } from "react";
import styled from "styled-components";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import categoryData from "../data/category.json";
import locaionData from "../data/location.json";
import rankData from "../data/rankdata.json";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

const Rank = () => {
  const [cat, setCat] = useState("");

  const handleChange = (event) => {
    setCat(event.target.value);
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
    },
  };

  const data = {
    labels: locaionData.locations,
    datasets: [
      {
        label: cat,
        data: rankData[cat],
        borderColor: "#1d0200",
        pointStyle: "rectRounded",
        pointRadius: 7,
        pointHoverRadius: 12,
      },
    ],
  };

  return (
    <Container>
      <SelectSeciton>
        <FormControl fullWidth>
          <InputLabel>Cat</InputLabel>
          <CustomSelect
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={cat}
            label="Cat"
            onChange={handleChange}
            variant="outlined"
          >
            {categoryData.category.map((v) => {
              return <MenuItem value={v}>{v}</MenuItem>;
            })}
          </CustomSelect>
        </FormControl>
      </SelectSeciton>
      <GraphSection>
        <Line data={data} options={options} />
      </GraphSection>
    </Container>
  );
};

export default Rank;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
`;

const SelectSeciton = styled.div`
  width: 350px;
`;

const GraphSection = styled.div``;

const CustomSelect = styled(Select)(() => ({
  backgroundColor: "#f5f5f5",
  overflow: "scroll",
  height: 50,
  "&.MuiOutlinedInput-root": {
    "& fieldset": {
      borderColor: "#aaa",
    },
    "&:hover fieldset": {
      borderColor: "#555",
    },
    "&.Mui-focused fieldset": {
      borderColor: "#222",
    },
  },
}));
