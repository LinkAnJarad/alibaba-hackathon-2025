import { useState } from "react";
import { api } from "../lib/api";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  const submit = async () => {
    const res = await api.post("/auth/register", { email, password, name });
    setMessage(res.data.message);
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
        {message && <div className="text-xs text-green-700">{message}</div>}
      </div>
    </div>
  );
}
