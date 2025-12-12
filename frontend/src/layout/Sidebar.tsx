// src/layout/Sidebar.tsx
import React from "react";

const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-title">CS Analytics</div>
      <nav className="sidebar-nav">
        <div className="sidebar-item sidebar-item-active">
          Dashboard
        </div>
      </nav>
    </aside>
  );
};

export default Sidebar;
