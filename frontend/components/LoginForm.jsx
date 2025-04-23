"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Alert } from "@/components/ui/alert";
import { loginUser } from "../utils/api";

export default function LoginForm({ onSuccess }) {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const router = useRouter();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Login</CardTitle>
      </CardHeader>
      <CardContent>
        <form
          className="flex flex-col gap-4"
          onSubmit={async (e) => {
            e.preventDefault();
            setError(null);
            setSuccess(null);
            const res = await loginUser(form);
            if (res.id) {
              setSuccess("Login successful!");
              onSuccess && onSuccess(res);
              // Redirect to dashboard after short delay for UX
              setTimeout(() => router.push("/dashboard"), 500);
            } else {
              setError(res);
            }
          }}
        >
          <div>
            <Label htmlFor="username">Username</Label>
            <Input
              name="username"
              value={form.username}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>
          <Button type="submit" className="w-full">
            Login
          </Button>
          {success && <Alert variant="success">{success}</Alert>}
          {error && (
            <Alert variant="destructive">
              {typeof error === "string" ? error : JSON.stringify(error)}
            </Alert>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
