const API_BASE =
  (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/").replace(
    /\/+$/,
    ""
  ) + "/api/accounts/";

// Helper to handle fetch errors
async function fetchWithError(url, options) {
  try {
    const res = await fetch(url, options);
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `HTTP error ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    // Log for debugging
    console.error("API fetch error:", url, err);
    throw err;
  }
}

export async function registerUser(data) {
  return fetchWithError(API_BASE + "register/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export async function loginUser(data) {
  return fetchWithError(API_BASE + "login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
    credentials: "include",
  });
}

export async function logoutUser(token) {
  return fetchWithError(API_BASE + "logout/", {
    method: "POST",
    headers: { Authorization: `Token ${token}` },
    credentials: "include",
  });
}

export async function getUserDetail(token) {
  return fetchWithError(API_BASE + "user/", {
    headers: { Authorization: `Token ${token}` },
    credentials: "include",
  });
}

export async function updateUserDetail(token, data) {
  return fetchWithError(API_BASE + "user/", {
    method: "PUT",
    headers: {
      Authorization: `Token ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    credentials: "include",
  });
}

export async function getUsersByType(token, userType) {
  return fetchWithError(API_BASE + `users/${userType}/`, {
    headers: { Authorization: `Token ${token}` },
    credentials: "include",
  });
}
