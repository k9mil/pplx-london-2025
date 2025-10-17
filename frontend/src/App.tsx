import React from "react";

function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden">
        <div className="p-8">
          <div className="uppercase tracking-wide text-sm text-indigo-500 font-semibold">
            Hello World
          </div>
          <p className="mt-2 text-gray-500">
            Welcome to your React + Vite + Tailwind + TypeScript app!
          </p>
          <button className="mt-4 px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600 transition-colors">
            Click me!
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
