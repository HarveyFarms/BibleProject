//////////////////////////////////////////////////
// LIBRARIES & DEPENDENCIES
// Node.js is a variant of JavaScript that works on the back-end
// Node applications can be managed from the command line using the node-package-manager (NPM) command
// - express is a library built to make developing Node applications easier
// - body-parser
// - mysql12/promise is a library used for connecting to our MySQL DBMS 
// - cors is a library used to enable cross-origin reference sharing (CORS)
// - dotenv is a library used for extracting environment variables from a .env file
// - bcryptjs is a library used for encrypting passwords (using a hash algorithm + salting)
// - session is a library for express that enables us to easily create session cookies to manage user sessions
// - passport is the library we are using for mainstreaming the authentication process
// - passport-local is an extension of passport used for performing local authentication
//////////////////////////////////////////////////

import express from 'express';
import bodyParser from "body-parser";
import cors from 'cors';
import config from "./config.js";
import bcrypt from "bcryptjs";
import nodemailer from "nodemailer";
import session from "express-session";
import passport from "passport";
import { Strategy } from "passport-local";

// Back-end logic
import Database from './infrastructure/database.js';

//////////////////////////////////////////////////
// Initialize Express app                       //
//////////////////////////////////////////////////
const app = express();

//////////////////////////////////////////////////
// Setup Email Management System                //
//////////////////////////////////////////////////
const transporter = nodemailer.createTransport({
  service: "Gmail",
  host: config.mail.host,
  port: config.mail.port,
  secure: true,
  auth: {
    user: config.mail.user,
    pass: config.mail.password
  },
});

async function sendVerificationEmail(email, verificationCode) {
  try {
    await transporter.sendMail({
      from: `"Paintball.io" <no-reply@paintball.io>`,
      to: email,
      subject: "Verify Your Account",
      html: `<p>Here is your verification code: ${verificationCode}</p>`
    }, (error, info) => {
      if (error) {
        console.log(error);
      } else {
        console.log("Email sent: " + info.response);
      }
    });

    //console.log("Verification email sent to:", email);
  } catch (error) {
    console.error("Error sending email:", error.message);
  }
}


//////////////////////////////////////////////////
// Middleware                                   //
//////////////////////////////////////////////////

// enable cross-origin reference sharing (CORS)
app.use(cors({
  origin: "http://localhost:3000",
  credentials: true
}));

// enable JSON format for data transfer
app.use(express.json());

// parses data passed through the URL
app.use(bodyParser.urlencoded({ extended: true }));


//////////////////////////////////////////////////
// Create Database Connection                   //
//////////////////////////////////////////////////
const db = new Database(config);

await db.test_connection();

//////////////////////////////////////////////////
// Back-end API                                 //
// This provides an interface for the front-end //
// to have access to all the data managed by    //
// the back-end                                 //
// e.g.: app.get(), app.post(), etc.            //
//////////////////////////////////////////////////

//////////////////////////////////////////////////
// Example GET Request                          //
//////////////////////////////////////////////////
app.get('/get-example-data', async (req, res) => {
  try {
    return res.json({ username: "RyanIsAmazing" });
  } catch (error) {
    console.error("Error signing up user:", error.message);
    return res.json({ error: "Internal server error" });
  }
});


//////////////////////////////////////////////////
// Run Server                                   //
//////////////////////////////////////////////////
const server = app.listen(config.app.port, () => {
  console.log(`Server running on port ${config.app.port}`);
});