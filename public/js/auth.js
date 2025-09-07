document.addEventListener("DOMContentLoaded", function () {
  checkAuthStatus();

  const loginForm = document.getElementById("loginForm");
  if (loginForm) loginForm.addEventListener("submit", handleLogin);

  const signupForm = document.getElementById("signupForm");
  if (signupForm) signupForm.addEventListener("submit", handleSignup);

  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) logoutBtn.addEventListener("click", handleLogout);
});

async function checkAuthStatus() {
  try {
    const response = await fetch("http://localhost:5000/api/user", {
      credentials: "include",
    });

    if (response.ok) {
      const user = await response.json();
      handleAuthenticatedUser(user);
    } else {
      handleUnauthenticatedUser();
    }
  } catch (error) {
    console.error("Auth check error:", error);
  }
}

function handleAuthenticatedUser(user) {
  if (["/", "/login", "/signup"].includes(window.location.pathname)) {
    redirectBasedOnRole(user.role);
  }

  const usernameDisplay = document.getElementById("usernameDisplay");
  if (usernameDisplay) {
    usernameDisplay.textContent = `Welcome, ${user.username} (${user.role})`;
  }
}

function handleUnauthenticatedUser() {
  if (window.location.pathname.includes("dashboard")) {
    window.location.href = "/login";
  }
}

function redirectBasedOnRole(role) {
  if (role === "patient") {
    window.location.href = "/dashboard_patient";
  } else {
    window.location.href = "/dashboard_doctor";
  }
}

async function handleLogin(e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const credentials = {
    email: formData.get("email"),
    password: formData.get("password"),
  };

  try {
    const response = await fetch("http://localhost:5000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
      credentials: "include",
    });

    const data = await response.json();

    if (response.ok) {
      redirectBasedOnRole(data.user.role);
    } else {
      alert(data.error || "Login failed");
    }
  } catch (error) {
    console.error("Login error:", error);
    alert("Login failed. Please try again.");
  }
}

async function handleSignup(e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const userData = {
    username: formData.get("username"),
    email: formData.get("email"),
    password: formData.get("password"),
    role: formData.get("role"),
  };

  try {
    const response = await fetch("http://localhost:5000/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
      credentials: "include",
    });

    const data = await response.json();

    if (response.ok) {
      redirectBasedOnRole(data.user.role);
    } else {
      alert(data.error || "Signup failed");
    }
  } catch (error) {
    console.error("Signup error:", error);
    alert("Signup failed. Please try again.");
  }
}

async function handleLogout() {
  try {
    const response = await fetch("http://localhost:5000/auth/logout", {
      method: "POST",
      credentials: "include",
    });

    if (response.ok) {
      window.location.href = "/";
    }
  } catch (error) {
    console.error("Logout error:", error);
  }
}
