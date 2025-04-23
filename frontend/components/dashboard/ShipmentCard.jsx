"use client";
import React, { useState } from "react";

const dummyPrediction = {
  dominant_ripeness: "ripe",
  shelf_life: "2-4 days",
  ripeness_summary: { ripe: 8, unripe: 2 },
  image_url:
    "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?auto=format&fit=crop&w=400&q=80",
};

export default function ShipmentCard({ shipment }) {
  const [showTrack, setShowTrack] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [showDetail, setShowDetail] = useState(false);

  const handleImageUpload = (e) => {
    e.preventDefault();
    setPrediction(dummyPrediction);
    setShowUpload(false);
  };

  return (
    <>
      <div
        className="rounded border p-4 bg-white dark:bg-gray-800 shadow hover:shadow-lg transition-shadow cursor-pointer"
        onClick={() => setShowDetail(true)}
      >
        <div className="flex justify-between">
          <div>
            <div className="font-semibold">
              {shipment.origin} → {shipment.destination}
            </div>
            <div className="text-xs text-gray-500">
              Status: {shipment.status}
            </div>
          </div>
          <div className="text-xs text-gray-500">
            Date: {shipment.shipment_date}
          </div>
        </div>
        <div className="mt-2 text-sm">
          <div>
            <b>Quantity:</b> {shipment.quantity}
          </div>
          <div>
            <b>Dominant Ripeness:</b>{" "}
            {prediction
              ? prediction.dominant_ripeness
              : shipment.dominant_ripeness}
          </div>
          <div>
            <b>Shelf Life:</b>{" "}
            {prediction ? prediction.shelf_life : shipment.shelf_life}
          </div>
        </div>
        <div className="mt-2 flex gap-2">
          <button
            className="px-3 py-1 rounded bg-blue-600 text-white text-xs hover:bg-blue-700 transition"
            onClick={(e) => {
              e.stopPropagation();
              setShowTrack((v) => !v);
            }}
          >
            {showTrack ? "Hide Tracking" : "Track"}
          </button>
          <button
            className="px-3 py-1 rounded bg-yellow-600 text-white text-xs hover:bg-yellow-700 transition"
            onClick={(e) => {
              e.stopPropagation();
              setShowUpload(true);
            }}
          >
            Upload Image
          </button>
        </div>
        {showTrack && (
          <div className="mt-2 text-xs bg-gray-100 dark:bg-gray-900 p-2 rounded animate-fade-in">
            <div>
              <b>Tracking Info:</b>
            </div>
            <div>
              Current Location:{" "}
              {shipment.status === "IN_TRANSIT" ? "On the way" : "Warehouse"}
            </div>
            <div>Estimated Arrival: {shipment.shipment_date}</div>
          </div>
        )}
        {prediction && (
          <div className="mt-2 text-xs bg-green-100 dark:bg-green-900 p-2 rounded animate-fade-in">
            <div>
              <b>Ripeness Prediction:</b>
            </div>
            <div>Dominant: {prediction.dominant_ripeness}</div>
            <div>Shelf Life: {prediction.shelf_life}</div>
            <div>
              Summary:{" "}
              {Object.entries(prediction.ripeness_summary)
                .map(([k, v]) => `${k}: ${v}`)
                .join(", ")}
            </div>
          </div>
        )}
      </div>
      {/* Upload Modal */}
      {showUpload && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in">
          <form
            className="bg-white dark:bg-gray-900 p-8 rounded shadow-lg min-w-[320px] flex flex-col gap-4 animate-scale-in"
            onSubmit={handleImageUpload}
          >
            <h3 className="font-bold mb-2">Upload Banana Image</h3>
            <input type="file" accept="image/*" required />
            <div className="flex gap-2 mt-4">
              <button
                type="button"
                className="px-4 py-2 rounded bg-gray-300 dark:bg-gray-700"
                onClick={() => setShowUpload(false)}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 rounded bg-yellow-600 text-white"
              >
                Predict Ripeness
              </button>
            </div>
          </form>
        </div>
      )}
      {/* Detail Modal */}
      {showDetail && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 animate-fade-in">
          <div className="bg-white dark:bg-gray-900 p-8 rounded shadow-lg min-w-[350px] max-w-lg animate-scale-in relative">
            <button
              className="absolute top-2 right-2 text-xl text-gray-500 hover:text-red-500"
              onClick={() => setShowDetail(false)}
              aria-label="Close"
            >
              ×
            </button>
            <h2 className="text-2xl font-bold mb-2">Shipment Details</h2>
            <div className="mb-2">
              <b>Origin:</b> {shipment.origin}
            </div>
            <div className="mb-2">
              <b>Destination:</b> {shipment.destination}
            </div>
            <div className="mb-2">
              <b>Quantity:</b> {shipment.quantity}
            </div>
            <div className="mb-2">
              <b>Status:</b> {shipment.status}
            </div>
            <div className="mb-2">
              <b>Date:</b> {shipment.shipment_date}
            </div>
            <div className="mb-2">
              <b>Dominant Ripeness:</b>{" "}
              {prediction
                ? prediction.dominant_ripeness
                : shipment.dominant_ripeness}
            </div>
            <div className="mb-2">
              <b>Shelf Life:</b>{" "}
              {prediction ? prediction.shelf_life : shipment.shelf_life}
            </div>
            <div className="mb-2">
              <b>Ripeness Summary:</b>{" "}
              {prediction ? JSON.stringify(prediction.ripeness_summary) : "N/A"}
            </div>
            <div className="mb-2">
              <b>Banana Image:</b>
              <div className="mt-2">
                <img
                  src={
                    prediction
                      ? prediction.image_url
                      : "https://placehold.co/200x120?text=No+Image"
                  }
                  alt="Banana"
                  className="rounded shadow max-w-[200px] transition-transform hover:scale-105"
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
