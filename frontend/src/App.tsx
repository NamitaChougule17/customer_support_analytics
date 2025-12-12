// src/App.tsx
import React from "react";
import Sidebar from "./layout/Sidebar";
import Header from "./layout/Header";
import DashboardPage from "./pages/DashboardPage";
import "./styles/style.css";

const App: React.FC = () => {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-main">
        <Header />
        <DashboardPage />
      </div>
    </div>
  );
};

export default App;
