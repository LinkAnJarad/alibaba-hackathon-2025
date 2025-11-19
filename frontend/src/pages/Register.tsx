import { useState } from "react";
import { api } from "../lib/api";
import { Link, useNavigate } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [userId, setUserId] = useState<number | null>(null);
  const navigate = useNavigate();

  const submit = async () => {
    try {
      setError(null);
      const res = await api.post("/auth/register", { email, password, name });
      setMessage(res.data.message);
      // Extract user ID from message or response
      const match = res.data.message.match(/User ID: (\d+)/);
      if (match) {
        setUserId(parseInt(match[1]));
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  const proceedToLogin = () => {
    navigate("/login");
  };

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-xl font-semibold mb-4">Register</h1>
      <div className="space-y-2">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Full Name"
          className="border rounded w-full p-2"
        />
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
          Create Account
        </button>
        {error && <div className="text-sm text-red-600">{error}</div>}
        {message && (
          <div className="text-sm text-green-700">
            {message}
            {userId && (
              <p className="mt-2 font-semibold text-blue-600">
                Keep your User ID: {userId}
              </p>
            )}
            <button
              onClick={proceedToLogin}
              className="mt-2 px-3 py-2 bg-green-600 text-white rounded text-sm"
            >
              Proceed to Login
            </button>
          </div>
        )}
        <div className="text-sm">
          Already have an account? <Link to="/login" className="text-blue-700">Login</Link>
        </div>
      </div>
    </div>
  );
}
