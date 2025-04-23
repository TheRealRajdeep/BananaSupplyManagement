"use client";
import React from "react";

export default function UserProfile({ userType = "FARMER" }) {
  // Dummy user data for both types
  const user =
    userType === "FARMER"
      ? {
          username: "farmer_john",
          email: "john@farm.com",
          first_name: "John",
          last_name: "Doe",
          profile: {
            user_type: "FARMER",
            phone_number: "1234567890",
            address: "Village Road, Farmville",
            company_name: "Green Farms",
          },
        }
      : {
          username: "distributor_amy",
          email: "amy@distribute.com",
          first_name: "Amy",
          last_name: "Smith",
          profile: {
            user_type: "DISTRIBUTOR",
            phone_number: "9876543210",
            address: "City Center, Metro City",
            company_name: "Fast Distributors",
          },
        };

  return (
    <div className="rounded-lg border p-6 bg-gray-100 dark:bg-gray-900">
      <h2 className="text-xl font-semibold mb-2">
        Welcome, {user.first_name}!
      </h2>
      <div className="text-sm text-gray-700 dark:text-gray-300">
        <div>
          <b>Email:</b> {user.email}
        </div>
        <div>
          <b>Name:</b> {user.first_name} {user.last_name}
        </div>
        <div>
          <b>User Type:</b> {user.profile.user_type}
        </div>
        <div>
          <b>Phone:</b> {user.profile.phone_number}
        </div>
        <div>
          <b>Address:</b> {user.profile.address}
        </div>
        <div>
          <b>Company:</b> {user.profile.company_name}
        </div>
      </div>
    </div>
  );
}
