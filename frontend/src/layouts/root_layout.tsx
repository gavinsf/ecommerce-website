// src/layouts/RootLayout.tsx
import { type ReactElement } from "react";
import { Outlet, Link } from "react-router-dom";

export default function RootLayout(): ReactElement {
    return (
        <div className="app-container">
            <nav>
                <Link to="/">Home</Link>
            </nav>

            <main>
                {/* Active sub-routes will render here */}
                <Outlet />
            </main>
        </div>
    );
}