"use client";
import React, { useState } from "react";

const distributors = [
  { id: 1, name: "Fast Distributors" },
  { id: 2, name: "QuickBanana Logistics" },
];

export default function CreateShipmentButton({
  userType = "FARMER",
  onCreate,
}) {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    origin: userType === "FARMER" ? "Green Farms" : "Fast Distributors",
    destination: "",
    quantity: "",
    shipment_date: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onCreate) {
      onCreate({
        ...form,
        id: Date.now(),
        status: "PENDING",
        dominant_ripeness: "Unknown",
        shelf_life: "Unknown",
      });
    }
    setOpen(false);
    setForm({
      origin: userType === "FARMER" ? "Green Farms" : "Fast Distributors",
      destination: "",
      quantity: "",
      shipment_date: "",
    });
  };

  return (
    <>
      <button
        className="px-4 py-2 rounded bg-green-600 text-white hover:bg-green-700 transition"
        onClick={() => setOpen(true)}
      >
        + Create Shipment
      </button>
      {open && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <form
            className="bg-white dark:bg-gray-900 p-8 rounded shadow-lg min-w-[320px] flex flex-col gap-4"
            onSubmit={handleSubmit}
          >
            <h3 className="font-bold mb-2">Create Shipment</h3>
            <div>
              <label className="block text-sm mb-1">Origin</label>
              <input
                className="w-full rounded border px-2 py-1"
                name="origin"
                value={form.origin}
                disabled
                readOnly
              />
            </div>
            <div>
              <label className="block text-sm mb-1">Destination</label>
              <select
                className="w-full rounded border px-2 py-1"
                name="destination"
                value={form.destination}
                onChange={handleChange}
                required
              >
                <option value="">Select Distributor</option>
                {distributors.map((d) => (
                  <option key={d.id} value={d.name}>
                    {d.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm mb-1">Quantity</label>
              <input
                className="w-full rounded border px-2 py-1"
                name="quantity"
                type="number"
                min={1}
                value={form.quantity}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label className="block text-sm mb-1">Shipment Date</label>
              <input
                className="w-full rounded border px-2 py-1"
                name="shipment_date"
                type="date"
                value={form.shipment_date}
                onChange={handleChange}
                required
              />
            </div>
            <div className="flex gap-2 mt-4">
              <button
                type="button"
                className="px-4 py-2 rounded bg-gray-300 dark:bg-gray-700"
                onClick={() => setOpen(false)}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 rounded bg-green-600 text-white"
              >
                Create
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
}
