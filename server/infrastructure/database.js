import mysql from "mysql2/promise";
import bcrypt from "bcryptjs";
// Note: Assumes config.js is imported already

export default class Database {
  constructor(config) {
    // TODO: use mysql2 library to create a connetion to your database
    // using the parameters we configured in config.js
    // i.e.: config.db.host
  }

  // this will test if you have setup the connection successfully
  async test_connection() {
    try {
      const connection = await this.db.getConnection();
      console.log("Connected to the MySQL database!");
      connection.release();
    } catch (error) {
      console.error("Error connecting to the database:", error.message);
    }
  }

  async get_verified_users(config) {
    // get verified users from 'users' users table
  }

  async get_unverified_users(config) {
    // get unverified users from "unverified_users" table
  }

  async is_username_registered(username) {
    // searches if given username exists in the users OR unverified_users tables
  }

  async is_email_registered(email) {
    // searches if given email exists in the users OR unverified_users tables
  }

  async register_user(config, cb) {
    // receives user info from config object
    // and then adds a user into the unverified_users table
    // cb is the function we want to call once the user has
    // been registered successfully 
    // i.e.: for user registration, we want to send them a email to verify their account
  }


  async verify_user(config, cb) {
    // once the user has been registered into unverified_users table
    // and they receive the code from the email sent to them
    // then we can call this method, which receives 
    // the code typed in from the user (on the front end)
    // which is passed here through the config object
    // if config.code matches the code generated in the unverified_users table
    // then the user should be moved from the unverified_users table
    // into the users table
    // the callback (cb) method is used to return a success method
  }

  async resend_verification_email(config, cb) {
    // this method should simply send an email to a user
    // who exists in the unverified_users table
    // used in case someone accidentally misses the previous email for some reason
  }

  refresh_unverified_users() {
    // this should create a interval to run on our server
    // so that we routinely deleted users from the unverified_users table
    // that way if someone registers an account and never verifies it
    // then their account is removed after a cerrtain amount of time
  }
}