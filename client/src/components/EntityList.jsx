import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
} from "@mui/material";
import { Link, useNavigate } from "react-router-dom";

const EntityList = ({ entities, title }) => {
  const navigate = useNavigate();

  return (
    <Paper sx={{ overflow: "hidden" }}>
      <Typography
        variant="h6"
        // gutterBottom
        align="center"
        sx={{ marginTop: 3 }}
      >
        {title}{':'}
      </Typography>
      <TableContainer>
        <Table sx={{ minWidth: 700 }} aria-label="entity table">
          <TableHead>
            <TableRow>
              <TableCell
                align="center"
                sx={{ fontWeight: "bolder" }}
                width={450}
              >
                Entity Name
              </TableCell>
              <TableCell align="center" sx={{ fontWeight: "bolder" }} width={150}>
                Document Number
              </TableCell>
              <TableCell align="center" sx={{ fontWeight: "bolder" }} width={100}>
                Status
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {entities.map((entity, index) => (
              <TableRow
                key={index}
                onClick={() => navigate("/document/" + entity.document_number)}
                className="company-table-row"
              >
                <TableCell align="center">{entity.name}</TableCell>
                <TableCell align="center">{entity.document_number}</TableCell>
                <TableCell align="center">{entity.status}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};

export default EntityList;
