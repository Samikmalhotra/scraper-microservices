import React, { useEffect, useState, useRef } from "react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";
import Loader from "../components/Loader";
import { Container, Card, CardContent, Typography } from "@mui/material";
import EntityCard from "../components/EntityCard";
import ErrorCard from "../components/ErrorCard";



async function fetchData(
  number,
  setData,
  setLoading,
  setError,
  requestInProgress
) {
  if (requestInProgress.current) return;
  try {
    requestInProgress.current = true;
    const body = {
      document_number: number,
    };
    setLoading(true);
    const response = await axios.post(
      "http://localhost:5001/get_data_by_document_number",
      body
    );
    setData(response.data);

    console.log(response.data);
  } catch (error) {
    setError(error);
    console.error(error.message);
  } finally {
    setLoading(false);
    requestInProgress.current = false;
  }
}

const DocumentNumberScreen = () => {
  const { number } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const requestInProgress = useRef(false);

  useEffect(() => {
    fetchData(number, setData, setLoading, setError, requestInProgress);
  }, [number]);

  if (loading) {
    return <Loader />;
  }
  if (error) {
    return <ErrorCard error={error}/>
  }

  return data && data.length == 1 ? (
    <EntityCard data={data[0]} />
  ) : (
    <Container>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            Document Number: {number}
          </Typography>
          <Typography variant="h6" gutterBottom>
            No data found
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default DocumentNumberScreen;
