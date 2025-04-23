"use client";
import React, { useState } from "react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

export default function LandingPage() {
  const [view, setView] = useState("landing");

  if (view === "login") {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <LoginForm />
        <button
          className="mt-4 underline text-blue-600"
          onClick={() => setView("landing")}
        >
          ← Back to Home
        </button>
      </div>
    );
  }

  if (view === "register") {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <RegisterForm />
        <button
          className="mt-4 underline text-blue-600"
          onClick={() => setView("landing")}
        >
          ← Back to Home
        </button>
      </div>
    );
  }

  // Default landing view
  return (
    <main className="flex flex-col items-center justify-center min-h-[60vh] gap-8">
      <h1 className="text-4xl font-bold text-center">
        Welcome to SmartAgriFlow
      </h1>
      <p className="text-lg text-center max-w-xl">
        Manage your banana shipments, track ripeness, and connect with farmers,
        distributors, and retailers.
      </p>
      <div className="flex gap-4">
        <button
          className="px-6 py-3 rounded bg-blue-600 text-white hover:bg-blue-700 transition text-lg font-semibold"
          onClick={() => setView("login")}
        >
          Login
        </button>
        <button
          className="px-6 py-3 rounded bg-green-600 text-white hover:bg-green-700 transition text-lg font-semibold"
          onClick={() => setView("register")}
        >
          Register
        </button>
      </div>
    </main>
  );
}
