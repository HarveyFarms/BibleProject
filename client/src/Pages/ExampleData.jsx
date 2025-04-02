import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function ExampleData() {
  const [username, setUsername] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/get-example-data', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();

        if (data.username) {
          setUsername(data.username);
        } else {
          console.error("Error: No username in response");
        }
      } catch (error) {
        console.error('Error fetching example data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Example Data</h1>
      <p>Example Data: {username || "Loading..."}</p>

      <p><Link to="/">Back to welcome page.</Link></p>
    </div>
  );
}

export default ExampleData;
