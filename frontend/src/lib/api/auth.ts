import { apiRequest } from "./client";

export type LoginRequest = {
  email: string;
  password: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export type MeResponse = {
  id: string;
  email: string;
  full_name: string;
  role: string;
};

export async function loginRequest(payload: LoginRequest): Promise<LoginResponse> {
  const formData = new URLSearchParams();
  formData.append("username", payload.email); // OAuth2PasswordRequestForm espera username
  formData.append("password", payload.password);

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  });

  if (!response.ok) {
    let errorMessage = "Error inesperado en login";

    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      errorMessage = `Error HTTP ${response.status}`;
    }

    throw new Error(errorMessage);
  }

  return response.json();
}

export async function meRequest(): Promise<MeResponse> {
  return apiRequest<MeResponse>("/auth/me", {
    method: "GET",
    auth: true,
  });
}