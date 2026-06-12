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
    <main className="authSplit">
      <section className="authBrandPanel">
        <div className="logoBlock">&lt;/&gt;</div>
        <h1>Sorting Game</h1>
        <h2>Master Sorting Algorithms</h2>
        <p>Play, learn, and compete in sorting challenges. Improve your skills and climb the leaderboard.</p>
      </section>
      <section className="authFormPanel">
        <article className="authBox">
          <h2>{mode === "login" ? "Welcome Back!" : "Create Account"}</h2>
          <p>{mode === "login" ? "Sign in to your account" : "Fill in the details to register"}</p>
          <form onSubmit={submit}>
            <label>Username<input placeholder="Enter your username" value={username} onChange={e => setUsername(e.target.value)} required /></label>
            {mode === "register" && <label>Email<input placeholder="Enter email" type="email" value={email} onChange={e => setEmail(e.target.value)} required /></label>}
            {mode === "register" && (
              <label>Class
                <select value={className} onChange={e => setClassName(e.target.value)}>
                  <option>12SV</option><option>12SD</option><option>13AG</option><option>13TA</option>
                </select>
              </label>
            )}
            <label>Password<input placeholder="Enter password" type="password" value={password} onChange={e => setPassword(e.target.value)} required /></label>
            {error && <div className="error">{error}</div>}
            <button className="primary wide" type="submit">{mode === "login" ? "Login" : "Register"}</button>
          </form>
          <p className="switchText">{mode === "login" ? "Don't have an account?" : "Already have an account?"} <button className="inlineLink" onClick={() => setMode(mode === "login" ? "register" : "login")}>{mode === "login" ? "Register here" : "Login here"}</button></p>
        </article>
      </section>
    </main>
  );
}
