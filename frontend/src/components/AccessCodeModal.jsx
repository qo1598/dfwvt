import React, { useState } from 'react';

const AccessCodeModal = ({ onVerify }) => {
    const [code, setCode] = useState("");
    const [error, setError] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (code) {
            // Simple client-side check or just pass it up
            onVerify(code);
        } else {
            setError(true);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white p-8 rounded-xl shadow-2xl max-w-sm w-full text-center">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">🖐 Access Restricted</h2>
                <p className="text-gray-600 mb-6">
                    To prevent excessive API usage, please enter the pilot access code.
                </p>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <input
                        type="text"
                        placeholder="Enter Code (e.g., PILOT...)"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                        className="w-full border-2 border-gray-300 p-3 rounded-lg focus:border-blue-500 focus:outline-none text-center text-lg uppercase tracking-widest"
                    />
                    {error && <p className="text-red-500 text-sm">Please enter a valid code.</p>}
                    <button
                        type="submit"
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-colors"
                    >
                        Enter Platform
                    </button>
                </form>
            </div>
        </div>
    );
};

export default AccessCodeModal;
