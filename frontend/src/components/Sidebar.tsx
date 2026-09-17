"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const workspaceItems = [
  {
    label: "Overview",
    href: "/",
  },
  {
    label: "Financials",
    href: "/financials",
  },
  {
    label: "Forecast",
    href: "/forecast",
  },
  {
    label: "Pipeline",
    href: "/pipeline",
  },
  {
    label: "Operations",
    href: "/operations",
  },
];

const analysisItems = [
  {
    label: "Scenarios",
    href: "/scenarios",
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">X</div>

        <div>
          <div className="brand-name">
            X-Fin
          </div>

          <div className="brand-caption">
            Delivery Finance
          </div>
        </div>
      </div>

      <nav className="navigation">
        <div className="nav-group">
          <div className="nav-heading">
            Workspace
          </div>

          {workspaceItems.map((item) => {
            const active =
              pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`nav-item ${
                  active ? "active" : ""
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </div>

        <div className="nav-group">
          <div className="nav-heading">
            Analysis
          </div>

          {analysisItems.map((item) => {
            const active =
              pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`nav-item ${
                  active ? "active" : ""
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </div>
      </nav>

      <div className="sidebar-footer">
        <div className="status-label">
          Data status
        </div>

        <div className="status-row">
          <span className="status-dot" />

          <span>Connected</span>
        </div>

        <div className="status-detail">
          Finance data current
        </div>
      </div>
    </aside>
  );
}