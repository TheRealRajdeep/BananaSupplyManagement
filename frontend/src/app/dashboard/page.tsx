"use client";
import React, { useState } from "react";
import UserProfile from "../../../components/dashboard/UserProfile";
import ShipmentList from "../../../components/dashboard/ShipmentList";
import CreateShipmentButton from "../../../components/dashboard/CreateShipmentButton";

// Define the Shipment type
type Shipment = {
    id: number;
    origin: string;
    destination: string;
    quantity: number;
    status: string;
    shipment_date: string;
    dominant_ripeness: string;
    shelf_life: string;
};

// Define the Shipment type
const initialShipments: { [key in "FARMER" | "DISTRIBUTOR"]: Shipment[] } = {
    FARMER: [
        {
            id: 1,
            origin: "Green Farms",
            destination: "Fast Distributors",
            quantity: 1000,
            status: "IN_TRANSIT",
            shipment_date: "2024-06-01",
            dominant_ripeness: "unripe",
            shelf_life: "6-7 days",
        },
        {
            id: 2,
            origin: "Green Farms",
            destination: "Fast Distributors",
            quantity: 800,
            status: "DELIVERED",
            shipment_date: "2024-05-20",
            dominant_ripeness: "ripe",
            shelf_life: "2-4 days",
        },
    ],
    DISTRIBUTOR: [
        {
            id: 3,
            origin: "Green Farms",
            destination: "Fast Distributors",
            quantity: 500,
            status: "PENDING",
            shipment_date: "2024-06-10",
            dominant_ripeness: "freshripe",
            shelf_life: "4-6 days",
        },
        {
            id: 4,
            origin: "Green Farms",
            destination: "Fast Distributors",
            quantity: 1200,
            status: "IN_TRANSIT",
            shipment_date: "2024-06-05",
            dominant_ripeness: "unripe",
            shelf_life: "6-7 days",
        },
    ],
};

export default function DashboardPage() {
    const [userType, setUserType] = useState<"FARMER" | "DISTRIBUTOR">("FARMER");
    const [shipments, setShipments] = useState<{ [key in "FARMER" | "DISTRIBUTOR"]: Shipment[] }>(initialShipments);

    const handleCreateShipment = (shipment: Shipment) => {
        setShipments((prev) => ({
            ...prev,
            [userType]: [shipment, ...prev[userType]],
        }));
    };

    return (
        <div className="max-w-5xl mx-auto flex flex-col gap-8 py-8">
            <div className="flex gap-4 mb-4">
                <button
                    className={`px-4 py-2 rounded ${userType === "FARMER" ? "bg-green-700 text-white" : "bg-gray-200 dark:bg-gray-800 dark:text-white"}`}
                    onClick={() => setUserType("FARMER")}
                >
                    Farmer Dashboard
                </button>
                <button
                    className={`px-4 py-2 rounded ${userType === "DISTRIBUTOR" ? "bg-green-700 text-white" : "bg-gray-200 dark:bg-gray-800 dark:text-white"}`}
                    onClick={() => setUserType("DISTRIBUTOR")}
                >
                    Distributor Dashboard
                </button>
            </div>
            <UserProfile userType={userType} />
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold">Your Shipments</h2>
                <CreateShipmentButton userType={userType} onCreate={handleCreateShipment} />
            </div>
            <ShipmentList userType={userType} shipments={shipments[userType]} />
        </div>
    );
}
