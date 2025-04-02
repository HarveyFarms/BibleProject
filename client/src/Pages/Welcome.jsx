// WelcomePage.js
import React from 'react';
import { Link } from 'react-router-dom';

function WelcomePage() {
  return (
    <div>
      <h1>Welcome to the Bible Project!</h1>
      <p><Link to="/example-data">See Example Data</Link></p>
    </div>
  );
}

export default WelcomePage;