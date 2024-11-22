import React from "react";
import CircularProgress from "@mui/material/CircularProgress";

const Loader = () => {
  return (
    <div style={{ textAlign: "center", padding: "20px", color: "#000000" }}>
      <CircularProgress />
      <h5>Loading...</h5>
    </div>
  );
};

export default Loader;
