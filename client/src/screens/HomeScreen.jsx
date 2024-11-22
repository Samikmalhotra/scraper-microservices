import {
  TextField,
  Box,
  Button,
  Chip,
  Card,
  Typography,
  Container,
  InputAdornment,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const HomeScreen = () => {
  const [searchtext, setSearchtext] = useState("");
  const [searchByCompany, setSearchByCompany] = useState(true);
  const navigate = useNavigate();
  const formSubmitHandler = (e) => {
    e.preventDefault();
    console.log(searchtext);
    setSearchtext("");
    searchByCompany
      ? navigate("/company/" + searchtext)
      : navigate("/document/" + searchtext);
  };
  return (
    <>
      <Container sx={{ width: 800, margin: "20px" }}>
        <Typography variant="h4" component="h2" gutterBottom sx={{ margin: 4, color: "#000000" }}>
          Search for a Company or Document Number
        </Typography>
        <Container sx={{ width: 700 }}>
          <Box id="search-div">
            <form onSubmit={formSubmitHandler}>
              <TextField
                id="input-with-sx"
                label={
                  searchByCompany
                    ? "Search for a company"
                    : "Search for a document"
                }
                variant="outlined"
                value={searchtext}
                onChange={(e) => setSearchtext(e.target.value)}
                fullWidth
                slotProps={{
                  input: {
                    endAdornment: (
                      <InputAdornment position="end">
                        <Button type="submit" sx={{ marginLeft: 2 }}>
                          <SearchIcon />
                          Search
                        </Button>
                      </InputAdornment>
                    ),
                  },
                }}
              />
            </form>
          </Box>
          <Box sx={{ textAlign: "center", margin: 4}}>
            <Chip
              label="Search by Company"
              onClick={() => setSearchByCompany(true)}
              variant={searchByCompany ? "filled" : "outlined"}
              sx={{ padding: 1, mr: 2 }}
              color="primary"
            />
            <Chip
              label="Search by Document Number"
              variant={searchByCompany ? "outlined" : "filled"}
              onClick={() => setSearchByCompany(false)}
              color="primary"
            />
          </Box>
        </Container>
      </Container>
    </>
  );
};

export default HomeScreen;
