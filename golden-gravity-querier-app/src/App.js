import React, { useState, useEffect } from 'react';

// Main App component for the Golden Gravity Spacetime Field Querier
function App() {
  // State variables for user input and generated insight
  const [phenomenon, setPhenomenon] = useState('');
  const [entanglementDensity, setEntanglementDensity] = useState('0.5'); // Default value
  const [insight, setInsight] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Define the PHI_PI constant, central to Golden Gravity
  const PHI_PI = 5.083203692;

  // Function to call the LLM and get a Golden Gravity insight
  const getGoldenGravityInsight = async () => {
    setIsLoading(true);
    setError('');
    setInsight(''); // Clear previous insight

    // Construct the prompt for the LLM based on Golden Gravity principles
    const prompt = `You are an AI assistant specializing in the Golden Gravity Framework.
    Given a scientific phenomenon and a conceptual entanglement density, provide a concise (2-3 sentences) insight from the perspective of Golden Gravity.
    Focus on how the (phi * pi) factor (approximately ${PHI_PI}) and quantum coherence (specifically the Spacetime Information Field (S) and Quantum Coherence Function (F_QC)) might influence or explain the phenomenon.
    
    Phenomenon: "${phenomenon}"
    Conceptual Entanglement Density (0-1, where higher values imply more coherence): "${entanglementDensity}"`;

    let chatHistory = [];
    chatHistory.push({ role: "user", parts: [{ text: prompt }] });
    const payload = { contents: chatHistory };
    const apiKey = ""; // Canvas will provide this at runtime if empty
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (result.candidates && result.candidates.length > 0 &&
          result.candidates[0].content && result.candidates[0].content.parts &&
          result.candidates[0].content.parts.length > 0) {
        const text = result.candidates[0].content.parts[0].text;
        setInsight(text);
      } else {
        setError('Failed to get insight. Please try again.');
        console.error('Unexpected API response structure:', result);
      }
    } catch (e) {
      setError(`Error fetching insight: ${e.message}. Please check your input.`);
      console.error('Fetch error:', e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-gray-100 p-4 sm:p-6 font-inter flex flex-col items-center justify-center">
      <div className="w-full max-w-4xl bg-gray-800 rounded-xl shadow-2xl p-6 sm:p-10 border border-purple-700">
        <h1 className="text-3xl sm:text-4xl font-bold text-center mb-6 text-purple-400">
          <span className="bg-gradient-to-r from-yellow-300 to-yellow-500 text-transparent bg-clip-text">Golden Gravity</span> Spacetime Field Querier
        </h1>
        <p className="text-center text-gray-300 mb-8 max-w-2xl mx-auto">
          Explore conceptual insights into scientific phenomena through the lens of the **Golden Gravity Framework**,
          where spacetime is a quantum-coherent information field influenced by the universal constant **$(\phi \cdot \pi) \approx {PHI_PI.toFixed(3)}$**.
        </p>

        {/* Input section */}
        <div className="mb-8 space-y-4">
          <div>
            <label htmlFor="phenomenon" className="block text-purple-300 text-lg font-medium mb-2">
              Scientific Phenomenon:
            </label>
            <input
              type="text"
              id="phenomenon"
              className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
              placeholder="e.g., Quantum Entanglement, Wormhole Stability, Consciousness"
              value={phenomenon}
              onChange={(e) => setPhenomenon(e.target.value)}
              disabled={isLoading}
            />
          </div>

          <div>
            <label htmlFor="entanglementDensity" className="block text-purple-300 text-lg font-medium mb-2">
              Conceptual Entanglement Density (0-1):
            </label>
            <input
              type="number"
              id="entanglementDensity"
              className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
              min="0"
              max="1"
              step="0.01"
              value={entanglementDensity}
              onChange={(e) => setEntanglementDensity(e.target.value)}
              disabled={isLoading}
            />
            <p className="text-sm text-gray-400 mt-1">
              Higher values suggest greater quantum coherence within the spacetime field.
            </p>
          </div>

          <button
            onClick={getGoldenGravityInsight}
            disabled={isLoading || !phenomenon || entanglementDensity === ''}
            className={`w-full py-3 px-6 rounded-lg font-bold text-lg transition duration-300 ease-in-out
              ${isLoading 
                ? 'bg-purple-600 cursor-not-allowed opacity-70' 
                : 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 transform hover:scale-105 shadow-lg'
              } focus:outline-none focus:ring-2 focus:ring-purple-500`}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating Insight...
              </span>
            ) : (
              'Generate Golden Gravity Insight'
            )}
          </button>
        </div>

        {/* Display Insight */}
        {error && (
          <div className="bg-red-900 bg-opacity-30 border border-red-700 text-red-300 p-4 rounded-lg mb-6 text-center">
            {error}
          </div>
        )}

        {insight && (
          <div className="bg-gray-700 rounded-xl p-6 sm:p-8 border border-purple-600 mt-8">
            <h2 className="text-2xl sm:text-3xl font-semibold text-purple-400 mb-4 text-center">
              Golden Gravity Insight:
            </h2>
            <p className="text-gray-200 leading-relaxed text-lg italic">
              "{insight}"
            </p>
          </div>
        )}

        {/* Conceptual disclaimer */}
        <p className="text-center text-gray-500 text-xs mt-10">
          This application provides conceptual insights based on the theoretical Golden Gravity Framework and is for illustrative purposes only.
        </p>
      </div>
    </div>
  );
}

export default App;
