import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css'; // Make sure your CSS styles are copied here

const LoginPage = ({ setIsAuthenticated }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const navigate =  useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {

      if (username === ''|| password === '')
      {
        alert("please enter both username and password");
        return;
      }
      const response = await axios.post('http://localhost:5000/', { username, password });
      const data = response.data;

      if (response.status >= 200 && response.status < 300) {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        setIsAuthenticated(true);
        alert('Login successful!');
        navigate('/home')
      } else {
        setErrorMsg(data.message||'Login failed');
        alert('invalid credentials');
      }
    } catch (err) {
      if (err.response && err.response.data) {
        setErrorMsg(err.response.data.message || 'Login failed');
      } else {
        setErrorMsg('An error occurred');
      }
      alert(errorMsg);
    }
  };

  return (
    <div className="login-box">
      <h2>Login</h2>
      <form className="form" onSubmit={handleSubmit}>
        <div className="user-box">
          <input
            className="input"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            // required
          />
          <label className="label">Username</label>
        </div>

        <div className="user-box">
          <input
            className="input"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            // required
          />
          <label className="label">Password</label>
        </div>

        <button type="submit" className="submit-btn">
          {/* replicate the span animation elements */}
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          Login
        </button>
      </form>
      {errorMsg && <p className="error">{errorMsg}</p>}
    </div>
  );
};

export default LoginPage;
