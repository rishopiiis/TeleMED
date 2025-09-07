const express = require("express");
const bcrypt = require("bcryptjs");
const { createUser, getUserByCredentials, userExists } = require("./database");

const router = express.Router();

router.post("/login", (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: "Email and password required" });
  }

  getUserByCredentials(email, (user, err) => {
    if (err) {
      return res.status(500).json({ error: "Server error" });
    }

    if (user && bcrypt.compareSync(password, user.password)) {
      req.session.user_id = user.id;
      req.session.username = user.username;
      req.session.email = user.email;
      req.session.role = user.role;

      res.json({
        message: "Login successful",
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          role: user.role,
        },
      });
    } else {
      res.status(401).json({ error: "Invalid credentials" });
    }
  });
});

router.post("/signup", (req, res) => {
  const { username, email, password, role } = req.body;

  if (!username || !email || !password || !role) {
    return res.status(400).json({ error: "All fields are required" });
  }

  if (!["patient", "doctor", "volunteer"].includes(role)) {
    return res.status(400).json({ error: "Invalid role" });
  }

  userExists(email, (exists, err) => {
    if (err) {
      return res.status(500).json({ error: "Server error" });
    }

    if (exists) {
      return res.status(409).json({ error: "User already exists" });
    }

    createUser(username, email, password, role, (userId, error) => {
      if (error) {
        return res.status(500).json({ error: "Failed to create user" });
      }

      req.session.user_id = userId;
      req.session.username = username;
      req.session.email = email;
      req.session.role = role;

      res.status(201).json({
        message: "User created successfully",
        user: {
          id: userId,
          username: username,
          email: email,
          role: role,
        },
      });
    });
  });
});

router.post("/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ error: "Logout failed" });
    }
    res.json({ message: "Logged out successfully" });
  });
});

module.exports = router;
