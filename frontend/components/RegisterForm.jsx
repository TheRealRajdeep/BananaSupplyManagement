"use client";
import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Alert } from "@/components/ui/alert";
import { registerUser } from "../utils/api";

export default function RegisterForm({ onSuccess }) {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    profile: {
      user_type: "",
      phone_number: "",
      address: "",
      company_name: "",
    },
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name in form.profile) {
      setForm({ ...form, profile: { ...form.profile, [name]: value } });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Register</CardTitle>
      </CardHeader>
      <CardContent>
        <form
          className="flex flex-col gap-4"
          onSubmit={async (e) => {
            e.preventDefault();
            setError(null);
            setSuccess(null);
            const res = await registerUser(form);
            if (res.id) setSuccess("Registration successful!");
            else setError(res);
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
            <Label htmlFor="email">Email</Label>
            <Input
              name="email"
              type="email"
              value={form.email}
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
          <div>
            <Label htmlFor="first_name">First Name</Label>
            <Input
              name="first_name"
              value={form.first_name}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="last_name">Last Name</Label>
            <Input
              name="last_name"
              value={form.last_name}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label>User Type</Label>
            <Select
              value={form.profile.user_type}
              onValueChange={(val) =>
                setForm({
                  ...form,
                  profile: { ...form.profile, user_type: val },
                })
              }
              required
            >
              <SelectTrigger>
                <SelectValue placeholder="Select user type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="FARMER">Farmer</SelectItem>
                <SelectItem value="DISTRIBUTOR">Distributor</SelectItem>
                <SelectItem value="RETAILER">Retailer</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="phone_number">Phone Number</Label>
            <Input
              name="phone_number"
              value={form.profile.phone_number}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="address">Address</Label>
            <Input
              name="address"
              value={form.profile.address}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="company_name">Company Name</Label>
            <Input
              name="company_name"
              value={form.profile.company_name}
              onChange={handleChange}
            />
          </div>
          <Button type="submit" className="w-full">
            Register
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
