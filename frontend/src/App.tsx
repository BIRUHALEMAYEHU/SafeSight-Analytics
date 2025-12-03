import { useState, useEffect } from 'react'

interface HealthResponse {
  status: string
}

function App() {
  const [backendStatus, setBackendStatus] = useState<string>('checking...')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/health')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data: HealthResponse = await response.json()
        setBackendStatus(data.status)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setBackendStatus('error')
      }
    }

    checkBackendHealth()
    // Optionally refresh every 5 seconds
    const interval = setInterval(checkBackendHealth, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">
          SafeSight Analytics
        </h1>
        <div className="space-y-2">
          <p className="text-gray-600">
            Backend status: 
            <span className={`ml-2 font-semibold ${
              backendStatus === 'ok' 
                ? 'text-green-600' 
                : backendStatus === 'error' 
                ? 'text-red-600' 
                : 'text-yellow-600'
            }`}>
              {backendStatus}
            </span>
          </p>
          {error && (
            <p className="text-red-500 text-sm mt-2">
              Error: {error}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default App

