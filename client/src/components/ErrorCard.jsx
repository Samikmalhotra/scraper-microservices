import React from "react";
import {
  Card,
  CardContent,
  Typography,
  CardActions,
  Button,
} from "@mui/material";
import { Alert } from "@mui/material";
import { useNavigate } from "react-router-dom";

const ErrorCard = ({ error }) => {
  console.log(error);
  const navigate = useNavigate();
  return (
    <Card sx={{ maxWidth: 400, margin: "auto", mt: 5 }}>
      <CardContent>
        <Alert severity="error" sx={{ marginBottom: 2 }}>
          {error.message}
        </Alert>
        <Typography variant="body2" color="textSecondary">
          {error.response.data.error}
        </Typography>
      </CardContent>
      <CardActions>
        <Button
          size="small"
          variant="contained"
          color="error"
          onClick={() => window.location.reload()}
        >
          Retry
        </Button>
        <Button
          size="small"
          variant="contained"
          color="primary"
          onClick={() => navigate("/")}
        >
          Search Again
        </Button>
      </CardActions>
    </Card>
  );
};

export default ErrorCard;
