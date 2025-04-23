const API_BASE = "/api/accounts/";

export async function registerUser(data) {
  const res = await fetch(API_BASE + "register/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function loginUser(data) {
  const res = await fetch(API_BASE + "login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
    credentials: "include",
  });
  return res.json();
}

export async function logoutUser(token) {
  const res = await fetch(API_BASE + "logout/", {
    method: "POST",
    headers: { Authorization: `Token ${token}` },
    credentials: "include",
  });
  return res.json();
}

export async function getUserDetail(token) {
  const res = await fetch(API_BASE + "user/", {
    headers: { Authorization: `Token ${token}` },
    credentials: "include",
  });
  return res.json();
}

export async function updateUserDetail(token, data) {
  const res = await fetch(API_BASE + "user/", {
    method: "PUT",
    headers: {
      Authorization: `Token ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    credentials: "include",
  });
  return res.json();
}

export async function getUsersByType(token, userType) {
  const res = await fetch(API_BASE + `users/${userType}/`, {
    headers: { Authorization: `Token ${token}` },
    credentials: "include",
  });
  return res.json();
}
