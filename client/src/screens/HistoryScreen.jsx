import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import Loader from "../components/Loader";
import EntityList from "../components/EntityList";
import ErrorCard from "../components/ErrorCard";

async function fetchData(setData, setLoading, setError, requestInProgress) {
  if (requestInProgress.current) return;
  try {
    requestInProgress.current = true;
    setLoading(true);   
    const response = await axios.get("http://localhost:5001/get_history");
    setData(response.data);
    console.log(response.data);
  } catch (error) {
    setError(error);
  } finally {
    setLoading(false);
    requestInProgress.current = false;
  }
}

const HistoryScreen = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const requestInProgress = useRef(false);

  useEffect(() => {
    fetchData(setData, setLoading, setError, requestInProgress);
  }, []);

  if (loading) {
    return <Loader />;
  }
  if (error) {
    return <ErrorCard error={error} />;
  }

  return data ? (
    <EntityList entities={data} title={"Your History"}/>
  ) : (
    <div>
      <h1>Screen 2</h1>
    </div>
  );
};

export default HistoryScreen;
