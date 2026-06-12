import { FormEvent, useState } from "react";
import { api, setToken, User } from "../api/client";

type Props = { onAuth: (user: User) => void };

export function AuthPage({ onAuth }: Props) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [className, setClassName] = useState("12SV");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    try {
      const response = mode === "login"
        ? await api.login({ username, password })
        : await api.register({ username, email, class_name: className, password });
      setToken(response.token);
      onAuth(response.user);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not sign in");
    }
  }

  return (
    <main className="authPage">
      <section className="card authCard">
        <h1>Sorting Game Online</h1>
        <p>Practise Bubble Sort and Insertion Sort passes, compete for scores, and track class analytics.</p>
        <form onSubmit={submit}>
          <label>Username<input value={username} onChange={e => setUsername(e.target.value)} required /></label>
          {mode === "register" && <label>Email<input type="email" value={email} onChange={e => setEmail(e.target.value)} required /></label>}
          {mode === "register" && (
            <label>Class
              <select value={className} onChange={e => setClassName(e.target.value)}>
                <option>12SV</option><option>12SD</option><option>13AG</option><option>13TA</option>
              </select>
            </label>
          )}
          <label>Password<input type="password" value={password} onChange={e => setPassword(e.target.value)} required /></label>
          {error && <div className="error">{error}</div>}
          <button className="primary" type="submit">{mode === "login" ? "Log in" : "Register"}</button>
        </form>
        <button className="linkButton" onClick={() => setMode(mode === "login" ? "register" : "login")}>{mode === "login" ? "Create a new account" : "Already have an account? Log in"}</button>
      </section>
    </main>
  );
}
