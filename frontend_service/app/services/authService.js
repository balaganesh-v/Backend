const AUTH_API = "http://localhost:8000/principal";

// Generic POST request helper
async function postRequest(endpoint, payload) {
  try {
    const response = await fetch(`${AUTH_API}/${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "Request failed");
    }

    return await response.json();
  } catch (error) {
    console.error(`${endpoint} Error:`, error);
    throw error;
  }
}

// Now your service functions are much shorter:
export function login(payload) {
  return postRequest("login", payload);
}

export function forgetPassword(email) {
  return postRequest("forget_password", { principal_email: email });
}

export function resetPassword(payload) {
  return postRequest("reset_password", payload); // { token, new_password }
}

export function addUserService(payload) {
  return postRequest("add_user", payload); // { user_name, user_email, user_password, user_role, user_class? }
}
