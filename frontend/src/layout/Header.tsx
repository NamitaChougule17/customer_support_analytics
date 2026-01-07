// src/layout/Header.tsx
import React from "react";

const Header: React.FC = () => {
  return (
    <header className="header">
      <div>
        <h1 className="header-title">Customer Support Call Analytics</h1>
        <p className="header-subtitle">
          React + TypeScript · FastAPI · Python · Supabase · Analytics · AI-ready insights
        </p>
      </div>
    </header>
  );
};

export default Header;
