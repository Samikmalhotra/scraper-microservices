import "./App.css";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import HomeScreen from "./screens/HomeScreen";
import CompanyScreen from "./screens/CompanyScreen";
import DocumentNumberScreen from "./screens/DocumentNumberScreen";
import HistoryScreen from "./screens/HistoryScreen";
import Sidebar from "./components/Sidebar";

function App() {
  return (
    <Router>
      <Sidebar />
      <Routes>
        <Route path="/" element={<HomeScreen/>} />
        <Route path="/history" element={<HistoryScreen/>} />
        <Route path="/company/:name" element={<CompanyScreen/>} />
        <Route path="/document/:number" element={<DocumentNumberScreen/>} />
      </Routes>
    </Router>
  );
}

export default App;
