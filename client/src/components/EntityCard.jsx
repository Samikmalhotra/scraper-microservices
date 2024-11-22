import React from "react";
import {
  Container,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
  Link,
} from "@mui/material";

const EntityCard = ({ data }) => {
  return (
    <Container>
      <Card sx={{ maxWidth: 800, margin: "20px auto" }}>
        <CardContent>
          <Typography variant="h4" component="h2" gutterBottom>
            {data.name}
          </Typography>
          <Typography variant="h6" color="textSecondary">
            Document Number: {data.document_number} | Status: {data.status}
          </Typography>
          <Box sx={{ textAlign: "left", my: 2 }}>
            <Typography variant="body1">
              <strong>Filed Date:</strong> {data.date_filed}
            </Typography>
            <Typography variant="body1">
              <strong>FEI/EIN Number:</strong> {data.fei_ein_number}
            </Typography>
            <Typography variant="body1">
              <strong>Event Date Filed:</strong> {data.event_date_filed}
            </Typography>
            <Typography variant="body1">
              <strong>Last Event:</strong> {data.last_event}
            </Typography>
            <Typography variant="body1">
              <strong>Event Effective Date:</strong> {data.event_effective_date}
            </Typography>
            <Typography variant="body1">
              <strong>Address:</strong> {data.address}
            </Typography>
            <Typography variant="body1">
              <strong>Mailing Address:</strong> {data.mailing_address}
            </Typography>
            <Typography variant="body1">
              <strong>State:</strong> {data.state}
            </Typography>
            <Typography variant="body1">
              <strong>Registered Agent:</strong> {data.registered_agent} at{" "}
              {data.registered_agent_address}
            </Typography>
          </Box>
          <Box sx={{ my: 2 }}>
            <Typography variant="h6" gutterBottom>
              Annual Reports
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Year</TableCell>
                    <TableCell>Filed Date</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.annual_reports.length > 0 &&
                    data.annual_reports.map((report, index) => (
                      <TableRow key={index}>
                        <TableCell>{report.year}</TableCell>
                        <TableCell>{report.filed_date}</TableCell>
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>

          <Box sx={{ my: 2 }}>
            <Typography variant="h6" gutterBottom>
              Officers
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Title</TableCell>
                    <TableCell>Address</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.officers &&
                    data.officers.map((officer, index) => (
                      <TableRow key={index}>
                        <TableCell>{officer.name}</TableCell>
                        <TableCell>{officer.title}</TableCell>
                        <TableCell>{officer.address}</TableCell>
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>

          <Box sx={{ my: 2 }}>
            <Typography variant="h6" gutterBottom>
              Documents
            </Typography>
            {data.document_images.map((doc, index) => (
              <Link
                href={doc.link}
                key={index}
                target="_blank"
                sx={{ display: "block", marginBottom: 1 }}
              >
                {doc.title}
              </Link>
            ))}
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default EntityCard;
