import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App'; // Import your main App component

// Get the root element from index.html
const container = document.getElementById('root');
// Create a root
const root = createRoot(container);
// Render your App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
