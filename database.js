const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');

let db;

function initDb() {
    db = new sqlite3.Database('database.db', (err) => {
        if (err) {
            console.error('Error opening database:', err);
        } else {
            console.log('Connected to SQLite database');
            createTables();
        }
    });
}

function createTables() {
    db.run(`
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    `, (err) => {
        if (err) {
            console.error('Error creating users table:', err);
        } else {
            console.log('Users table ready');
        }
    });

    // Add more tables as needed for your application
}

function createUser(username, email, password, role, callback) {
    const hashedPassword = bcrypt.hashSync(password, 10);
    db.run(
        'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
        [username, email, hashedPassword, role],
        function(err) {
            if (err) {
                console.error('Error creating user:', err);
                callback(null, err);
            } else {
                callback(this.lastID, null);
            }
        }
    );
}

function getUserByCredentials(email, callback) {
    db.get('SELECT * FROM users WHERE email = ?', [email], (err, row) => {
        if (err) {
            console.error('Error fetching user:', err);
            callback(null, err);
        } else {
            callback(row, null);
        }
    });
}

function userExists(email, callback) {
    db.get('SELECT id FROM users WHERE email = ?', [email], (err, row) => {
        if (err) {
            console.error('Error checking user existence:', err);
            callback(false, err);
        } else {
            callback(!!row, null);
        }
    });
}

function getUserById(userId) {
    return new Promise((resolve, reject) => {
        db.get('SELECT * FROM users WHERE id = ?', [userId], (err, row) => {
            if (err) {
                reject(err);
            } else {
                resolve(row);
            }
        });
    });
}

function getPatientDetails(patientId) {
    return {
        id: patientId,
        name: "Patient User",
        email: "patient@example.com",
        medicalHistory: "No significant history",
        appointments: []
    };
}

function getDoctorDetails(doctorId) {
    return {
        id: doctorId,
        name: "Doctor User",
        email: "doctor@example.com",
        specialty: "General Medicine",
        patients: []
    };
}

module.exports = {
    initDb,
    createUser,
    getUserByCredentials,
    userExists,
    getUserById,
    getPatientDetails,
    getDoctorDetails
};