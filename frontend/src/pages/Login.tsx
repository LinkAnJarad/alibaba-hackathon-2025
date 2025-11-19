import { useState } from "react";
import { api } from "../lib/api";
import { Link, useNavigate } from "react-router-dom";

interface User {
  id: number;
  email: string;
  name: string;
  verified: boolean;
  role: string;
}

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const submit = async () => {
    try {
      setError(null);
      const res = await api.post("/auth/login", { email, password });
      const userData = res.data as User;
      setUser(userData);
      // Store user ID in localStorage for prototyping
      localStorage.setItem("userId", userData.id.toString());
      // Redirect to dashboard
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-xl font-semibold mb-4">Login</h1>
      <div className="space-y-2">
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="border rounded w-full p-2"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="border rounded w-full p-2"
        />
        <button onClick={submit} className="px-3 py-2 bg-blue-600 text-white rounded">
          Sign In
        </button>
        {error && <div className="text-sm text-red-600">{error}</div>}
        {user && (
          <div className="text-sm text-green-700">
            Welcome {user.name}! (ID: {user.id})
          </div>
        )}
        <div className="text-sm">
          No account? <Link to="/register" className="text-blue-700">Register</Link>
        </div>
      </div>
    </div>
  );
}
