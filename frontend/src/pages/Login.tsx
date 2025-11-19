import { useState } from "react";
import { api } from "../lib/api";
import { Link } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);

  const submit = async () => {
    const res = await api.post("/auth/login", { email, password });
    setToken(res.data.access_token);
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
        {token && (
          <div className="text-xs text-green-700">Signed in. Token: {token}</div>
        )}
        <div className="text-sm">
          No account? <Link to="/register" className="text-blue-700">Register</Link>
        </div>
      </div>
    </div>
  );
}
