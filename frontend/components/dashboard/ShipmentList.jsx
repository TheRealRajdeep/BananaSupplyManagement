"use client";
import React from "react";
import ShipmentCard from "./ShipmentCard";

export default function ShipmentList({
  userType = "FARMER",
  shipments = [],
  onTrack,
}) {
  return (
    <div className="grid gap-4">
      {shipments.map((shipment) => (
        <ShipmentCard key={shipment.id} shipment={shipment} onTrack={onTrack} />
      ))}
    </div>
  );
}
