const express = require("express");
const session = require("express-session");
const cors = require("cors");
const path = require("path");
const {
  initDb,
  createUser,
  getUserByCredentials,
  userExists,
  getUserById,
  getPatientDetails,
  getDoctorDetails,
} = require("./database");
const authRoutes = require("./auth");

const app = express();
const PORT = 5000;

// Middleware
app.use(express.json());
app.use(express.static("public"));
app.use(
  cors({
    origin: "http://localhost:63342",
    credentials: true,
  })
);
app.use(
  session({
    secret: "your-secret-key-here-change-in-production",
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false, httpOnly: true },
  })
);

// Initialize database
initDb();

// Routes
app.use("/auth", authRoutes);

// API Routes
app.get("/api/user", (req, res) => {
  if (req.session.user_id) {
    const user = getUserById(req.session.user_id);
    if (user) {
      res.json({
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
      });
      return;
    }
  }
  res.status(401).json({ error: "Not authenticated" });
});

app.get("/api/patient/details", (req, res) => {
  if (req.session.user_id && req.session.role === "patient") {
    const patient = getPatientDetails(req.session.user_id);
    res.json(patient);
  } else {
    res.status(403).json({ error: "Not authorized" });
  }
});

app.get("/api/doctor/details", (req, res) => {
  if (req.session.user_id && req.session.role === "doctor") {
    const doctor = getDoctorDetails(req.session.user_id);
    res.json(doctor);
  } else {
    res.status(403).json({ error: "Not authorized" });
  }
});

// Serve HTML pages
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "login.html"));
});

app.get("/signup", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "signup.html"));
});

app.get("/dashboard_patient", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "dashboard_patient.html"));
});

app.get("/dashboard_doctor", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "dashboard_doctor.html"));
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Debugger PIN: 490-132-131`);
});
