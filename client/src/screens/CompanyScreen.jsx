import React, { useEffect, useState, useRef } from "react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";
import EntityList from "../components/EntityList";
import Loader from "../components/Loader";
import ErrorCard from "../components/ErrorCard";

async function fetchData(
  name,
  setData,
  setLoading,
  setError,
  requestInProgress
) {
  if (requestInProgress.current) return;
  try {
    requestInProgress.current = true;
    const body = {
      entity_name: name,
    };
    const response = await axios.post(
      "http://localhost:5000/scrape_data_by_entity_name",
      body
    );
    setData(response.data);
  } catch (error) {
    setError(error);
  } finally {
    setLoading(false);
    requestInProgress.current = false;
  }
}

const CompanyScreen = () => {
  const { name } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const requestInProgress = useRef(false);
  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchData(name, setData, setLoading, setError, requestInProgress);
  }, [name]);

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return <ErrorCard error={error} />;
  }

  return data ? (
    <EntityList entities={data} title={"Companies matching search criteria"}/>
  ) : (
    <div>
      <h1>Screen 1</h1>
    </div>
  );
};

export default CompanyScreen;
